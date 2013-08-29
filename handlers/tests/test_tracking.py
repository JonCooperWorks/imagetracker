import unittest2

from library import testing
from models.image import Image
from models.visit import Visit
from models.visitor import Visitor


class TestTrackingHandler(testing.TestCase, unittest2.TestCase):

  DEFAULT_FILENAME = 'file.jpg'

  def test_get_tracking_image(self):
    image = Image(filename=self.DEFAULT_FILENAME)
    image.put()
    response = self.app.get(
        self.uri_for('tracking_image', filename=image.filename))
    self.assertOk(response)
    self.assertLength(1, Visit.query())
    self.assertLength(1, Visitor.query())

  def test_duplicate_cookies_not_made(self):
    image = Image(filename=self.DEFAULT_FILENAME)
    image.put()
    response = self.app.get(
        self.uri_for('tracking_image', filename=image.filename))
    self.assertOk(response)
    self.assertLength(1, Visit.query())
    self.assertLength(1, Visitor.query())
    response = self.app.get(
        self.uri_for('tracking_image', filename=image.filename))
    self.assertOk(response)
    self.assertLength(2, Visit.query())
    self.assertLength(1, Visitor.query())
