#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python


import os

from google.appengine.ext import ndb
import logging
import ninja_storage

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# [START ndb classes] 
class Location(ndb.Model):
    building = ndb.StringProperty(required=True, indexed=True)
    department = ndb.StringProperty(indexed=False)


class Ninja(ndb.Model):
    email = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=False)
    imageUrl = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    location = ndb.StructuredProperty(Location)
# [END ndb classes]


class MainPage(webapp2.RequestHandler):

    def get(self):
        ninjas = Ninja.query().order(-Ninja.date).fetch(10)

        templateValues = {
            'ninjas': ninjas
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(templateValues))


class SaveNinja(webapp2.RequestHandler):

    def post(self):
        ninja_ID = self.request.get('id')

        if ninja_ID == '':
            logging.info('Ninja %s no tiene ID' % self.request.get('email'))
            ninja = Ninja()
        else:
            ninja = Ninja.get_by_id(int(ndb.Key(Ninja, ninja_ID).id()))

        ninja.name = self.request.get('name')
        ninja.email = self.request.get('email')
        ninja.imageUrl = self.request.get('imageUrl')  
    
        location = Location()
        location.building = self.request.get('building')
        location.department = self.request.get('department')
        ninja.location = location

        ninja.put()

        logging.info('Ninja %s almacenado correctamente' % ninja.email)

        # Recargamos home con ninjas actualizados
        ninjas = Ninja.query().order(-Ninja.date).fetch(10)

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
        #ninja = Ninja.query(Ninja.key == ndb.Key(Ninja, ninja_ID).id()).fetch(1)[0]
        ninja = Ninja.get_by_id(int(ndb.Key(Ninja, ninja_ID).id()))

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
        #ninja = Ninja.query(Ninja.key == ndb.Key(Ninja, ninja_ID).id()).fetch(1)[0]
        ninja = Ninja.get_by_id(int(ndb.Key(Ninja, ninja_ID).id()))

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
        ninja = Ninja.get_by_id(int(ndb.Key(Ninja, ninja_ID).id()))
        ninja.key.delete()


        # Recargamos home con ninjas actualizados
        ninjas = Ninja.query().order(-Ninja.date).fetch(10)

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
