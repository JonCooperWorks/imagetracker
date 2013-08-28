import os

import webapp2


DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')


webapp2_config = {
    'webapp2_extras.sessions': {
        'secret_key': 'vpgd[HGn|:|kKa:bUKO,rsR.=euk>;cEL--TV$?2sdmlVo0IK/Uiq['
    },
    'webapp2_extras.jinja2': {
        'environment_args': {
            'autoescape': True,
            'extensions': [
                'jinja2.ext.i18n',
                'pyhaml_jinja.HamlExtension',
            ],
        },
    },
}

app = webapp2.WSGIApplication(debug=DEBUG,
                              config=webapp2_config)
