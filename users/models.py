from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''
    If you’re starting a new project, it’s highly recommended to set up a custom user model, even if the default User model is sufficient for you.
    This model behaves identically to the default user model, but you’ll be able to customize it in the future if the need arises.
    See: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

    Configure users.User to be the model used for the auth application by adding AUTH_USER_MODEL to settings.py:
    AUTH_USER_MODEL='users.User'
    '''
    pass