import textwrap

from shutil import copyfile

from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.common.Shell import Shell

# Basic auth
# https://swagger.io/docs/specification/2-0/authentication/basic-authentication/


class BasicAuth:
    """
    This class handles writing the components for basic authentication. 
    This class writes a file to ~/.cloudmesh/.auth_users

    Each row of .auth_users is username:password formatted. 
    """
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
        # Scan ~/.cloudmesh/.auth_users for username and password
        users = {}
        with open(cls.USERS_FILE, 'r') as f:
            for row in f:
                user, passwd = row.strip().split(':')
                users[user] = passwd
        if username in users:
            if users[username] == password:
                if username == 'admin':
                    return {'sub': 'admin', 'scope': 'secret'}
                else:
                    return {'sub': 'user1', 'scope': ''}

        return None

    @classmethod
    def reset_users(cls):
        open(cls.USERS_FILE, 'w').close()

    @classmethod
    def add_user(cls, user, password):
        with open(cls.USERS_FILE, 'a') as f:
            f.write(f'{user}:{password}\n')
            f.close()

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
