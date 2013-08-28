import webapp2

from models import Visit


class BaseHandler(webapp2.RequestHandler):
  """Base class for all RequestHandlers."""


class TrackingHandler(BaseHandler):
  """Serves the tracking image.

  This handler serves an image, and logs any viewers' IP addresses and an
  identifier with which to monitor them.
  This can be used for tracking people across websites by posting an image to
  the comments section, or checking when people open emails by putting the
  image in the email body."""

  def get(self):
    identifier = self.request.get('identifier', '')
    ip_address = self.request.remote_addr
    user_agent = self.request.headers['User-Agent']
    visit = Visit(identifier=identifier, ip_address=ip_address,
                  user_agent=user_agent)
    visit.put()

    self.response.out.write('hi')
