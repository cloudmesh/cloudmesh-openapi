#!/usr/bin/python
import boto3
from time import sleep
import subprocess
import pandas as pd
import numpy as np
from cloudmesh.configuration.Config import Config
from AIServices import AIServices
import os
from flask import jsonify
from cloudmesh.openapi.registry.fileoperation import FileOperation
import connexion
from pathlib import Path
from cloudmesh.common.util import path_expand
from cloudmesh.common.StopWatch import StopWatch


AIServObj = AIServices('aws')

def get_supported_times_series_services():
    """
    Provides list of AI Time Series Services Supported
    :param name:
    :return:
           list of Time Series Forecasting Services Supported
    """
    req_info = "Supported Time Series Forecast Services AWS : Forecast "
    pinfo = {"model": req_info}
    return jsonify(pinfo)

def init_cloud_param(cloudname='None'):
    """
    Initializes the requested cloud parameters

    :param name: if none or not supported value, return a message
    unsupported cloud
    :return:
         whether the requested cloud services was initializaed successfully or not
    """
    if cloudname=='aws':
        AIServObj.init_cloud_params(cloudname)
        pinfo = {"model": 'AWS AI Service initialized successfully'}
    elif cloudname=='azure':
        AIServObj.init_cloud_params(cloudname)
        pinfo = {"model": 'Azure AI Service initialized successfully'}
    else :
        pinfo={"model":'No AI Service initialized successfully'}
    return jsonify(pinfo)

def upload() -> str:
    """
    Uploads the provided data file to .cloudmesh/upload-file directory
    :param name: file name
    :return:
           filename
     """
    filename=FileOperation().file_upload()
    returnstr= filename + ' uploaded successfully'
    return returnstr

def updatedf(x,setval):
    """
    update the negative values to requested value
    :param name: each row of the column
                 setval: value to be set
    :return:
        updated value of the row for the column
    """
    if x < 0 :
        x=setval
    return x

def updateNan(x):
     return x.fillna(0)


def validate() -> str:
    """
    update the negative values to requested value
    :param name: each row of the column
                setval: value to be set
    :return:
        updated value of the row for the column
    """
    file = connexion.request.files.get("upload")
    filename = file.filename
    if file:
        import datetime
        import os
        path = f"~/.cloudmesh/upload-file"
        file_path = os.path.join(path, filename)
        df = pd.read_csv(file_path)

        numerics = ['int16', 'int32', 'int64']
        for c in [c for c in df.columns if df[c].dtype in numerics]:
                 df[c] = df[c].applymap(np.int64)

        df = df.apply(lambda x: updateNan(x))

        df['target_value'] = df['target_value'].astype(int)

        AIServObj.df = df
        returnStr = filename + ' validated successfully'
    return returnStr

def split_train_test(data,percentage=0.3):
    """
        update the negative values to requested value
        :param name:
            split the data into specified percentage
        return:
            confirms if data was split correctly and individual data sets were created
    """
    from sklearn.model_selection import train_test_split
    x_train ,x_test = train_test_split(data,test_size=percentage)
    return x_train, x_test

def split_data_train_test(split_pct=0.3):
    """
    update the negative values to requested value
    :param name:
        split the data into specified percentage
    return:
        confirms if data was split correctly and individual data sets were created
    """
    split_pct=float(split_pct/100)

    if hasattr(AIServObj, 'df'):
        train_df, test_df= split_train_test(AIServObj.df,split_pct)
        StopWatch.start('to_csv')
        train_df.to_csv("aiservices-train.csv", header=False, index=False)
        test_df.to_csv("aiservices-test.csv", header=False, index=False)
        StopWatch.stop('to_csv')
    else:
        return 'Please validate the data first'
    return 'Data split successfully'


def generate_forecast(country='United Kingdom'):
    """
    Upload the training dataset to cloud storgae store(AWS= S3)
    Create a Dataset Group.
    Create a Dataset, in Forecast there are 3 types of dataset,
    Import data into Forecast from AWS Storage S3
    Train a model
    Create a Predictor
    Create a Forecast

    :param name:
        split the data into specified percentage
    return:
        confirms if data was split correctly and individual data sets were created
    """
    import botocore
    AIServObj.key = "aiservices-train.csv"

    if hasattr(AIServObj, 'bucket_name'):

        StopWatch.start('to_s3')
        boto3.Session().resource('s3').Bucket(AIServObj.bucket_name).Object(AIServObj.key).upload_file("aiservices-train.csv")
        StopWatch.stop('to_s3')
        datasetGroupArn=AIServObj.createDatasetGroup()

        if hasattr(AIServObj, 'datasetGroupArn'):
            datasetArn=AIServObj.createDataset()

            if hasattr(AIServObj, 'datasetArn'):
                ds_import_job_arn=AIServObj.createDatsetImport()

                if hasattr(AIServObj, 'ds_import_job_arn'):
                   predictor_arn=AIServObj.createPredictor()

                   if hasattr(AIServObj, 'predictor_arn'):
                        forecast_arn=AIServObj.createForecast()
                   else:
                       AIServObj.forecast_srv.delete_predictor(PredictorArn=AIServObj.predictor_arn)
                       AIServObj.forecast_srv.delete_dataset_import_job(DatasetImportJobArn=AIServObj.ds_import_job_arn)
                       AIServObj.forecast_srv.delete_dataset(DatasetArn=AIServObj.datasetArn)
                       AIServObj.forecast_srv.delete_dataset_group(DatasetGroupArn=AIServObj.datasetGroupArn)
                       boto3.Session().resource('s3').Bucket(AIServObj.bucket_name).Object(AIServObj.key).delete()
                       return "Algorithm encountered an error while creating Forecast"
                else:
                    AIServObj.forecast_srv.delete_dataset_import_job(DatasetImportJobArn=AIServObj.ds_import_job_arn)
                    AIServObj.forecast_srv.delete_dataset(DatasetArn=AIServObj.datasetArn)
                    AIServObj.forecast_srv.delete_dataset_group(DatasetGroupArn=AIServObj.datasetGroupArn)
                    boto3.Session().resource('s3').Bucket(AIServObj.bucket_name).Object(AIServObj.key).delete()
                    return "Algorithm encountered an error while creating Predictor"
            else:
                AIServObj.forecast_srv.delete_dataset(DatasetArn=AIServObj.datasetArn)
                AIServObj.forecast_srv.delete_dataset_group(DatasetGroupArn=AIServObj.datasetGroupArn)
                boto3.Session().resource('s3').Bucket(AIServObj.bucket_name).Object(AIServObj.key).delete()
                return "Algorithm encountered an error while creating import Job"

        else:
            AIServObj.forecast_srv.delete_dataset_group(DatasetGroupArn=AIServObj.datasetGroupArn)
            boto3.Session().resource('s3').Bucket(AIServObj.bucket_name).Object(AIServObj.key).delete()
            return "Algorithm encountered an error while creating Data set"
    else:
        return 'Please initialize cloud service'

    return "Forecast generated successfully"

def queryGeneratedForecast(countryName):
    '''
    Query the generated Forecast
    :param countryName:
    :return: Response from the generated query
    '''
    if hasattr(AIServObj, 'forecast_arn'):
        forecastResponse=AIServObj.queryForecast(countryName)
    else:
        return "Execute create forecast first"

    AIServObj.forecastResponse=forecastResponse
    return forecastResponse
