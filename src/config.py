#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import os


# Asignamos a la variable el ID del proyecto
PROJECT_ID = os.environ.get('PROJECT_ID', '')

# Establecemos el nombre del bucket asi como extensiones permitidas
CLOUD_STORAGE_BUCKET = 'bucket-ninja'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Establecemos el namespace
NAME_SPACE = ''
