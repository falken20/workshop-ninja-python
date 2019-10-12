#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

# Uso de Third-party libraries

# appengine_config.py
import os
import logging
from google.appengine.api.modules import modules
from google.appengine.ext import vendor
from google.appengine.api import namespace_manager
from google.appengine.api import users


from src import config


# Add any libraries install in the "lib" folder.
vendor.add('lib')


# Mostramos en logs algunas variables de entorno
# logging.info('WNP: OS VALUE --> %s', format(os.environ.viewvalues()))
logging.info('WNP: SERVER_NAME --> %s', format(os.environ.get('SERVER_NAME', '')))

# Mostramos en logs el usuario conectado
if users.get_current_user():
    logging.info('WNP: ACCESO USUARIO --> %s', users.get_current_user().email())
else:
    logging.info('WNP: ACCESO USUARIO --> Usuario no detectado')

# Mostramos en logs namespace usado
if config.NAME_SPACE:
    logging.info('WNP: NAMESPACE --> %s', config.NAME_SPACE)
else:
    logging.info('WNP: NAMESPACE --> default')

# Mostramos en logs el nombre del bucket a utilizar
if config.CLOUD_STORAGE_BUCKET:
    logging.info('WNP: BUCKET --> %s', config.CLOUD_STORAGE_BUCKET)
else:
    logging.error('WNP: BUCKET --> no definido')

# TODO:
# Esta función sólo es llamada cuando no se asigna un namespace
def namespace_manager_default_namespace_for_request():
    return config.NAME_SPACE