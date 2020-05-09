import os
from google.oauth2 import service_account
import io
from google.cloud import storage, vision
import csv
import boto3
from cloudmesh.common.util import path_expand
#from flask import jsonify

def detect_text_google() -> str:
    """
    Detects text in the file using Google Vision API.

    :return: p
    :return type: str
    """

    path = path_expand('~/.cloudmesh/google.json')
    # Get credentials
    credentials = service_account.Credentials.from_service_account_file(path)

    client = vision.ImageAnnotatorClient(credentials=credentials)

    path = path_expand('~/cm/cloudmesh-openapi/tests/image-analysis/sign_text.png')

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)

    try:
        texts = response.text_annotations

        p = texts[0].description
    except Exception as e:
        p = {'Text' : "error could not use image service"}
        print(e)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return p

def detect_text_aws() -> str:
    """
    Function that detects text from image using AWS Rekognition

    :return: p
    :return type: str
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
    try:
        text_detections = response['TextDetections']
        p = []
        for group in text_detections:
            p.append(group['DetectedText'])
    except Exception as e:
        p = {'Text' : "error could not use image service"}
        print(e)

    return ' '.join(p)
