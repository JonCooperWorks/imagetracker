import logging

from google.appengine.api import memcache, urlfetch, users
from webapp2_extras import jinja2
import webapp2

from models import Image, Visit, Visitor


class BaseHandler(webapp2.RequestHandler):
  """Base class for all RequestHandlers."""

  @webapp2.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def render_template(self, template, context=None):
    """Renders the template with the provided context (optional)."""
    context = context or {}

    extra_context = {
        'request': self.request,
        'uri_for': self.uri_for}

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


class TrackingHandler(BaseHandler):
  """Serves the tracking image.

  This handler serves an image, and logs any viewers' IP addresses and an
  identifier with which to monitor them.
  This can be used for tracking people across websites by posting an image to
  the comments section, or checking when people open emails by putting the
  image in the email body.

  We set a cookie with a UUID on each request and associate it with a
  Visitor object.
  We can use the UUID stored in each cookie to differentiate between each
  visitor, allowing us to monitor which websites each person visits, and
  and maintain a list of IP addresses they use.
  We can eventually figure out their identity from this information, by
  collecting progressively more data."""

  def get(self, filename):
    image = Image.get_by_filename(filename)
    if not image:
      return self.abort(404)

    # Gather the information we take from the user.
    identifier = self.request.get('identifier', '')
    ip_address = self.request.remote_addr
    referrer = self.request.referrer
    user_agent = self.request.headers.get('User-Agent', '')
    visitor_uuid = self.request.cookies.get('VISITOR_UUID', '')

    # If they're not in our database, create a new entity to track them.
    visitor = Visitor.get_by_uuid(visitor_uuid)
    if visitor is None:
      visitor = Visitor().put()

    visit = Visit(identifier=identifier, ip_address=ip_address,
                  user_agent=user_agent, referrer=referrer,
                  image=image.key, visitor=visitor.key)
    visit.put()

    self.response.content_type = 'image/jpeg'
    self.response.set_cookie(key='VISITOR_UUID', value=visitor.uuid)
    self.response.out.write(image.data)


class ImageHandler(BaseHandler):
  """Allows a user to create a tracking image and view it's statistics.

  This handler is responsible for displaying a form allowing a user to enter
  an image from the internet, then downloading and storing it in the datastore
  as a `ndb.BlobProperty`.
  It also provides the ability for a user to view all information of visitors
  to their image."""

  def get(self):
    return self.render_to_response('form.html')

  def post(self):
    user = users.get_current_user()

    if not user:
      return self.abort(404)

    filename = self.request.POST.get('filename', '')
    image_source = self.request.POST.get('image_source', '')

    # TODO: Handle the error of a filename being present and display the error.
    if Image.get_by_filename(filename):
      logging.error('File with filename {filename} already exists.'
                    .format(filename=filename))
      return

    try:
      image_data = urlfetch.fetch(image_source).content

    # TODO: Handle the error case of image not being there and display this
    # to the user.
    except urlfetch.DownloadError as e:
      logging.exception(e.message)
      return

    image = Image(data=image_data, filename=filename,
                  user=user)
    image.put()

    # TODO: Redirect to somewhere useful.
    return self.redirect_to('tracking_image', filename=image.filename)
