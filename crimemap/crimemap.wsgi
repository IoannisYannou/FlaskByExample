activate_this = '/var/www/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, "/var/www/FlaskByExample/crimemap")
from crimemap import app as application
