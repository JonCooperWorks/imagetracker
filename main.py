import os

import webapp2

from handlers import TrackingHandler


DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')


routes = [
    (r'/test/', TrackingHandler),
]
app = webapp2.WSGIApplication(routes, debug=DEBUG)
