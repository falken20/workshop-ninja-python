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
from src import storage

# Establecemos la carpeta que va a contener los templates que se van a usar
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Establecemos token de identidad
auth_token = app_identity.get_access_token('https://www.googleapis.com/auth/cloud-platform')
logging.info('WNP: Using token {} to represent identity {}'.format(auth_token, app_identity.get_service_account_name()))

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

        if ninja_ID == '':
            logging.info('WNP: Ninja %s no tiene ID', self.request.get('email'))
            ninja = model.Ninja()
        else:
            ninja = model.Ninja.get_by_id(int(ndb.Key(model.Ninja, ninja_ID).id()))

        ninja.name = self.request.get('name')
        ninja.email = self.request.get('email')
    
        location = model.Location()
        location.building = self.request.get('building')
        location.department = self.request.get('department')
        ninja.location = location

        fileUpload = self.request.POST.get('image')

        # Comprobamos si ha seleccionado algún archivo
        if hasattr(fileUpload, 'filename'):
            logging.info('WNP: Imagen a almacenar en Google Cloud Storage -> %s', fileUpload.filename)
            imageUrlGCS = storage.upload_file(fileUpload, fileUpload.filename)
            logging.info('WNP: url imagen a almacenar en Google Cloud Storage %s', imageUrlGCS)
            ninja.imageUrl = imageUrlGCS  
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
