ZIP_LIBRARIES = [
    'library/pyhaml_jinja.zip', 'library/keen.zip',
    'library/requests.zip', 'library/'
]


# Zipimport configuration:
def configure_libraries():
  import sys

  sys.path.extend(ZIP_LIBRARIES)

  # Ensure no duplicates in the PYTHONPATH.
  sys.path = list(set(sys.path))

configure_libraries()

import os

import webapp2
from webapp2_extras.routes import RedirectRoute

from handlers.dashboard import DashboardHandler
from handlers.static import StaticHandler
from handlers.tracking import TrackingHandler


DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')


_routes = [
    ('tracking_image', 'GET', '/images/<filename:.*>', TrackingHandler,
        'get'),
    ('dashboard.images', None, '/dashboard/images', DashboardHandler,
        'images'),
    ('home', 'GET', '/', StaticHandler('home.haml'), 'get'),
]


routes = []

for name, methods, pattern, handler_cls, handler_method in _routes:
  # Allow a single string, but this has to be changed to a list.
  if isinstance(methods, basestring):
    methods = [methods]

  # Create the route.
  route = RedirectRoute(name=name, template=pattern, methods=methods,
                        handler=handler_cls, handler_method=handler_method,
                        strict_slash=True)

  # Add the route to the proper public list.
  routes.append(route)

webapp2_config = {
    'webapp2_extras.sessions': {
        'secret_key': 'GXpg0WIa+:$;`diU5[:^7~XOL#z0t;2}CD$dTjG6bDydmuT!gu=gz1',
    },
    'webapp2_extras.jinja2': {
        'environment_args': {
            'autoescape': True,
            'extensions': [
                'pyhaml_jinja.HamlExtension',
            ],
        },
    },
}


app = webapp2.WSGIApplication(routes=routes, debug=DEBUG,
                              config=webapp2_config)
