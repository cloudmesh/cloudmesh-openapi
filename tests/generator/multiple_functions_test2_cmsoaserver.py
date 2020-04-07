
import connexion

# Create the application instance
app = connexion.App(__name__, specification_dir='/Users/Jonathan/cm/cloudmesh-openapi/tests/generator')

# Read the yaml file to configure the endpoints
app.add_api('/Users/Jonathan/cm/cloudmesh-openapi/tests/generator/multiple_functions_test2.yaml')

if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port=8080,
            debug=False,
            server='flask')
