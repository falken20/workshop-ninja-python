#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import os


# TODO: Asignamos a la variable el ID del proyecto
PROJECT_ID = os.environ.get('PROJECT_ID', '')

# TODO: Establecemos el nombre del bucket asi como tamaños máximos y extensiones permitidas
CLOUD_STORAGE_BUCKET = 'bucket-ninja'
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])