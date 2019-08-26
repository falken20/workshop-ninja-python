#!/usr/bin/env python

# Copyright 2019
#
# Workshop Ninja Python

# Uso de Third-party libraries

# appengine_config.py
from google.appengine.api.modules import modules
from google.appengine.ext import vendor

# Add any libraries install in the "lib" folder.
vendor.add('lib')