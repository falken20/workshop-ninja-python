#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import os


# Asignamos a la variable el ID del proyecto
PROJECT_ID = os.environ.get('PROJECT_ID', '')

# Establecemos el nombre del bucket asi como extensiones permitidas
CLOUD_STORAGE_BUCKET = 'bucket-ninja-ws'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# TODO 1: Establecemos el namespace que luego será usado en appengine_config.py
NAME_SPACE = ''
