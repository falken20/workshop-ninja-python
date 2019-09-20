#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python


from google.appengine.ext import ndb


# [START ndb Ninja class] 
class Ninja(ndb.Model):
    email = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=True)
    building = ndb.StringProperty(required=True)
    department = ndb.StringProperty(required=True, indexed=True)
    image = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
# [END ndb class]


# [START ndb Mooc class]
class Mooc(ndb.Model):
    ninja_id = ndb.IntegerProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=False)
    desc = ndb.StringProperty(required=True, indexed=False)
    points = ndb.IntegerProperty(required=True, indexed=False)
    date = ndb.DateTimeProperty(auto_now=True, indexed=True)
    file = ndb.StringProperty(required=False, indexed=False)
# [END ndb class]

