""" Sunnytrail client library.

The easiest and fastest way to integrate. This file can also be used as CLI tool if you wish to play with the API."""

import sys
import urllib
import simplejson

from time import time

class SunnytrailException(Exception): 
  """ Generic class for Sunnytrail related exceptions """
  pass

class Sunnytrail(object):
  def __init__(self, key, base_url='api.thesunnytrail.com', use_ssl=True):
    self.key = key
    self._base_url = ("https://%s" if use_ssl else "http://%s") % url
    self._use_ssl = use_ssl

  def send_event(self, event):
    """ Send an event to the API """
    print event.to_json()
    
class Event(object):
  def __init__(self, id, name, email, action, plan):
    pass 

  def to_json(self):
    pass

class Plan(object):
  def __init__(self, name, price, recurring = None):
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

def main():
  pass

if __name__ == '__main__':
  sys.exit(main())

