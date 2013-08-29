# Zipimport configuration:
def configure_libraries():
  import sys

  ZIP_LIBRARIES = ['library/pyhaml_jinja.zip', 'library/']
  sys.path.extend(ZIP_LIBRARIES)

  # Ensure no duplicates in the PYTHONPATH.
  sys.path = list(set(sys.path))

configure_libraries()

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
