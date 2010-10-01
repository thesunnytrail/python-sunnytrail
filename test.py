#!/usr/bin/env python

import mox
import unittest
import sunnytrail

class EventTest(unittest.TestCase):

  def test_create_signup_event(self):
    e = sunnytrail.SignupEvent()

class ApiTestCase(unittest.TestCase):
  def setUp(self):
    self.mox = mox.Mox()

  def tearDown(self):
    self.mox.UnsetStubs()

class SunnyTrailTest(ApiTestCase):
  pass

if __name__ == '__main__':
  unittest.main()

