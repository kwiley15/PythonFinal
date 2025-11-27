#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    #sets the default django settings module for the program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netflixsite.settings')
    try:
        #import django commadn line function 
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django is not installed, raise an error
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)# excutes the command line 


#this runs the main function when the script is executed directly.
if __name__ == '__main__':
    main()
