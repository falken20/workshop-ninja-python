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
from google.appengine.api import users

from src import config

# Add any libraries install in the "lib" folder.
vendor.add('lib')

# Mostramos en logs el usuario conectado
if users.get_current_user() is not None:
    logging.info('WNP: ACCESO USUARIO --> %s', users.get_current_user().user_id())
else:
    logging.info('WNP: ACCESO USUARIO --> Usuario no detectado')

# Esta función sólo es llamada cuando no se asigna un namespace
def namespace_manager_default_namespace_for_request():
    logging.info('WNP: Namespace --> %s', config.NAME_SPACE)
    return config.NAME_SPACE