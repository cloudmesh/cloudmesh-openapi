from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from cloudmesh.common.util import path_expand
from pathlib import Path
from PIL import Image
import sys
import time
import requests


# Add Computer Vision subscription key to the environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# Add Computer Vision endpoint to the environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

'''
def file_upload() -> str:
    """
       This function will upload file into .cloudmesh/upload-file location
       This will first get upload file object from request.files function
       and then override this object in given location.
    """
    file = connexion.request.files.get("upload")
    filename = file.filename
    if file:
        file_path = f"~/.cloudmesh/upload-file"
        p = Path(path_expand(file_path))
        p.mkdir(parents=True, exist_ok=True)
        file.save(f'{p.absolute()}/{filename}')
    return filename
'''


def get_text_results(image_name: str) -> str:
    """
    Read text from an image
    This example describes the contents of a text image

    Parameters:
        image_name (str): Name of the image file
    """
    # ComputerVision describe service URL
    ocr_url = endpoint + "vision/v2.1/ocr"

    # Set image_path to the local path of an image
    file_path = f"~/.cloudmesh/upload-file"

    p = Path(path_expand(file_path))

    image_path = p/image_name  # set image path

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()

    print("===== Read text from an image =====")
    # Call API
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'language': 'unk',
              'detectOrientation':'true'}

    response = requests.post(ocr_url, headers=headers, data=image_data)

    response.raise_for_status()

    read_text = response.json()
    #print(read_text
    return read_text
