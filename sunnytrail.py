""" Sunnytrail client library.

The easiest and fastest way to integrate. This file can also 
be used as CLI tool if you wish to play with the API."""

import sys
import urllib
import simplejson

from urllib import FancyURLopener
from time import time

class SunnytrailOpener(FancyURLopener):
  version = 'Sunnytrail Python API Wrapper 1.0'

class SunnytrailException(Exception): 
  """ Generic class for Sunnytrail related exceptions """
  pass

class Sunnytrail(object):
  opener = SunnytrailOpener

  def __init__(self, key, base_url='api.thesunnytrail.com', use_ssl=True):
    self._key = key
    self._base_url = ("https://%s" if use_ssl else "http://%s") % base_url
    self._messages_url = "%s/messages?%s" % \
      (self._base_url, urllib.urlencode({'apikey': self._key}))
    self._use_ssl = use_ssl

  def send(self, event):
    """ Send an event to the API """
    h = self.opener().open(self._messages_url, \
      {'message': event.to_json()})
    r = h.read()
 
class Event(object):
  def __init__(self, id, name, email, action, plan):
    self._id = id
    self._name = name
    self._email = email
    self._action = action
    self._plan = plan

  def to_hash(self):
    ret = {
      'name': self._name,
      'email': self._email,
      'action': self._action.to_hash(),
      'plan': self._plan.to_hash()
    }
    if self._id is not None:
      ret['id'] = self._id

    return ret

  def to_json(self):
    return simplejson.dumps(self.to_hash())

class SignupEvent(Event):
  def __init__(self, id, name, email, plan, created=None):
    super(SignupEvent, self).__init__(id, name, \
      email, SignupAction(created), plan)

class PayEvent(Event):
  def __init__(self, id, name, email, plan, created=None):
    super(PayEvent, self).__init__(id, name, \
      email, PayAction(created), plan)

class CancelEvent(Event):
  def __init__(self, id, name, email, created = None):
    super(CancelEvent, self).__init__(id, \
      name, email, CancelAction(created), EmptyPlan())

class EmptyPlan(object):
  def to_hash(self): return {}

class Plan(object):
  def __init__(self, name, price = 0, recurring = None):
    self._name = name
    self._price = float(price)
    self._recurring = None if recurring is None else int(recurring)

  @property
  def name(self): return self._name

  @property
  def price(self): return self._price

  @property 
  def recurring(self): return self._recurring

  @property
  def is_recurring(self): return self._recurring is not None

  def to_hash(self):
    ret = {
      'name': self._name,
      'price': self._price
    }
    if self.is_recurring:
      ret['recurring'] = self._recurring

    return ret

class Action(object):
  def __init__(self, name, created=None):
    created = created if created is not None else time()

    if name not in ('signup', 'pay', 'cancel'):
      raise ValueError('Invalid action name. '\
        'Expected values: signup, pay or cancel')

    self._name = name
    self._created = int(created)

  @property
  def name(self): return self._name

  @property
  def created(self): return self._created

  def to_hash(self):
    return {
      'name': self._name,
      'created':  self._created
    }

class SignupAction(Action):
  def __init__(self, created=None):
    super(SignupAction, self).__init__('signup', created)

class PayAction(Action):
  def __init__(self, created=None):
    super(PayAction, self).__init__('pay', created)

class CancelAction(Action):
  def __init__(self, created=None):
    super(CancelAction, self).__init__('cancel', created)

def main():
  pass

if __name__ == '__main__':
  sys.exit(main())

