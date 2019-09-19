#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import logging
import re

import webapp2

from src import model
from src import storage_handler
from src import namespace_handler

from src.utils import send, read_body

from google.appengine.ext.db import BadValueError


class Moocs(webapp2.RequestHandler):

    def list(self):
        ninja_id = self.request.get('ninja_id', default_value=None)
        if ninja_id is None:
            moocs = model.Mooc.query().order(model.Mooc.date).fetch()
        else:
            moocs = model.Mooc.query(model.Mooc.ninja_id == int(ninja_id)).order(model.Mooc.date).fetch()
        send(self, 200, moocs)

    def retrieve(self, mooc_id):
        mooc = model.Mooc.get_by_id(int(mooc_id))
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
        key = mooc.put()
        logging.info('WNP: Mooc %s almacenado correctamente en namespace %s', mooc.name, namespace_handler.get_name_ns())

    def create(self):
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
        mooc = model.Mooc.get_by_id(int(mooc_id))
        if mooc is None:
            send(self, 404)
        else:
            mooc.key.delete()
            send(self, 204)