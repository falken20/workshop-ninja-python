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
from google.appengine.api import namespace_manager


from src import model
from src import storage_handler
from src import memcache_handler

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
        ninja.building = self.request.get('building')
        ninja.department = self.request.get('department')

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

        key = ninja.put()

        # TODO
        # Lo añadimos a la memcache
        memcache_handler.add_key_memcache(key.id(), ninja)

        # TODO
        ns = namespace_manager.get_namespace() if namespace_manager.get_namespace() else 'default'

        logging.info('WNP: Ninja %s almacenado correctamente en namespace %s', ninja.email, ns)

        # Recargamos home con ninjas actualizados
        ninjas = model.Ninja.query().order(-model.Ninja.date).fetch(10)

        templateValues = {
            'ninjas': ninjas
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(templateValues))


class AddNinja(webapp2.RequestHandler):

    def get(self):
        templateValues = {
            'action': 'Add'
        }

        template = JINJA_ENVIRONMENT.get_template('form-add.html')
        self.response.write(template.render(templateValues))


class UpdateNinja(webapp2.RequestHandler):

    def get(self):
        ninja_ID = self.request.get('ninja_ID')

        ninja = ndb.Key(model.Ninja, long(ninja_ID)).get()

        templateValues = {
            'action': 'Update',
            'ninja': ninja
        }

        template = JINJA_ENVIRONMENT.get_template('form-update.html')
        self.response.write(template.render(templateValues))


class ShowNinja(webapp2.RequestHandler):

    def get(self):
        ninja_ID = self.request.get('ninja_ID')

        ninja = model.Ninja.get_by_id(int(ndb.Key(model.Ninja, ninja_ID).id()))

        templateValues = {
            'action': 'Show',
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


class SearchNinja(webapp2.RequestHandler):

    def get(self):

        ninjas = model.Ninja.query().order(-model.Ninja.date).fetch(10)

        templateValues = {
            'ninjas': ninjas,
            'action': 'Search'
        }

        template = JINJA_ENVIRONMENT.get_template('form-search.html')
        self.response.write(template.render(templateValues))


class GetFilterNinja(webapp2.RequestHandler):

    def post(self):
        ninja_filter = self.request.get('ninja_filter')

        logging.info('WPN: Realizamos filtro con el valor %s', ninja_filter)

        if ninja_filter == '' or ninja_filter is None:
            ninjas = model.Ninja.query().order(-model.Ninja.date).fetch(10)
        else:
            ninjas = model.Ninja.query(model.Ninja.department == ninja_filter).order(-model.Ninja.date)
            # ninjas = ndb.gql("SELECT * FROM Ninja WHERE department = :1 ORDER BY date", ninja_filter)

        templateValues = {
            'ninjas': ninjas,
            'action': 'Search',
            'ninja_filter': ninja_filter
        }

        template = JINJA_ENVIRONMENT.get_template('form-search.html')
        self.response.write(template.render(templateValues))

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/saveNinja', SaveNinja),
    ('/addNinja', AddNinja),
    ('/updateNinja', UpdateNinja),
    ('/showNinja', ShowNinja),
    ('/deleteNinja', DeleteNinja),
    ('/searchNinja', SearchNinja),
    ('/getFilterNinja', GetFilterNinja)
    ], debug=True)
# [END app]
