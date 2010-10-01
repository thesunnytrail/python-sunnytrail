""" Sunnytrail client library.

The easiest and fastest way to integrate. This file can also be used as CLI tool if you wish to play with the API."""

import sys
import urllib
import simplejson

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
  def to_json(self):
    pass

class SignupEvent(Event):
  def __init__(self, name, email, plan):
    pass

class PayEvent(Event):
  pass

class CancelEvent(Event):
  pass

def main():
  pass

if __name__ == '__main__':
  sys.exit(main())

