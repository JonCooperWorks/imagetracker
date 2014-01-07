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
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
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
