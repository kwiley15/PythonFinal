"""
ASGI config for netflixsite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os # import os to interact with enviroment variables 

from django.core.asgi import get_asgi_application # Import ASGI application handler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netflixsite.settings') # settings module for the netflixsite project, which settings.py to use 

application = get_asgi_application() # create the application 

#we are not using this page 