import uuid

from google.appengine.ext import ndb


class Visitor(ndb.Model):
    """Stores a record of each visitor.

    Each visitor simply has a UUID that we use to set a cookie to track them
    across websites."""

    uuid = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

    def put(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())

        return super(Visitor, self).put(*args, **kwargs)

    @classmethod
    def get_by_uuid(cls, uuid):
        return cls.query().filter(cls.uuid == uuid).get()
