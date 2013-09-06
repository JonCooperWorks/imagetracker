import datetime

import unittest2

from library import testing
from models.image import Image
from models.visit import Visit


class TestImage(testing.TestCase, unittest2.TestCase):

  DEFAULT_FILENAME = 'test.jpg'

  def test_defaults(self):
    image = Image()
    image.put()
    self.assertIsNone(image.data)
    self.assertIsNone(image.filename)
    self.assertIsNone(image.user)
    self.assertIsNone(image.content_type)
    self.assertAlmostEqual(datetime.datetime.now(), image.created,
                           delta=datetime.timedelta(seconds=5))

  def test_get_by_filename(self):
    image = Image(filename=self.DEFAULT_FILENAME)
    image.put()
    self.assertEqual(image.key, Image.get_by_filename(image.filename).key)
    self.assertIsNone(Image.get_by_filename('not.jpg'))

  def test_get_visits(self):
    image = Image()
    image.put()
    visit_key = Visit(image=image.key).put()
    self.assertLength(1, image.get_visits())
    self.assertEqual(visit_key, image.get_visits().get().key)
