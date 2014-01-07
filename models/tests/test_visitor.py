import datetime

import unittest2

from library import testing
from models.visitor import Visitor


class TestVisitor(testing.TestCase, unittest2.TestCase):
    def test_defaults(self):
        visitor = Visitor()
        self.assertIsNone(visitor.uuid)
        self.assertAlmostEqual(datetime.datetime.now(), visitor.timestamp,
                               delta=datetime.timedelta(seconds=5))

    def test_put(self):
        visitor = Visitor()
        visitor.put()
        self.assertIsNotNone(visitor.uuid)

    def test_get_by_uuid(self):
        visitor = Visitor()
        visitor.put()
        self.assertIsNotNone(Visitor.get_by_uuid(visitor.uuid))
        self.assertIsNone(Visitor.get_by_uuid(''))
