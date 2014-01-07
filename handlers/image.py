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
        images = Image.get_by_user(users.get_current_user())
        return self.render_to_response('images.haml', {'images': images})

    def post(self):
        error = None
        user = users.get_current_user()

        if not user:
            return self.abort(404)

        filename = self.request.POST.get('filename', '')
        image_source = self.request.POST.get('image_source', '')

        if Image.get_by_filename(filename):
            error = ('File with filename {filename} already exists.'
                     .format(filename=filename))
            logging.error(error)

        try:
            response = urlfetch.fetch(image_source)

        except urlfetch.DownloadError as e:
            error = ('Failed to download file \'{filename}\''
                     .format(filename=filename))
            logging.exception(e.message)

        if response.status_code == 404:
            error = '{filename} not found.'.format(filename=filename)

        if error is not None:
            self.session.add_flash(value=error, level='error')
            return self.render_to_response('images.haml')

        # Store the image in the datastore and ensure the write is fully applied
        # before redirecting.
        image_data = response.content
        content_type = response.headers.get('Content-Type', '')
        image = Image(data=image_data, filename=filename, user=user,
                      content_type=content_type)
        image.put().get()

        return self.redirect_to('image')
