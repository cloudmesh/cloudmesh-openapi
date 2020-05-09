class AIServices:

    def __init__(self,cloudname='None'):
        '''
        Initialize function for the AI Service class
        currently support AWS Forecast Service
        :param cloudname:
        '''
        print("Time Series Service initialized")

    def init_cloud_params(self,cloudname):
        '''
        Initialize cloud parameter for the service requested
        support AWS forecast service
        :param cloudname:
        :return:
        '''

        from cloudmesh.configuration.Config import Config
        self.conf = Config()["cloudmesh"]
        self.user = Config()["cloudmesh"]["profile"]["user"]
        self.spec = self.conf["cloud"][cloudname]
        self.cloudname = cloudname
        print(self.spec)
        self.default = self.spec["default"]
        self.cloudtype = self.spec["cm"]["kind"]

        if self.cloudtype=='aws':
            self.bucket_name = self.spec["cm"]["bucket_name"]
            self.region_name = self.spec["cm"]["region_name"]
            self.forecast = self.spec["cm"]["forecast_srv"]
            self.forecastquery_srv = self.spec["cm"]["forecastquery_srv"]
            self.s3_srv = self.spec["cm"]["s3_srv"]
            self.role_arn = self.spec["cm"]["iam_role_arn"]
            self.algorithmArn = self.spec["cm"]["algorithmArn"]

            import boto3
            self.session = boto3.Session(region_name=self.region_name)
            self.forecast_srv = self.session.client(service_name=self.forecast)
            self.forecastquery = self.session.client(service_name=self.forecastquery_srv)

            print("AWS Cloud was requested")
        elif self.cloudname == 'azure':
            print("Azure cloud was requested")
        else :
            print("Supported cloud services at this time : ")


    def createDatasetGroup(self):
        '''
        Create Dataset Group required for AWS Forecasting Service
        :return:
        '''
        from cloudmesh.common.StopWatch import StopWatch

        import time

        def create_uuid(project_name):
            import random
            id=random.randrange(100000)
            return project_name + '_' + str(id)

        self.DATASET_FREQUENCY = "D"
        self.TIMESTAMP_FORMAT = "yyyy-MM-dd hh:mm:ss"
        proj = 'timeseries'
        self.project=create_uuid(proj)

        self.datasetName = self.project + '_ds'
        self.datasetGroupName = self.project + '_dsg'
        self.s3DataPath = "s3://" + self.bucket_name + "/" + self.key

        StopWatch.start('to_dsg')
        create_dataset_group_response = self.forecast_srv.create_dataset_group(DatasetGroupName=self.datasetGroupName,
                                                                          Domain="CUSTOM", )
        datasetGroupArn = create_dataset_group_response['DatasetGroupArn']
        self.datasetGroupArn=datasetGroupArn
        StopWatch.stop('to_dsg')
        print(StopWatch.get('to_dsg'))
        return self.datasetGroupArn

    def createDataset(self):
        import json
        import os
        home1 = os.path.expanduser('~')
        file_path = os.path.join(home1, '.cloudmesh', 'upload-file','schema.json')
        print(file_path)

        with open(file_path) as json_file:
            schema = json.load(json_file)

        print(self.datasetName)
        print(schema)

        response = self.forecast_srv.create_dataset(
            Domain="CUSTOM",
            DatasetType='TARGET_TIME_SERIES',
            DatasetName=self.datasetName,
            DataFrequency=self.DATASET_FREQUENCY,
            Schema=schema
        )
        datasetArn = response['DatasetArn']
        self.datasetArn=datasetArn
        self.forecast_srv.update_dataset_group(DatasetGroupArn=self.datasetGroupArn, DatasetArns=[self.datasetArn])

        return self.datasetArn

    def createDatsetImport(self):

        import time

        datasetImportJobName = self.project + '_IMPORT_JOB'
        ds_import_job_response = self.forecast_srv.create_dataset_import_job(DatasetImportJobName=datasetImportJobName,
                                                                    DatasetArn=self.datasetArn,
                                                                    DataSource={
                                                                        "S3Config": {
                                                                            "Path": self.s3DataPath,
                                                                            "RoleArn": self.role_arn
                                                                        }
                                                                    },
                                                                    TimestampFormat=self.TIMESTAMP_FORMAT
                                                                    )
        ds_import_job_arn = ds_import_job_response['DatasetImportJobArn']

        while True:
            status = self.forecast_srv.describe_dataset_import_job(DatasetImportJobArn=ds_import_job_arn)['Status']
            if status in ('ACTIVE', 'CREATE_FAILED'): break
            time.sleep(10)

        self.ds_import_job_arn=ds_import_job_arn
        return self.ds_import_job_arn

    def createPredictor(self):
        self.predictorName = self.project + '_deeparp_algo'
        forecastHorizon = 24
        create_predictor_response = self.forecast_srv.create_predictor(PredictorName=self.predictorName,
                                                              AlgorithmArn=self.algorithmArn,
                                                              ForecastHorizon=forecastHorizon,
                                                              PerformAutoML=False,
                                                              PerformHPO=False,
                                                              EvaluationParameters={"NumberOfBacktestWindows": 1,
                                                                                    "BackTestWindowOffset": 24},
                                                              InputDataConfig={"DatasetGroupArn": self.datasetGroupArn},
                                                              FeaturizationConfig={"ForecastFrequency": "D",
                                                                                   "Featurizations":
                                                                                       [
                                                                                           {
                                                                                               "AttributeName": "target_value",
                                                                                               "FeaturizationPipeline":
                                                                                                   [
                                                                                                       {
                                                                                                           "FeaturizationMethodName": "filling",
                                                                                                           "FeaturizationMethodParameters":
                                                                                                               {
                                                                                                                   "frontfill": "none",
                                                                                                                   "middlefill": "zero",
                                                                                                                   "backfill": "zero"}
                                                                                                           }
                                                                                                   ]
                                                                                               }
                                                                                       ]
                                                                                   }
                                                              )
        predictor_arn = create_predictor_response['PredictorArn']
        import time

        while True:
            status = self.forecast_srv.describe_predictor(PredictorArn=predictor_arn)['Status']
            if status in ('ACTIVE', 'CREATE_FAILED'): break
            time.sleep(10)

        self.predictor_arn=predictor_arn
        return self.predictor_arn

    def createForecast(self):

        forecastName = self.project + '_deeparp_algo_forecast'
        create_forecast_response = self.forecast_srv.create_forecast(ForecastName=forecastName,
                                                            PredictorArn=self.predictor_arn)
        forecast_arn = create_forecast_response['ForecastArn']

        import time

        while True:
            status = self.forecast_srv.describe_forecast(ForecastArn=forecast_arn)['Status']
            if status in ('ACTIVE', 'CREATE_FAILED'): break
            time.sleep(10)

        self.forecast_arn=forecast_arn
        return self.forecast_arn

    def queryForecast(self,countryname):

        forecastResponse = self.forecastquery.query_forecast(
            ForecastArn=self.forecast_arn,
            Filters={"item_id": countryname}
        )
        self.forecastResponse=forecastResponse
        self.countryname=countryname
        return self.forecastResponse
