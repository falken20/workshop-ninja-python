#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import logging
import re

from google.appengine.ext import ndb

import webapp2

from src import model
from src import storage_handler
from src import namespace_handler

from src.utils import send, read_body


class Ninjas(webapp2.RequestHandler):

    def list(self):
        department = self.request.get('department', default_value=None)
        if department is None:
            ninjas = model.Ninja.query().order(model.Ninja.name).fetch()
        else:
            ninjas = model.Ninja.query(model.Ninja.department == department).order(model.Ninja.name).fetch()
        send(self, 200, ninjas)

    def retrieve(self, ninja_id):
        ninja = model.Ninja.get_by_id(int(ninja_id))
        if ninja is None:
            send(self, 404)
        else:
            send(self, 200, ninja)

    @staticmethod
    def save_ninja(ninja, data):
        # Asignamos los valores recogidos
        ninja.name = data['name']
        ninja.email = data['email']
        ninja.building = data['building']
        ninja.department = data['department']

        # Comprobamos si ha seleccionado algún archivo
        if 'image' in data:
            image_data = data['image']
            if image_data != "":
                # Guardamos fichero en GCS
                # Contenido: 'data:image/png;base64,iVBORw...'
                # Extraer tipo mime de la imagen y datos en base 64
                mime, data = re.match('data:(.*);base64,(.*)', image_data).groups()
                ninja.image = storage_handler.upload_base64_file(data, mime, str(ninja.key.id()))
            else:
                # Borramos imagen en GCS
                storage_handler.delete_file(str(ninja.key.id()))
                ninja.image = None

        # Almacenamos el objeto ninja
        ninja.put()

        logging.info('WNP: Ninja %s almacenado correctamente en namespace %s', ninja.email, namespace_handler.get_name_ns())

    def create(self):
        # Recogemos los campos introducidos por el usuario
        ninja_data = read_body(self)
        if ninja_data is None:
            send(self, 400) # Bad Request
        else:
            # Creamos un objeto ninja a partir de la clase Ninja(model.py), en él guardaremos los campos del formulario
            ninja = model.Ninja()
            # Asignamos y reservamos un id
            first, last = model.Ninja.allocate_ids(1)
            # Generamos una clave única a partir del id
            ninja.key = ndb.Key(model.Ninja, first)
            try:
                Ninjas.save_ninja(ninja, ninja_data)
            except KeyError as e:
                send(self, 400, "No se encuentra la propiedad: %s" % e.message)  # Bad Request
                logging.info("WNP: No se encuentra la propiedad: %s", e.message)
                return
            send(self, 201, ninja)

    def update(self, ninja_id):
        # Obtenemos el ninja a modificar a partir de su ID
        ninja = model.Ninja.get_by_id(int(ninja_id))
        if ninja is None:
            send(self, 404)
        else:
            # Recogemos los campos introducidos por el usuario
            ninja_data = read_body(self)
            if ninja_data is None:
                send(self, 400)  # Bad Request
            else:
                try:
                    Ninjas.save_ninja(ninja, ninja_data)
                except KeyError as e:
                    send(self, 400, "No se encuentra la propiedad: %s" % e.message)  # Bad Request
                    logging.info("WNP: No se encuentra la propiedad: %s", e.message)
                    return
                send(self, 200, ninja)

    def delete(self, ninja_id):
        # Obtenemos el ninja a eliminar a partir de su ID
        ninja = model.Ninja.get_by_id(int(ninja_id))
        if ninja is None:
            send(self, 404)
        else:
            ninja.key.delete()
            send(self, 204)

