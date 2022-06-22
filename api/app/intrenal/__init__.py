import os
from .auth import Auth


auth_instance = Auth(os.environ["SECRET_KEY"], token_url='/users/login')
