import csv
import boto3
from google.cloud import vision

def detect_handwriting(service, image):
    pass


def detect_text(service: str, path: str) ->str:
    if service in ('aws', 'google'):
        if service == 'google':
            credentials = 'figure out how to implement'

            client = vision.ImageAnnotatorClient(credentials=credentials)

            with open(path, 'rb') as image_file:
                content = image_file.read()

            image = vision.types.Image(content=content)

            response = client.text_detection(image=image)
            texts = response.text_annotations
            # print("{}".format(texts[0].description))
            print('Texts: \n{}'.format(texts[0].description))

            if response.error.message:
                raise Exception(
                    '{}\nFor more info on error messages, check: '
                    'https://cloud.google.com/apis/design/errors'.format(
                        response.error.message))

        elif service == 'aws':
            access_key_id = 'figure out how to implement'
            secret_access_key = 'figure out how to implement'

            client = boto3.client('rekognition',
                                  aws_access_key_id=access_key_id,
                                  aws_secret_access_key=secret_access_key)

            with open(path, 'rb') as image_file:
                content = image_file.read()

            response = client.detect_text(
                Image={
                    'Bytes': content,
                    # 'S3Object': {
                    #    'Bucket': 'string',
                    #    'Name': 'string',
                    #    'Version': 'string'
                    # }
                },
                Filters={
                    'WordFilter': {
                        'MinConfidence': 95
                        #        'MinBoundingBoxHeight': ...,
                        #        'MinBoundingBoxWidth': ...
                        #    },
                        #    'RegionsOfInterest': [
                        #        {
                        #            'BoundingBox': {
                        #                'Width': ...,
                        # 'Height': ...,
                        # 'Left': ...,
                        # 'Top': ...
                    }
                },
                # ]
                # }
            )

            text_detections = response['TextDetections']

            for group in text_detections:
                print(group['DetectedText'])

            if response.error.message:
                raise Exception(
                    '{}\nFor more info on error messages, check: '
                    'https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html'.format(
                        response.error.message))
    else:
        print('Service not available')



def detect(service, kind, image):
    pass


#service in aws, google
#kind in handwriting, text

#~ /.cloudmesh / cloudmesh.yaml
