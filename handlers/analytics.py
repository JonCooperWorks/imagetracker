import datetime
import logging
import time

from google.appengine.api import users
from google.appengine.ext import ndb
import keen

from config import DEBUG
from handlers import base
from models.visit import Visit


class AnalyticsHandler(base.BaseHandler):
  """Send all data to keen.io for analysis.

  This handler is responsible for exporting the data received from our visitors
  to keen.io for further processing (Charts, graphs, etc.).
  It can either be run as an hourly cron task (AnalyticsHandler.get) or from
  the task queue (AnalyticsHandler.post)."""

  def get(self):
    current_time = datetime.datetime.utcnow()
    one_hour_ago = current_time - datetime.timedelta(hours=1)
    visits = [serialize_ndb_model(visit)
              for visit in Visit.query(Visit.timestamp >= one_hour_ago)]
    if visits:
      keen.add_events({
          'visits': visits,
      })

  def post(self):
    if not self.is_taskqueue_request():
      logging.error('Request outside of task queue.')
      return

    visit_key = self.request.POST.get('visit_key', '')
    visit = ndb.Key(urlsafe=visit_key).get()

    if not visit:
      logging.error('Invalid visit key passed: {visit_key}'
                    .format(visit_key=visit_key))
      return

    # Shoot the event off to keen.
    logging.info('Successfully sent {visit_key} to keen.io'
                 .format(visit_key=visit_key))

    # Don't send data from development app server.
    if not DEBUG:
      keen.add_event('visits', serialize_ndb_model(visit))


def serialize_ndb_model(model):
  """Adapt the entities returned by the query to be sent to keen.io."""

  model_dict = model.to_dict()
  for k, v in model_dict.iteritems():
    # Follow `ndb.KeyProperty`s to expand the models.
    if isinstance(v, ndb.key.Key):
      model_dict[k] = serialize_ndb_model(v.get())

    # Convert all dates to UTC and represent as unix time.
    elif isinstance(v, datetime.datetime):
      model_dict[k] = int(time.mktime(v.timetuple()))

    # Simply stringify `UserProperty`s
    elif isinstance(v, users.User):
      model_dict[k] = str(v)

    # Don't send any blobs to keen.io
    elif isinstance(v, bytes):
      model_dict[k] = None

  return model_dict
