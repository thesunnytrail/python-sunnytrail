
from distutils.core import setup

try:
  import setuptools
except ImportError:
  pass

setup(
  name='sunnytrail',
  version='0.1',
  description='Python Wrapper for the Sunnytrail API',
  author='Sunnytrail Team',
  author_email='andrei@thesunnytrail.com',
  url='http://www.thesunnytrail.com/',
  py_modules=['sunnytrail'],
  scripts=['sunnytrail'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
  ],
)

