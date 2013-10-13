import datetime
import time

from google.appengine.api import users
from google.appengine.ext import ndb
import keen

from handlers import base
from models.visit import Visit
from models.visitor import Visitor


class AnalyticsHandler(base.BaseHandler):
  """Send all data to keen.io for analysis.

  This handler is responsible for exporting the data received from our visitors
  to keen.io for further processing (Charts, graphs, etc.).
  It should be run as a scheduled task every hour, meaning the data at keen.io
  will be at most one hour old."""

  def get(self):
    current_time = datetime.datetime.utcnow()
    one_hour_ago = current_time - datetime.timedelta(hours=1)
    visits = [serialize_ndb_model(visit)
              for visit in Visit.query(Visit.timestamp >= one_hour_ago)]
    visitors = [serialize_ndb_model(visitor)
                for visitor in Visitor.query(
                    Visitor.timestamp >= one_hour_ago)]
    if visits:
      keen.add_events({
          'visits': visits,
          'visitors': visitors,
      })


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
