import sys
from os.path import join
from .common import APP_ROOT

# Allows importing apps into INSTALLED_APPS without using written.apps.app_name
sys.path.append(APP_ROOT)
sys.path.append(join(APP_ROOT, 'apps'))
