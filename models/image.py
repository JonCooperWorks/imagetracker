from google.appengine.ext import ndb


class Image(ndb.Model):
  """Stores tracking images to be served to visitors.

  Each Image consists of the image data, stored as a Blob, and a filename
  associated with the image.
  Every filename must be unique, to allow lookups by filename to retrieve the
  correct image."""

  # Image data.
  data = ndb.BlobProperty()
  filename = ndb.StringProperty()
  user = ndb.UserProperty()

  @classmethod
  def get_by_filename(cls, filename):
    return cls.query().filter(cls.filename == filename).get()
