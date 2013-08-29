import logging

from google.appengine.api import urlfetch, users

from handlers.base import BaseHandler
from models.image import Image


class ImageHandler(BaseHandler):
  """Allows a user to create a tracking image and view it's statistics.

  This handler is responsible for displaying a form allowing a user to enter
  an image from the internet, then downloading and storing it in the datastore
  as a `ndb.BlobProperty`.
  It also provides the ability for a user to view all information of visitors
  to their image."""

  def get(self):
    return self.render_to_response('form.haml')

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
      response = urlfetch.fetch(image_source)

    # TODO: Handle the error case of image not being there and display this
    # to the user.
    except urlfetch.DownloadError as e:
      logging.exception(e.message)
      return

    # Store the image in the datastore and ensure the write is fully applied
    # before redirecting.
    image_data = response.content
    content_type = response.headers.get('Content-Type', '')
    image = Image(data=image_data, filename=filename, user=user,
                  content_type=content_type)
    image.put().get()

    # TODO: Redirect to somewhere useful.
    return self.redirect_to('tracking_image', filename=filename)
