import uuid

from google.appengine.ext import ndb


class Visit(ndb.Model):
  """Stores tracking information from a visitor.

  This is to be used to log a visit to the page, as well as associated
  metadata.
  Currently, we only log a visitor's IP address, User-Agent, referrer,
  and the time of the visit.

  The nature of the identifier depends on the context in which we're tracking
  user, but should be something meaningful.
  For example, if we want to see when someone read an email, we can use their
  email address as the identifier, or to secretly monitor a website's traffic,
  we can set the website's URL as the identifier."""

  # Visitor data.
  ip_address = ndb.StringProperty()
  user_agent = ndb.StringProperty()
  referrer = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)
  visitor = ndb.KeyProperty()

  # Administrative data.
  image = ndb.KeyProperty(kind='Image')
  identifier = ndb.StringProperty()

  @classmethod
  def get_by_identifier(cls, email):
    return cls.query().filter(cls.identifier == email)

  @classmethod
  def get_by_ip_address(cls, ip_address):
    return cls.query().filter(cls.ip_address == ip_address)


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


class Visitor(ndb.Model):
  """Stores a record of each visitor.

  Each visitor simply has a UUID that we use to set a cookie to track them
  across websites."""

  uuid = ndb.StringProperty()

  def put(self, *args, **kwargs):
    if not self.uuid:
      self.uuid = str(uuid.uuid4())

    return super(Visitor, self).put(*args, **kwargs)

  @classmethod
  def get_by_uuid(cls, uuid):
    return cls.query().filter(cls.uuid == uuid).get()
