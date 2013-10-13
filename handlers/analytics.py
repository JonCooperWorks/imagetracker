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
