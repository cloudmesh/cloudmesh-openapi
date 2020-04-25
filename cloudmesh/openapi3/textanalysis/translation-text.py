import requests, uuid, json
import argparse
from google.cloud import translate
from cloudmesh.common.dotdict import dotdict


"""
User must manually assign key and project_id variables in function translate_text
 to their values from their Google Cloud and Azure Portal. Otherwise, 
 authentication will not work.
"""
def translate_text(cloud=str, text=str):

    if cloud == "azure":
        key = ''

        endpoint = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
        params = '&to=it'

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

        output_response(request, cloud)
    elif cloud == "google":
        client = translate.TranslationServiceClient()

        parent = client.location_path('project_id', "global")

        request = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",
            source_language_code="en-US",
            target_language_code="it",
        )

        output_response(request, cloud)
    else:
        print("Cloud not supported.")


def output_response(request, cloud):

    if cloud == "azure":
        response = request.json()
        print(
            json.dumps(response, sort_keys=True, indent=4,
                       separators=(',', ': ')))
    elif cloud == "google":
        for translation in request.translations:
            print(u"Translated text: {}".format(translation.translated_text))
    else:
        print("Cloud note supported.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument(
    #     'language',
    #     help='The language you would like to translate to')
    parser.add_argument('cloud',
                        help="The cloud service you would like to use.")
    parser.add_argument('text',
                        help="The text you would like to translate from english.")
    # parser.add_argument('credentials',
    #                     help="Provide your project ID or subscription key for Google Cloud or Azure, respectively.")
    args = parser.parse_args()

    translate_text(args.cloud, args.text)

