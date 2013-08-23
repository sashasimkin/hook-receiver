"""
WSGI config for project.
"""
import os
import sys
import app


sys.path.insert(0, app.PATH)

activate_this = os.path.join(app.PATH, '.env/bin/activate_this.py')

if os.path.exists(activate_this):
    execfile(activate_this, dict(__file__=activate_this))