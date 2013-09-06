from google.appengine.ext import ndb

from models.visit import Visit


class Image(ndb.Model):
  """Stores tracking images to be served to visitors.

  Each Image consists of the image data, stored as a Blob, and a filename
  associated with the image.
  Every filename must be unique, to allow lookups by filename to retrieve the
  correct image."""

  # Image data.
  content_type = ndb.StringProperty()
  data = ndb.BlobProperty()
  filename = ndb.StringProperty()
  user = ndb.UserProperty()

  # Administrative data.
  created = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def get_by_filename(cls, filename):
    return cls.query().filter(cls.filename == filename).get()

  @classmethod
  def get_by_user(cls, user):
    return cls.query().filter(cls.user == user).order(-cls.created)

  def get_visits(self):
    return Visit.query().filter(Visit.image == self.key)
