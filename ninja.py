#!/usr/bin/env python

# Copyright 2019
#
# Workshop Ninja Python

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def ninja_key(email):
    """
    Constructs a Datastore key for a Ninja entity.We use email as the key.
    """
    return ndb.Key('Ninja', email)

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
        query = Ninja.query().order(-Ninja.date)
        ninjas = query.fetch(10)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        templateValues = {
            'ninjas': ninjas,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(templateValues))


class saveNinja(webapp2.RequestHandler):

    def post(self):
        ninja = Ninja()
        ninja.name = self.request.get('name')
        ninja.email = self.request.get('email')
        ninja.imageUrl = self.request.get('imageUrl')      

        location = Location()
        location.building = self.request.get('building')
        location.department = self.request.get('department')
        ninja.location = location

        ninja.put()

        query_params = {'email': ninja.name}
        self.redirect('/?' + urllib.urlencode(query_params))


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

        print('LOG -------> ', ninja_ID)

        query = Ninja.query(Ninja.key == ndb.Key(Ninja, 'aghkZXZ-Tm9uZXISCxIFTmluamEYgICAgIDArwoM'))
        ninja = Ninja.get_by_id('5838406743490560')
        #query = Ninja.query(Ninja.ID == ninja_ID)
        #ninja = query.fetch(1)

        print('LOG -------> ', ninja)

        action = 'Update'
        templateValues = {
            'action': action,
            'ninja': ninja
        }

        template = JINJA_ENVIRONMENT.get_template('form-update.html')
        self.response.write(template.render(templateValues))


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/save', saveNinja),
    ('/form-add', AddNinja),
    ('/form-update', UpdateNinja)
    ], debug=True)
# [END app]
