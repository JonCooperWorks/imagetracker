from google.appengine.api import memcache
from webapp2_extras import jinja2, sessions
import webapp2


class BaseHandler(webapp2.RequestHandler):
    """Base class for all RequestHandlers."""

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def dispatch(self):
        """Override dispatch to initialize and persist session data."""
        self.session_store = sessions.get_store(request=self.request)

        try:
            super(BaseHandler, self).dispatch()
        finally:
            self.session_store.save_sessions(self.response)

    def render_template(self, template, context=None):
        """Renders the template with the provided context (optional)."""
        context = context or {}

        extra_context = {
            'request': self.request,
            'uri_for': self.uri_for,
            'session': self.session}

        # Only override extra context stuff if it's not set by the template:
        for key, value in extra_context.items():
            if key not in context:
                context[key] = value

        return self.jinja2.render_template(template, **context)

    def render_to_response(self, template, context=None, use_cache=False):
        """Renders the template and writes the result to the response."""

        if use_cache:
            # Use the request's path to store the contents.

            # WARNING: This could cause scary problems if you render
            # user-specific pages.
            # DO NOT use current_profile in a template rendered with use_cache=True.
            cache_key = self.request.path
            contents = memcache.get(cache_key)

            if not contents or 'flushcache' in self.request.arguments():
                contents = self.render_template(template, context)

                # If add() returns False, it means another request is already trying
                # to cache the page. No need to do anything here.
                if memcache.add('lock.%s' % cache_key, True):
                    memcache.set(cache_key, contents)
                    memcache.delete('lock.%s' % cache_key)

        else:
            contents = self.render_template(template, context)

        self.response.write(contents)

    def is_taskqueue_request(self):
        return self.request.headers.get('X-AppEngine-QueueName') is not None
