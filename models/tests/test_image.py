import unittest2

from library import testing
from models.image import Image


class TestImage(testing.TestCase, unittest2.TestCase):

  DEFAULT_FILENAME = 'test.jpg'

  def test_defaults(self):
    image = Image()
    self.assertIsNone(image.data)
    self.assertIsNone(image.filename)
    self.assertIsNone(image.user)
    self.assertIsNone(image.content_type)

  def test_get_by_filename(self):
    image = Image(filename=self.DEFAULT_FILENAME)
    image.put()
    self.assertEqual(image.key, Image.get_by_filename(image.filename).key)
    self.assertIsNone(Image.get_by_filename('not.jpg'))
