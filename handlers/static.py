from handlers.base import BaseHandler


def StaticHandler(template, use_cache=True):
    """Generates a handler that can render the specified template."""

    class Handler(BaseHandler):
        def get(self):
            return self.render_to_response(template, use_cache=use_cache)

    return Handler
