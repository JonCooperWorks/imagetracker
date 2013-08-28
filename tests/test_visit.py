import datetime
import unittest2

from library import testing
from models import Visit


class TestVisitModel(testing.TestCase, unittest2.TestCase):

  DEFAULT_EMAIL = 'test@example.com'
  DEFAULT_IP = '192.168.1.1'

  def test_defaults(self):
    visit = Visit()
    visit.put()
    self.assertIsNone(visit.ip_address)
    self.assertIsNone(visit.email)
    self.assertAlmostEqual(datetime.datetime.now(), visit.time,
                           delta=datetime.timedelta(seconds=5))

  def test_get_by_email(self):
    visit = Visit(email=self.DEFAULT_EMAIL)
    visit.put()
    self.assertLength(1, Visit.get_by_email(self.DEFAULT_EMAIL))
    self.assertLength(0, Visit.get_by_email('not@registered.com'))

  def test_get_by_ip_address(self):
    visit = Visit(ip_address=self.DEFAULT_IP)
    visit.put()
    self.assertLength(1, Visit.get_by_ip_address(self.DEFAULT_IP))
    self.assertLength(0, Visit.get_by_ip_address('1.1.1.1'))
