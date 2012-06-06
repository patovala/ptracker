import os
import sys
sys.stdout = sys.stderr
# Add the virtual Python environment site-packages directory to the path
import site
site.addsitedir('/home/ptrack/env2.6/lib/python2.6/site-packages')
sys.path.append('/home/ptrack/ptrack/')

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages
os.environ['PYTHON_EGG_CACHE'] = '/home/ptrack/ptrack/egg-cache'

#If your project is not on your PYTHONPATH by default you can add the following
sys.path.append('/home/ptrack/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

