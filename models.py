from google.appengine.ext import ndb


class Visit(ndb.Model):
  """Stores tracking information from a visitor.

  This is to be used to log a visit to the page, as well as associated
  metadata, such as the visitor's IP address, email address and the time of
  the visit."""

  ip_address = ndb.StringProperty()
  email = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def get_by_email(cls, email):
    return cls.query().filter(cls.email == email)

  @classmethod
  def get_by_ip_address(cls, ip_address):
    return cls.query().filter(cls.ip_address == ip_address)
