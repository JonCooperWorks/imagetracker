import unittest2

from library import testing
from models.image import Image
from models.visit import Visit
from models.visitor import Visitor


class TestTrackingHandler(testing.TestCase, unittest2.TestCase):

  DEFAULT_FILENAME = 'file.jpg'
  DEFAULT_CONTENT_TYPE = 'image/jpeg'

  def test_get_tracking_image(self):
    image = Image(
        filename=self.DEFAULT_FILENAME, content_type=self.DEFAULT_CONTENT_TYPE)
    image.put()
    response = self.app.get(
        self.uri_for('tracking_image', filename=image.filename))
    self.assertOk(response)
    self.assertEqual(image.content_type, response.content_type)
    self.assertLength(1, Visit.query())
    self.assertLength(1, Visitor.query())

    visit = Visit.query().get()
    visitor = Visitor.query().get()
    self.assertEqual(image.key, visit.image)
    self.assertEqual(visitor.key, visit.visitor)

  def test_duplicate_visitors_not_made(self):
    image = Image(
        filename=self.DEFAULT_FILENAME, content_type=self.DEFAULT_CONTENT_TYPE)
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

    visit1, visit2 = Visit.query()
    visitor = Visitor.query().get()
    self.assertEqual(visitor.key, visit1.visitor, visit2.visitor)
    self.assertEqual(image.key, visit1.image, visit2.image)
