#!/usr/bin/env python

import mox
import unittest
import sunnytrail

class PlanTest(unittest.TestCase):
  def test_create_plan(self):
    p = sunnytrail.Plan('plan-name', 10, 30)

    self.assertEqual(p.name, 'plan-name')
    self.assertEqual(p.price, 10)
    self.assertEqual(p.recurring, 30)

  def test_by_default_a_plan_is_not_recurring(self):
    p = sunnytrail.Plan('test', 10)
    assert not p.is_recurring

  def test_convert_a_not_recurring_plan_to_a_hash(self):
    p = sunnytrail.Plan('dummy', 10)
    assert self.all_keys_in(p.to_hash(), 'name', 'price')

  def test_convert_recurring_plan_to_hash(self):
    p = sunnytrail.Plan('dummy', 10, 20)
    assert self.all_keys_in(p.to_hash(), 'name', 'price', 'recurring')

  def all_keys_in(self, h, *keys):
    return all(map(lambda k: k in h, keys))

class ActionTest(unittest.TestCase):
  pass

class ApiTestCase(unittest.TestCase):
  def setUp(self):
    self.mox = mox.Mox()

  def tearDown(self):
    self.mox.UnsetStubs()

class SunnyTrailTest(ApiTestCase):
  pass

if __name__ == '__main__':
  unittest.main()

