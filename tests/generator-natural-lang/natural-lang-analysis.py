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
        credentials.cloudmesh__cloud__google__credentials__path_to_json_file)

    return credentials_list


def analyze(filename: str, cloud: str) -> float:
    """Run a sentiment analysis request on text within a passed filename.

    :param filename: The sentence to be analyzed
    :type filename: str
    :param cloud: The cloud to operate on
    :type cloud: str
    :return: score
    :return type: float

    """

    credentials_list = get_credentials()

    with open(filename, 'r') as review_file:
        # Instantiates a plain text document.
        content = review_file.read()

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
