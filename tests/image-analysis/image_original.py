import os
from google.oauth2 import service_account
import io
from google.cloud import storage, vision
from cloudmesh.common.util import path_expand
from flask import jsonify
from cloudmesh.common.debug import VERBOSE

# Get credentials
credentials = service_account.Credentials.from_service_account_file(
    path_expand('~/.cloudmesh/google.json'))


def detect_text() -> str:
    """
    Detects text in the file.

    Parameters:
        path (str): path to image file
    """

    client = vision.ImageAnnotatorClient(credentials=credentials)
    VERBOSE(client)

    path = path_expand('~/cm/cloudmesh-openapi/tests/image-analysis/sign_text.png')
    VERBOSE(path)

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    VERBOSE(content)

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    try:
        texts = response.text_annotations
        #print("{}".format(texts[0].description))

        p = {'Texts' : (texts[0].description)}
    except Exception as e:
        p = {'Text' : "error could not use image service"}
        print(e)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return jsonify(p)
