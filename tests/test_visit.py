import datetime
import unittest2

from library import testing
from models import Visit


class TestVisitModel(testing.TestCase, unittest2.TestCase):

  DEFAULT_IDENTIFIER = 'test@example.com'
  DEFAULT_IP = '192.168.1.1'

  def test_defaults(self):
    visit = Visit()
    visit.put()
    self.assertIsNone(visit.ip_address)
    self.assertIsNone(visit.identifier)
    self.assertIsNone(visit.user)
    self.assertIsNone(visit.image)
    self.assertIsNone(visit.referrer)
    self.assertIsNone(visit.user_agent)
    self.assertAlmostEqual(datetime.datetime.now(), visit.time,
                           delta=datetime.timedelta(seconds=5))

  def test_get_by_identifier(self):
    visit = Visit(identifier=self.DEFAULT_IDENTIFIER)
    visit.put()
    self.assertLength(1, Visit.get_by_identifier(self.DEFAULT_IDENTIFIER))
    self.assertLength(0, Visit.get_by_identifier('not@registered.com'))

  def test_get_by_ip_address(self):
    visit = Visit(ip_address=self.DEFAULT_IP)
    visit.put()
    self.assertLength(1, Visit.get_by_ip_address(self.DEFAULT_IP))
    self.assertLength(0, Visit.get_by_ip_address('1.1.1.1'))
