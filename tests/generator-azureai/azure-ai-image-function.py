import os
import requests
import sys
from cloudmesh.common.util import path_expand
import connexion
from pathlib import Path


# Get Computer Vision subscription key from the environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# Get Computer Vision endpoint from the environment variables.
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

def get_image_desc(image_name: str) -> str:
    """
    Describe an Image
    This example describes the contents of an image with the confidence score.

    Parameters:
        image_name (str): Name of the image+extension
    """
    # ComputerVision describe service URL
    describe_url = endpoint + "vision/v2.1/describe"

    # Set image_path to the local path of an image
    file_path = f"~/.cloudmesh/upload-file"

    p = Path(path_expand(file_path))

    image_path = p/image_name  # set image path

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()

    print("===== Describe an image =====")
    # Call API
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}

    response = requests.post(describe_url, headers=headers, data=image_data)
    response.raise_for_status()

    # The 'describe' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    image_description = response.json()
    #print(image_description)
    return image_description

def get_image_analysis(image_name: str) -> str:
    """
    Analyze an Image
    This example analyzes the contents of an image with the confidence score.

    Parameters:
        image_name (str): Name of the image+extension
    """
    # ComputerVision analyze service URL
    analyze_url = endpoint + "vision/v2.1/analyze"

    # Set image_path to the local path of an image
    file_path = f"~/.cloudmesh/upload-file"

    p = Path(path_expand(file_path))

    image_path = p/image_name  # set image path

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()

    print("===== Analyze an image =====")
    # Call API
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}

    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'describe' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    image_analysis = response.json()
    #print(image_analysis)
    return image_analysis

def get_image_tags(image_name: str) -> str:
    """
    Generate list of tags for input image with confidence score.

    Parameters:
        image_name (str): Name of the image+extension
    """
    # ComputerVision tag service URL
    tag_url = endpoint + "vision/v2.1/tag"

    # Set image_path to the local path of an image
    file_path = f"~/.cloudmesh/upload-file"

    p = Path(path_expand(file_path))

    image_path = p/image_name  # set image path

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()

    print("===== Analyze an image =====")
    # Call API
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    #params = {'visualFeatures': 'Categories,Description,Color'}

    response = requests.post(tag_url, headers=headers, data=image_data)
    response.raise_for_status()

    # The 'describe' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    image_tags = response.json()
    #print(image_tags)
    return image_tags
