import re
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import requests, uuid, json, yaml, os
from google.cloud import translate
from cloudmesh.common.FlatDict import flatten
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.Shell import Shell
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.common.util import path_expand
from pathlib import Path
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate

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


def get_credentials():
    credential_file = os.environ['CLOUDMESH_CREDENTIALS_YAML']
    credentials_list = []
    with open(credential_file) as file:
        documents = yaml.full_load(file)
    credentials = flatten(documents)
    credentials = dotdict(credentials)

    # add needed credentials to the credentials array
    credentials_list.append(
        credentials.cloudmesh__cloud__azure__credentials__AZURE_TRANSLATOR_KEY)
    credentials_list.append(
        credentials.cloudmesh__cloud__azure__credentials__AZURE_TEXT_ANALYTICS_KEY)
    credentials_list.append(
        credentials.cloudmesh__cloud__azure__credentials__AZURE_TEXT_ANALYTICS_ENDPOINT)
    credentials_list.append(
        credentials.cloudmesh__cloud__google__credentials__auth)

    return credentials_list


@DatabaseUpdate()
def add_file(fileName, **kwargs):
    """
    Adds the contents of a file located in the specified location to the registry

    :param fileName: The name of the file containing text
    :return:
    """
    cache_path = "~/.cloudmesh/text-cache/"
    p = Path(path_expand(cache_path))
    file_location = str(p) + "/" + fileName
    file_list = Shell.run("ls " + cache_path)
    file_list = file_list.split("\n")
    file_list.pop()

    if fileName in file_list:
        with open(file_location, 'r') as review_file:
            # Instantiates a plain text document.
            content = review_file.read()

        entry = {
            "cm": {
                "cloud": "local",
                "kind": "text",
                "name": fileName,
                "driver": None
            },
            "name": fileName,
            "content": content
        }

    for key in kwargs:
        entry[key] = kwargs[key]

    return entry


def load_content(fileName):
    """
    Load the content from the entry if it exists in the mongo db local-text
    collection

    :param fileName: name of the file contents being accessed
    :return:
    """

    db = CmDatabase()
    result = db.find(collection="local-text",
                      cloud="local",
                      kind="text",
                      query={"name": f"{fileName}"})
    result = flatten(result)
    result.pop()
    return result[0]["content"]


def analyze(filename: str, cloud: str) -> float:
    """Run a sentiment analysis request on text within a passed filename.

    :param filename: The sentence to be analyzed
    :type filename: str
    :param cloud: The cloud to operate on
    :type cloud: str
    :return: score
    :return type: float

    """

    # get credentials for Google and Azure cloud text services listed in
    # cloudmesh yaml
    credentials_list = get_credentials()

    # add file located in text cache directory to the registry so it can be
    # loaded and passed to services.
    add_file(filename)
    content = load_content(filename)

    if cloud == "azure":
        credentials = CognitiveServicesCredentials(credentials_list[1])
        endpoint = credentials_list[2]
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
        response = client.sentiment(documents=documents)
    elif cloud == "google":
        client = language.LanguageServiceClient()

        document = types.Document(
            content=content,
            type=enums.Document.Type.PLAIN_TEXT)

        response = client.analyze_sentiment(document=document)
    else:
        print("Cloud not supported.")

    if cloud == "azure":
        print("------Azure Cognitive Services------")
        for document in response.documents:
            print("Sentence ", document.id, " has a sentiment score of ",
                  "{:.2f}".format(document.score))
            return document.score
    elif cloud == "google":
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


def translate_text(cloud: str, text: str, lang: str) -> str:

    """Run a sentiment analysis request on text within a passed filename.

        :param text: The sentence to be translated
        :type text: str
        :param cloud: The cloud to operate on
        :type cloud: str
        :return: response
        :return type: str
        """

    credentials = get_credentials()

    if cloud == "azure":
        key = credentials[0]

        endpoint = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
        params = '&to=' + lang

        full_url = endpoint + params
        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': text
        }]

        request = requests.post(full_url, headers=headers, json=body)

        response = request.json()
        print(
            json.dumps(response, sort_keys=True, indent=4,
                       separators=(',', ': ')))
        return response
    elif cloud == "google":
        client = translate.TranslationServiceClient()

        parent = client.location_path('project_id', 'global')

        request = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",
            source_language_code="en-US",
            target_language_code=lang
        )

        for translation in request.translations:
            print(u"Translated text: {}".format(
                translation.translated_text))
            response = translation.translated_text
        return response
    else:
        print("Cloud not supported.")
