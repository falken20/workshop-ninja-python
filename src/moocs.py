#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import logging
import re
import time

import webapp2

from src import model
from src import storage_handler
from src import namespace_handler

from src.utils import send, read_body

from google.appengine.ext.db import BadValueError


class Moocs(webapp2.RequestHandler):

    def list(self):
        # TODO: Obtener los moocs de un determinado ninja que podemos obtener de variable 'ninja_id' de la request
        # Mostrar los moocs ordenados por model.Mooc.date
        send(self, 200, moocs)

    def retrieve(self, mooc_id):
        # TODO: En este metodo recuperamos un determinado mooc a partir de su mooc_id
        if mooc is None:
            send(self, 404)
        else:
            send(self, 200, mooc)

    @staticmethod
    def save_mooc(mooc, data):
        mooc.ninja_id = data['ninja_id']
        mooc.name = data['name']
        mooc.desc = data['desc']
        mooc.points = data['points']

        # Comprobamos si ha seleccionado algún archivo
        if 'file' in data:
            file_data = data['file']
            # Guardamos fichero en GCS
            mime, data = re.match('data:(.*);base64,(.*)', file_data).groups()
            mooc.file = storage_handler.upload_base64_file(data, mime, "%s_%d" % (mooc.ninja_id, int(time.time())))
            mooc.put()

        mooc.put()
        logging.info('WNP: Mooc %s almacenado correctamente en namespace %s', mooc.name, namespace_handler.get_name_ns())

    def create(self):
        # Se ejecuta al guardar los datos de un mooc en su mantenimiento
        mooc_data = read_body(self)
        if mooc_data is None:
            send(self, 400)  # Bad Request
        else:
            ninja = model.Ninja.get_by_id(mooc_data['ninja_id'])
            if ninja is None:
                send(self, 404)
            else:
                mooc = model.Mooc()
                try:
                    Moocs.save_mooc(mooc, mooc_data)
                except KeyError as e:
                    send(self, 400, "No se encuentra la propiedad: %s" % e.message)  # Bad Request
                    logging.info("WNP: No se encuentra la propiedad: %s", e.message)
                    return
                except BadValueError as e:
                    send(self, 400, "Valor incorrecto: %s" % e.message)
                    logging.info("WNP: Valor incorrecto: %s", e.message)
                    return
                send(self, 201, mooc)

    def delete(self, mooc_id):
        # TODO: Completa el método para elimina un determinado mooc
        if mooc is None:
            send(self, 404)
        else:
            send(self, 204)
