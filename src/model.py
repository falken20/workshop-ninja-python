#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python


from google.appengine.ext import ndb


# [START ndb Ninja class] 
class Ninja(ndb.Model):
    email = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=False)
    building = ndb.StringProperty(required=True)
    department = ndb.StringProperty(required=True, indexed=True)
    filename = ndb.StringProperty(required=False, indexed=False)
    imageUrl = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
# [END ndb class]


