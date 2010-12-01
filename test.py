#!/usr/bin/env python

import sys, os, signal
import unittest
import sunnytrail
import simplejson
import socket
import subprocess
import _urllib as urllib

from time import time, sleep

try:
  all
except:
  def all(seq):
    for el in seq:
      if not el: return False
    return True

try:
  from urlparse import parse_qs # python 2.6 and newer
except ImportError:
  from cgi import parse_qs # python 2.5 

def get_unused_port():
  """ Vulnerable to race conditions but good enough for now"""
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('localhost', 0))
  addr, port = s.getsockname()
  s.close()
  return port

def wait_for_port(host, port):
  s = socket.socket()
  while True:
    try:
      s.connect((host, port))
      s.close()
      return

    except socket.error:
      sleep(0.1)

class FunctionalTest(unittest.TestCase):    
  def setUp(self):
    self.process = None
  
  def tearDown(self):
    if self.process:
      os.kill(self.process.pid, signal.SIGTERM)
      self.process.wait()
      self.process = None

  def serve(self, code, content = ''):
    port = get_unused_port()
    self.process = subprocess.Popen([
        'python', 'http_serve.py',
        '--port', str(port),
        '--code', str(code),
        '--content', str(content),
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    wait_for_port('localhost', port)
    return 'localhost:%d' % port

  def test_error(self):
    hostport = self.serve(202)
    
    client = sunnytrail.Sunnytrail('key', hostport, use_ssl = False)
    client.send(sunnytrail.CancelEvent('id', 'name', 'email'))

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
  def test_create_action(self):
    now = int(time())
    p = sunnytrail.Action('signup')

    assert 'name' in p.to_hash()
    assert 'created' in p.to_hash()

    self.assertEquals(p.name, 'signup')
    self.assertTrue(p.created >= now)

  def test_create_action_with_invalid_name(self):
    self.assertRaises(ValueError, sunnytrail.Action, 'dummy-name')

class EventTest(unittest.TestCase):
  def test_create_free_signup_event(self):
    actual = sunnytrail.SignupEvent('id', 'name', \
      'email', sunnytrail.Plan('plan'), 123).to_json()

    expected = '{"action": {"name": "signup", "created": 123}, '\
      '"plan": {"price": 0.0, "name": "plan"}, "id": "id", '\
      '"name": "name", "email": "email"}'
    self.assertEquals(actual, expected)

  def test_create_paied_plan_signup_event(self):
    actual = sunnytrail.SignupEvent('id', 'name', \
      'email', sunnytrail.Plan('plan', 49), 123).to_json()

    expected = '{"action": {"name": "signup", "created": 123}, '\
      '"plan": {"price": 49.0, "name": "plan"}, "id": "id", '\
      '"name": "name", "email": "email"}'
    self.assertEqual(actual, expected)

  def test_create_payment_event(self):
    actual = sunnytrail.PayEvent('id', 'name', \
      'email', sunnytrail.Plan('plan', 49), 123).to_json()

    expected = '{"action": {"name": "pay", "created": 123}, '\
      '"plan": {"price": 49.0, "name": "plan"}, '\
      '"id": "id", "name": "name", "email": "email"}'
    self.assertEqual(actual, expected)

  def test_create_cancel_event(self):
    actual = sunnytrail.CancelEvent('id', 'name', 'email', 123).to_json()

    expected = '{"action": {"name": "cancel", "created": 123}, '\
      '"plan": {}, "id": "id", "name": "name", "email": "email"}'
    self.assertEqual(actual, expected)

class TestOpener(object):
  def __init__(self):
    self._url = self._data = None
    self._exception = None
    self._response = None

  def should_raise(self, e):
    self._exception = e

  def should_respond(self, r):
    self._response = r

  def open(self, url, data):
    if self._exception is not None:
      raise self._exception

    self._url, self._data = url, data

    class EmptyResponse(object):
      code = 202
      def read(self): return ''
      def close(self): pass

    return self._response or EmptyResponse()

class SunnytrailTest(unittest.TestCase):

  def setUp(self):
    self.client = sunnytrail.Sunnytrail('dummykey')

    self.opener = TestOpener()
    self.client.urlopen = self.opener.open

    self.cancel_event = sunnytrail.CancelEvent('id', 'name', 'email')

  def test_send_signup_event(self):
    self.client.send(sunnytrail.SignupEvent('id', 'name', \
      'email', sunnytrail.Plan('test')))

    assert 'dummykey' in self.opener._url

    data = simplejson.loads(
      parse_qs(self.opener._data)['message'][0])
    assert 'id' in data

  def test_403_error(self):
    class InvalidMessage(object):
      code = 403
      def close(self): pass
      def read(self):
        return '{"message": "invalid message", "errors": '\
          '[["message", "email should be valid"]]}'

    self.opener.should_respond(InvalidMessage())

    self.assertRaises(sunnytrail.SunnytrailException, 
      self.client.send, self.cancel_event)

  def test_403_error_invalid_json_response(self):
    class InvalidJSONResponse(object):
      code = 403
      def close(self): pass
      def read(self):
        return 'just a dummy string'

    self.opener.should_respond(InvalidJSONResponse())

    self.assertRaises(sunnytrail.SunnytrailException,
      self.client.send, self.cancel_event)

  def test_503_error(self):
    self.opener.should_raise(
      IOError('http error', 503, None, None))

    self.assertRaises(sunnytrail.ServiceUnavailable,
      self.client.send, self.cancel_event)

if __name__ == '__main__':
  unittest.main()

