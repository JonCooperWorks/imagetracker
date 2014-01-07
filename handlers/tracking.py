import logging

from google.appengine.api import taskqueue

from handlers.base import BaseHandler
from models.image import Image
from models.visit import Visit
from models.visitor import Visitor


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
    collecting progressively more data.

    Whenever an image is served, a task is dispatched to send the visit data to
    keen.io for analysis, and to update our metrics in real time."""

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
            visitor = Visitor()
            visitor.put()

        visit = Visit(identifier=identifier, ip_address=ip_address,
                      user_agent=user_agent, referrer=referrer,
                      image=image.key, visitor=visitor.key)
        visit.put()

        # Dispatch a task to send the visit to keen.io for analysis.
        visit_key = visit.key.urlsafe()
        logging.info('Dispatching task to process {visit_key}'
        .format(visit_key=visit_key))
        taskqueue.add(url=self.uri_for('analytics'),
                      params={'visit_key': visit_key})

        self.response.content_type = str(image.content_type)
        self.response.set_cookie(key='VISITOR_UUID', value=visitor.uuid)
        self.response.out.write(image.data)
