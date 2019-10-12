#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

from google.appengine.api.modules import modules


# Asignamos a la variable el ID del proyecto
PROJECT_ID = 'dev-bbva-gae-cicd'

# TODO:
# Establecemos el nombre del bucket asi como extensiones permitidas
CLOUD_STORAGE_BUCKET = modules.get_current_module_name()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# El nombre de namespace se toma del nombre del servicio desplegado
NAME_SPACE = modules.get_current_module_name()
