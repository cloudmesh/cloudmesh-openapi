
import connexion

# Create the application instance
app = connexion.App(__name__, specification_dir='/Users/Jonathan/cm/cloudmesh-openapi/tests/server-cms')

# Read the yaml file to configure the endpoints
app.add_api('/Users/Jonathan/cm/cloudmesh-openapi/tests/server-cms/cms.yaml')

if __name__ == '__main__':
    app.run(host='127.0.0.2',
            port=8080,
            debug=False,
            server='flask')
