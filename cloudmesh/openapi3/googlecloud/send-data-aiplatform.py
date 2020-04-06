from googleapiclient import discovery
from googleapiclient import errors
from oauth2client.client import GoogleCredentials
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.Shell import Shell
from google.cloud import storage
from google.cloud import bigquery

class GCloudSetup:

    def __init__(self, project_id, bucket_name, region, local_data):

        self.project_id = project_id
        self.bucket_name = bucket_name
        self.region = region
        self.local_data = local_data

    def test_function(self):
        client = bigquery.Client()

        query_job = client.query("""
            SELECT
              CONCAT(
                'https://stackoverflow.com/questions/',
                CAST(id as STRING)) as url,
              view_count
            FROM `bigquery-public-data.stackoverflow.posts_questions`
            WHERE tags like '%google-bigquery%'
            ORDER BY view_count DESC
            LIMIT 10""")

    def load_local_file(self, dataset, table):

        client = bigquery.Client()
        filename = self.local_data
        dataset_id = dataset
        table_id = table

        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.skip_leading_rows = 1
        job_config.autodetect = True

        with open(filename, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_ref,
                                              job_config=job_config)

        job.result()  # Waits for table load to complete.

        print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id,
                                              table_id))

        results = query_job.result()
    # def create_client_object(self, name, account_details_file):
    #
    #     client = storage.Client
    #     client.create_bucket(name)
    #
    #     account_data = open(account_details_file, "r")
    #     data = account_data.read()
    #     data = dotdict(data)
    #
    #     # Set properties on a plain resource object.
    #     # bucket = storage.Bucket(name)
    #     # bucket.location = data.cloudmesh.storage.google.default.Location
    #     # bucket. = "COLDLINE"
    #     # Pass that resource object to the client.
    #     # API request.
    #
    # def parse_credentials(self, account_details_path):
    #
    #     account_data = dotdict(account_details_path)
    #
    #     gcloud_project_id = account_data.cloudmesh.storage.google.credentials.project_id
    #     bucket_name = account_data.cloudmesh.storage.google.default.Link_for_gsutil
    #     sub_bucket_name = gcloud_project_id + "-aiplatform"
    #     region = account_data.cloudmesh.storage.google.default.Location
    #
    #     storage_credentials = {}
    #
    #     storage_credentials.append(gcloud_project_id, region, bucket_name, sub_bucket_name)
    #
    #     Shell.run("gsutil mb -l " + region + " " + bucket_name + sub_bucket_name)
    #
    #     return storage_credentials
    #
    # def upload_model_gcloud(self, model, bucket):
    #
    #     Shell.run("gsutil cp " + model + " " + bucket + "/" + model)
