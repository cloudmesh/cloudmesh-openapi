import cms
from cloudmesh.common.Printer import Printer
from flask import Flask
from flask import jsonify
from flask import request

return_json = True

app = Flask(__name__)


# note when wservicee get NOne back the service shoudl return
# ('', 204) # e.g. result not found this is handlesd in openapi
#

def FORMAT(data, output):
    if output == 'json' or output == None:
        data = jsonify(data)
    elif output == 'html':
        data = Printer.write(data, output="html")
    return data


def test(service: str) -> dict:
    return {"test": "hello"}


@app.route('/cloudmesh/vm/<string:service>')
def vm(service: str) -> list:
    """
    Lists the VMs on the cloud service

    :param service: The name of the service
    :return: the information in json format
    """
    output = user = request.args.get('format')
    result = cms.vm(service)
    return FORMAT(result, output)


@app.route('/cloudmesh/flavor/<string:service>')
def flavor(service: str) -> list:
    """
    Lists the flavors on the cloud service

    :param service: The name of the service
    :return: the information in json format
    """
    output = user = request.args.get('format')
    result = cms.flavor(service)
    return FORMAT(result, output)

    # return jsonify(result)


@app.route('/cloudmesh/image/<string:service>')
def image(service: str) -> list:
    """
    Lists the images on teh cloud service

    :param service: The name of the service
    :return: the information in json format
    """
    output = user = request.args.get('format')
    result = cms.image(service)
    return FORMAT(result, output)


@app.route('/cloudmesh/boot/<string:service>')
def boot(service: str) -> list:
    """
    Boots a VM on the cloud service

    :param service: The name of the service
    :return: the information in json format
    """
    # TODO: needs more work, read from yaml file defaults
    output = user = request.args.get('format')
    result = cms.boot(service)
    return FORMAT(result, output)


@app.route('/')
def hello_world():
    return 'OK. Cloudmesh service is running.'


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1")
