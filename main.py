import os

import webapp2
from webapp2_extras.routes import RedirectRoute

from handlers.image import ImageHandler
from handlers.tracking import TrackingHandler


DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')


_routes = [
    ('/images/<filename:.*>', TrackingHandler, 'tracking_image'),
    ('/add_image', ImageHandler, 'image'),
]

routes = []
for pattern, handler, name in _routes:
  route = RedirectRoute(name=name, template=pattern, handler=handler,
                        strict_slash=True)
  routes.append(route)


app = webapp2.WSGIApplication(routes=routes, debug=DEBUG)
