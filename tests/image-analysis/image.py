import os
from google.oauth2 import service_account
import io
from google.cloud import storage, vision
from cloudmesh.common.util import path_expand
from cloudmesh.openapi.registry.fileoperation import FileOperation
from flask import jsonify
#from cloudmesh.common.debug import VERBOSE

def upload() -> str:
    filename=FileOperation().file_upload()
    return filename

def detect_text() -> str:
    """
    Detects text in the file.
    :return: result
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
            # print("{}".format(texts[0].description))

        p = {'Texts' : (texts[0].description)}
    except Exception as e:
        p = {'Text' : "error could not use image service"}
        print(e)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return p
    #return jsonify(p)

