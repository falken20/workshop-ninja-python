#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import logging

import webapp2

from src import model
from src import storage_handler
from src import namespace_handler

from src.utils import send, read_body


class Ninjas(webapp2.RequestHandler):

    def list(self):
        ninjas = model.Ninja.query().order(-model.Ninja.date).fetch(10)
        send(self, 200, ninjas)

    @staticmethod
    def save_ninja(ninja, data):
        ninja.name = data['name']
        ninja.email = data['email']
        ninja.building = data['building']
        ninja.department = data['department']

        key = ninja.put()

        # Comprobamos si ha seleccionado algún archivo
        if 'image' in data:
            image_data = data['image']
            # Guardamos fichero en GCS
            storage_handler.upload_base64_file(image_data, str(key.id()))

        logging.info('WNP: Ninja %s almacenado correctamente en namespace %s', ninja.email, namespace_handler.get_name_ns())

    def create(self):
        ninja_data = read_body(self)
        if ninja_data is None:
            send(self, 400) # Bad Request
        else:
            ninja = model.Ninja()
            try:
                Ninjas.save_ninja(ninja, ninja_data)
            except KeyError as e:
                send(self, 400, "No se encuentra la propiedad: %s" % e.message)  # Bad Request
                logging.info("WNP: No se encuentra la propiedad: %s", e.message)
                return
            send(self, 201, ninja)

    def update(self, ninja_id):
        ninja = model.Ninja.get_by_id(int(ninja_id))
        if ninja is None:
            send(self, 404)
        else:
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
        ninja = model.Ninja.get_by_id(int(ninja_id))
        if ninja is None:
            send(self, 404)
        else:
            ninja.key.delete()
            send(self, 200)

