import csv
import boto3
from cloudmesh.common.util import path_expand
from flask import jsonify

def detect_text() -> str:
    """
    Function that detects text from image

    :param path:
    :return:
    """

    # get credentials
    with open(path_expand('~/cm/aws-credentials.csv'), 'r') as input:
        next(input)
        reader = csv.reader(input)
        for line in reader:
            access_key_id = line[2]
            secret_access_key = line[3]

    client = boto3.client('rekognition',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key)

    path = path_expand('~/cm/cloudmesh-openapi/tests/image-analysis/sign_text.png')

    with open(path, 'rb') as image_file:
        content = image_file.read()


    response = client.detect_text(
        Image={
            'Bytes': content,
            #'S3Object': {
            #    'Bucket': 'string',
            #    'Name': 'string',
            #    'Version': 'string'
            #}
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
                        #'Height': ...,
                        #'Left': ...,
                        #'Top': ...
                    }
                },
            #]
        #}
    )

    text_detections = response['TextDetections']
    p = []
    for group in text_detections:
        p.append(group['DetectedText'])

    return jsonify({'text': p})
