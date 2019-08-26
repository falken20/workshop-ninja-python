#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python


import os
import jinja2
import webapp2
import logging
from google.appengine.ext import ndb
from google.appengine.api import app_identity

from src import model
from src import config
from src import storage_handler

# Establecemos la carpeta que va a contener los templates que se van a usar
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        ninjas = model.Ninja.query().order(-model.Ninja.date).fetch(10)

        templateValues = {
            'ninjas': ninjas
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(templateValues))


class SaveNinja(webapp2.RequestHandler):

    def post(self):
        ninja_ID = self.request.get('id')

        is_new_ninja = False
        if ninja_ID == '':
            logging.info('WNP: Ninja %s no tiene ID, es un alta', self.request.get('email'))
            is_new_ninja = True
            ninja = model.Ninja()
        else:
            ninja = model.Ninja.get_by_id(int(ndb.Key(model.Ninja, ninja_ID).id()))

        ninja.name = self.request.get('name')
        ninja.email = self.request.get('email')
    
        location = model.Location()
        location.building = self.request.get('building')
        location.department = self.request.get('department')
        ninja.location = location

        file_upload = self.request.POST.get('image')

        # Comprobamos si ha seleccionado algún archivo
        if hasattr(file_upload, 'filename'):
            # Si es modificación y tenia imagen guardada, borramos imagen anterior de GCS
            if not is_new_ninja and ninja.filename is not None:
                storage_handler.delete_file('', ninja.filename)

            # Guardamos fichero en GCS
            ninja.filename, ninja.imageUrl = storage_handler.upload_file(
                file_upload.file.read(), 
                '',
                file_upload.filename, 
                file_upload.type)  
            
        else:
            logging.info('WNP: Ninja sin imagen de perfil seleccionada, se queda como estaba')

        ninja.put()
        logging.info('WNP: Ninja %s almacenado correctamente', ninja.email)

        # Recargamos home con ninjas actualizados
        ninjas = model.Ninja.query().order(-model.Ninja.date).fetch(10)

        templateValues = {
            'ninjas': ninjas
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(templateValues))


class AddNinja(webapp2.RequestHandler):

    def get(self):
        action = 'Add'
        templateValues = {
            'action': action
        }
        template = JINJA_ENVIRONMENT.get_template('form-add.html')
        self.response.write(template.render(templateValues))


class UpdateNinja(webapp2.RequestHandler):

    def get(self):
        ninja_ID = self.request.get('ninja_ID')
        #ninja = model.Ninja.query(model.Ninja.key == ndb.Key(model.Ninja, ninja_ID).id()).fetch(1)[0]
        ninja = model.Ninja.get_by_id(int(ndb.Key(model.Ninja, ninja_ID).id()))

        action = 'Update'
        templateValues = {
            'action': action,
            'ninja': ninja
        }

        template = JINJA_ENVIRONMENT.get_template('form-update.html')
        self.response.write(template.render(templateValues))


class ShowNinja(webapp2.RequestHandler):

    def get(self):
        ninja_ID = self.request.get('ninja_ID')
        #ninja = model.Ninja.query(model.Ninja.key == ndb.Key(model.Ninja, ninja_ID).id()).fetch(1)[0]
        ninja = model.Ninja.get_by_id(int(ndb.Key(model.Ninja, ninja_ID).id()))

        action = 'Show'
        templateValues = {
            'action': action,
            'ninja': ninja
        }

        template = JINJA_ENVIRONMENT.get_template('form-ninja.html')
        self.response.write(template.render(templateValues))


class DeleteNinja(webapp2.RequestHandler):

    def get(self):
        ninja_ID = self.request.get('ninja_ID')
        ninja = model.Ninja.get_by_id(int(ndb.Key(model.Ninja, ninja_ID).id()))

        # Si tenia imagen guardada borramos imagen anterior de GCS
        if ninja.filename is not None:
            storage_handler.delete_file('', ninja.filename)

        ninja.key.delete()

        # Recargamos home con ninjas actualizados
        ninjas = model.Ninja.query().order(-model.Ninja.date).fetch(10)

        templateValues = {
            'ninjas': ninjas
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(templateValues))

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/saveNinja', SaveNinja),
    ('/addNinja', AddNinja),
    ('/updateNinja', UpdateNinja),
    ('/showNinja', ShowNinja),
    ('/deleteNinja', DeleteNinja)
    ], debug=True)
# [END app]
