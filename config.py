import os

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
