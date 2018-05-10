"""
WSGI config for mysite_MYSQL project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import os
import site
import sys

from django.core.wsgi import get_wsgi_application


# Add the site-packages of the chosen virtualenv to work with
# site.addsitedir() will let you use the site packages and dependencies within the
# virtualenv you created initially for your specific project with your specific packages


# FIXME: This is obviously not right!!
site.addsitedir("/home/christian/.virtualenvs/py3/lib/python3.4/site-packages")

# Add the app's directory to the PYTHONPATH
# sys.path.append() adds your project's directory to the Python path
# It is advised you add both the main directory holding your apps and
# its child that contains the settings.py file which in this case is "myproject".

sys.path.append('/D/myfiles/2016/django/mysite_MYSQL')
sys.path.append('/D/myfiles/2016/django/mysite_MYSQL/mysite_MYSQL')
# wird nicht gebraucht wie es scheint:
sys.path.append('/D/myfiles/2016/django/mysite_MYSQL/ZSIV')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite_MYSQL.settings")
# bei mehreren Projekten:
# siehe https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/modwsgi/
# os.environ["DJANGO_SETTINGS_MODULE"] = "{{ project_name }}.settings"

# Activate your virtual env
activate_env = os.path.expanduser("~/.virtualenvs/py3/bin/activate_this.py")
# execfile(activate_env, dict(__file__=activate_env))
# python 3 replacement, see http://stackoverflow.com/questions/436198/what-is-an-alternative-to-execfile-in-python-3-0
with open(activate_env) as f:
    code = compile(f.read(), activate_env, 'exec')
    exec(code, dict(__file__=activate_env))

application = get_wsgi_application()
