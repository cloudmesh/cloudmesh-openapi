import base64
import textwrap

from shutil import copyfile

from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.common.Shell import Shell
from cloudmesh.configuration.Config import Config

class BasicAuth:
    """
    This class handles writing the components for basic authentication. 
    It will write to cloudmesh.yaml config file with the user and encoded password

    Each row of .auth_users is username:password formatted. 

    https://swagger.io/docs/specification/2-0/authentication/basic-authentication/
    """
    CONFIG_ATTRIBUTE_AUTH = 'cloudmesh.openapi.authentication'
    CONFIG_VALUE_AUTH = 'basic'
    CONFIG_ATTRIBUTE_USER = 'cloudmesh.openapi.username'
    CONFIG_ATTRIBUTE_PASSWORD = 'cloudmesh.openapi.password'
    HALT_FLAG = '#### basic_auth functionality added'
    USERS_FILE = path_expand('~/.cloudmesh/.auth_users')

    AUTH_FUNC_TEMPLATE = textwrap.dedent("""
    from cloudmesh.openapi.authentication.basic import BasicAuth

    def basic_auth(username, password, required_scopes=None):
        return BasicAuth.basic_auth(username, password)
    
    {halt_flag}
    """)

    @classmethod
    def basic_auth(cls, username, password, required_scopes=None):
        """
        basic_auth function to be listed as x-basicInfoFunc in generated openapi yaml
        """
        config = Config()
        if username == config[cls.CONFIG_ATTRIBUTE_USER]:
            if cls._decode(config[cls.CONFIG_ATTRIBUTE_PASSWORD]) == password:
                if username == 'admin':
                    return {'sub': 'admin', 'scope': 'secret'}
                else:
                    return {'sub': 'user1', 'scope': ''}

        return None

    @classmethod
    def reset_users(cls):
        """
        DEPRECATED
        """
        pass

    @classmethod
    def add_user(cls, user, password):
        config = Config()
        config[cls.CONFIG_ATTRIBUTE_AUTH] = cls.CONFIG_VALUE_AUTH
        config[cls.CONFIG_ATTRIBUTE_USER] = user
        config[cls.CONFIG_ATTRIBUTE_PASSWORD] = cls._encode(password)
        config.save()

    @classmethod
    def _decode(cls, b64text):
        """
        Decode some string with base64 and return the decoded string
        """
        return base64.b64decode(b64text.encode('ascii')).decode('ascii')
        
    @classmethod
    def _encode(cls, text):
        """
        Encode some string with base64 and return the string representation
        """
        return base64.b64encode(text.encode('ascii')).decode('ascii')

    @classmethod
    def write_basic_auth(cls, filename, module_name):
        """
        Writes the basic auth configuration to a new python file and returns the new module name
        and new filename
        """
        basic_auth_enabled = False
        for line in open(filename):
            if cls.HALT_FLAG in line:
                basic_auth_enabled = True
                break

        if not basic_auth_enabled:
            filename_auth = filename[:-len('.py')] + '_basic_auth_enabled.py'
            copyfile(filename, filename_auth)
            Console.info(f'copied {filename} to {filename_auth}')
            filename = filename_auth
            module_name = module_name + '_basic_auth_enabled'
            with open(filename, 'a') as f:
                f.write('\n')
                f.write(cls.AUTH_FUNC_TEMPLATE.format(halt_flag=cls.HALT_FLAG))
                f.close()
            Console.info(f'added basic auth functionality to {filename}')

        return module_name, filename
