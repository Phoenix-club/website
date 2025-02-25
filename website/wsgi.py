"""
WSGI config for website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import os
import sys

# Add your project directory to the system path
sys.path.append('/home/phoenixkkw/website')  # Change to your actual project folder

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

# Activate the virtual environment (named 'env')
activate_this = '/home/phoenixkkw/env/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

# Get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

