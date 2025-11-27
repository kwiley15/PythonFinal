"""
WSGI config for netflixsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os # import os to interact with enviroment variables 

from django.core.wsgi import get_wsgi_application # import WSGI application handler 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netflixsite.settings') # set the default settings for module , which settings.py to use 

application = get_wsgi_application() # create the application 

#we are not using this page 