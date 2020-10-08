import argparse
import os
import re
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

"""
Set of functions to analyze a provided plain text document for language 
sentiment. 

Must provide Azure Cognitive Services API key and endpoint information from your
Azure Portal Text Analytics Resource.

Must provide Google Cloud Project Credentials from service account file
to run locally in your terminal profile.

Example from Google:
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"
"""

#Must be provided by user before this can be used effectively
key = ""
endpoint = ""

def subtraction(x: float, y: float) -> float:
    """
    subtraction int and float sample.

    :param x: x value
    :type x: int
    :param y: y value
    :type y: float
    :return: result
    :return type: float
    """
    return x - y

def uploadText(filename: str) -> str:
    with open(filename,'r') as review_file:
        content = review_file.read()

    return content

def analyze(filename: str, cloud: str) -> float:
    """Run a sentiment analysis request on text.

    :param filename: text file
    :type filename: str
    :param cloud: type of cloud service
    :type cloud: str
    :return: score
    :return type: float
    """

    with open(filename, 'r') as review_file:
        # Instantiates a plain text document.
        content = review_file.read()

    if cloud == "azure":
        credentials = CognitiveServicesCredentials(key)
        text_analytics_client = TextAnalyticsClient(endpoint=endpoint,
                                                    credentials=credentials)
        client = text_analytics_client

        documents = []

        sentences = re.split('\.|\?|!', content)

        for index, sentence in enumerate(sentences):
            new_doc = {"id": index,
                       "language": "en",
                       "text": sentence}
            documents.append(new_doc.copy())
        print(documents)
        response = client.sentiment(documents=documents)
    elif cloud == "google":
        client = language.LanguageServiceClient()

        document = types.Document(
            content=content,
            type=enums.Document.Type.PLAIN_TEXT)

        response = client.analyze_sentiment(document=document)
    else:
        print("Cloud not supported.")
    # print(response)

    score = response.document_sentiment.score
    magnitude = response.document_sentiment.magnitude
    print("------Google Natural Language Analysis------")
    for index, sentence in enumerate(response.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))
    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))

    return score

    # print_result(response, cloud)
    # return response


# def print_result(response, cloud):
#     """
#
#     :param response: response value of sentiment analysis
#     :type response: float
#     :param cloud: cloud service being used
#     :type cloud: str
#     :return: 0
#     """
#
#     if cloud == "azure":
#         print("------Azure Cognitive Services------")
#         for document in response.documents:
#             print("Sentence ", document.id, " has a sentiment score of ",
#                   "{:.2f}".format(document.score))
#     elif cloud == "google":
#         score = response.document_sentiment.score
#         magnitude = response.document_sentiment.magnitude
#         print("------Google Natural Language Analysis------")
#         for index, sentence in enumerate(response.sentences):
#             sentence_sentiment = sentence.sentiment.score
#             print('Sentence {} has a sentiment score of {}'.format(
#                 index, sentence_sentiment))
#         print('Overall Sentiment: score of {} with magnitude of {}'.format(
#             score, magnitude))
#     else:
#         print("Cloud not supported.")
#
#     return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'filename',
        help='The path to the file you would like to analyze')
    parser.add_argument('cloud', help="The cloud service you would like to use.")
    args = parser.parse_args()
    uploadText(args.movie_review_filename)
    # analyze(args.movie_review_filename, args.cloud)
