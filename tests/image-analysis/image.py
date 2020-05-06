import os
from google.oauth2 import service_account
import io
from google.cloud import storage, vision
from cloudmesh.common.util import path_expand
from cloudmesh.openapi.registry.fileoperation import FileOperation
from flask import jsonify
#from cloudmesh.common.debug import VERBOSE

'''
def geturl(x) -> str:
    """
    upload function

    :return:
    """
    return f'http://localhost:8080/cloudmesh/image/image_url?x={x}'
'''

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
    #image = vision.types.Image()
    #image.source.image_uri = geturl('https://cdn.searchenginejournal.com/wp-content/uploads/2014/09/google-logo-760x380.png')

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

    return jsonify(p)


