from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
import image
import sys
import time


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

#Authenticate the client
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

#remote_image_URL = "./images/landmark.jpg"

def get_image_desc(remote_image_url: str) -> str:
    """
    adding float and float.

    :param remote_image_url: x value
    :type remote_image_url: str
    :return type: str
    """
    print("===== Describe an image - remote =====")
    # Call API
    description_results = computervision_client.describe_image(remote_image_url)

    # Get the captions (descriptions) from the response, with confidence level
    print("Description of remote image: ")
    if (len(description_results.captions) == 0):
        print("No description detected.")
    else:
        for caption in description_results.captions:
            print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))

def get_image_category(remote_image_url: str) -> str:
    """
    adding float and float.

    :param remote_image_url: x value
    :type remote_image_url: str
    :return type: str
    """
    print("===== Categorize an image - remote =====")
    # Select the visual feature(s) you want.
    remote_image_features = ["categories"]
    # Call API with URL and features
    categorize_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features)

    # Print results with confidence score
    print("Categories from remote image: ")
    if (len(categorize_results_remote.categories) == 0):
        print("No categories detected.")
    else:
        for category in categorize_results_remote.categories:
            print("'{}' with confidence {:.2f}%".format(category.name, category.score * 100))

def get_image_tags(remote_image_url: str) -> str:
    """
    adding float and float.

    :param remote_image_url: x value
    :type remote_image_url: str
    :return type: str
    """
    print("===== Tag an image - remote =====")
    # Call API with remote image
    tags_result_remote = computervision_client.tag_image(remote_image_url)

    # Print results with confidence score
    print("Tags in the remote image: ")
    if (len(tags_result_remote.tags) == 0):
        print("No tags detected.")
    else:
        for tag in tags_result_remote.tags:
            print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))


