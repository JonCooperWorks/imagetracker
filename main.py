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

import webapp2
from webapp2_extras.routes import RedirectRoute

from config import DEBUG
from handlers.analytics import AnalyticsHandler
from handlers.image import ImageHandler
from handlers.logout import LogoutHandler
from handlers.static import StaticHandler
from handlers.tracking import TrackingHandler


_routes = [
    ('/images/<filename:.*>', TrackingHandler, 'tracking_image'),
    ('/dashboard/images', ImageHandler, 'image'),
    ('/dashboard/metrics', StaticHandler('metrics.haml', use_cache=False),
        'metrics'),
    ('/analytics', AnalyticsHandler, 'analytics'),
    ('/logout', LogoutHandler, 'logout'),
    ('/', StaticHandler('home.haml'), 'home'),
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
