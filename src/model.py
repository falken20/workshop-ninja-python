#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python


from google.appengine.ext import ndb


# [START ndb Location class] 
class Location(ndb.Model):
    building = ndb.StringProperty(required=True, indexed=True)
    department = ndb.StringProperty(indexed=False)
# [END ndb class]


# [START ndb Ninja class] 
class Ninja(ndb.Model):
    email = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=False)
    filename = ndb.StringProperty(required=False, indexed=False)
    imageUrl = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    location = ndb.StructuredProperty(Location)
# [END ndb class]
