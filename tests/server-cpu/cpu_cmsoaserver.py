
import connexion

# Create the application instance
app = connexion.App(__name__, specification_dir='/Users/Jonathan/cm/cloudmesh-openapi/tests/server-cpu')

# Read the yaml file to configure the endpoints
app.add_api('/Users/Jonathan/cm/cloudmesh-openapi/tests/server-cpu/cpu.yaml')

if __name__ == '__main__':
    app.run(host='None',
            port=8080,
            debug=False,
            server='flask')
