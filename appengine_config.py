#!/usr/bin/env python

# Copyright 2019
#
# Workshop Ninja Python

# Uso de Third-party libraries

# appengine_config.py
import logging
from google.appengine.api.modules import modules
from google.appengine.ext import vendor
from google.appengine.api import namespace_manager

from src import config

# Add any libraries install in the "lib" folder.
vendor.add('lib')

# Called only if the current namespace is not set.
def namespace_manager_default_namespace_for_request():
    # The returned string will be used as the Google Apps domain.
    logging.info('WNP: Establecemos el namespace: %s', config.NAME_SPACE)
    return config.NAME_SPACE