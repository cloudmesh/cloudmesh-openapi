from googleapiclient import discovery
from googleapiclient import errors
from oauth2client.client import GoogleCredentials
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.Shell import Shell

ml = discovery.build('ml','v1')

project_id = 'projects/{}'.format('my-first-project-273222')

request_dict = {'name': 'model name',
                'description': 'This is a test description'}

request = ml.projects().models().create(parent=project_id, body=request_dict)

response = request.execute()


class GCloudSetup:

    def __init__(self, project_id, bucket_name, region):

        self.project_id = project_id
        self.bucket_name = bucket_name
        self.region = region


    def parse_credentials(self, account_details_path):

        account_data = dotdict(account_details_path)

        gcloud_project_id = account_data.cloudmesh.storage.google.credentials.project_id
        bucket_name = account_data.cloudmesh.storage.google.default.Link_for_gsutil
        sub_bucket_name = gcloud_project_id + "-aiplatform"
        region = account_data.cloudmesh.storage.google.default.Location

        storage_credentials = {}

        storage_credentials.append(gcloud_project_id, region, bucket_name, sub_bucket_name)

        Shell.run("gsutil mb -l " + region + " " + bucket_name + sub_bucket_name)

        return storage_credentials

    def upload_model_gcloud(self, model, bucket):

        Shell.run("gsutil cp " + model + " " + bucket + "/" + model)
