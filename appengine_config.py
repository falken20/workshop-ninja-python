#!/usr/bin/env python
# coding=utf-8

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

# Esta función sólo es llamada cuando no se asigna un namespace
def namespace_manager_default_namespace_for_request():
    # Si quisieramos por ejemplo establecer el usuario logado como namespace (from google.appengine.api import users)
    # return users.get_current_user().user_id() 
    logging.info('WNP: Namespace --> %s', config.NAME_SPACE)
    return config.NAME_SPACE