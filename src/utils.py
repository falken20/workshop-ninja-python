#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import logging

import json

import datetime

from google.appengine.ext import ndb


def serialize(model):
    """ Returns dictionary from a ndb.Model object """
    if isinstance(model, list):
        return [serialize(i) for i in model]
    elif isinstance(model, ndb.Model):
        data = model.to_dict()
        data['_id'] = model.key.id()
        return serialize(data)
    elif isinstance(model, dict):
        obj = {}
        for prop in model.keys():
            value = model[prop]
            if value is None:
                continue

            if isinstance(value, ndb.Expando):
                obj[prop] = serialize(value)
            elif isinstance(value, ndb.Key):
                print value
                obj[prop] = value
            elif isinstance(value, datetime.datetime):
                obj[prop] = str(value)
            elif isinstance(value, str):
                obj[prop] = value
            elif isinstance(value, unicode):
                obj[prop] = value
            elif isinstance(value, long):
                obj[prop] = value
            elif isinstance(value, int):
                obj[prop] = value
            elif isinstance(value, list):
                obj[prop] = []
                for item in value:
                    obj[prop].append(serialize(item))
            else:
                logging.warning("WNP: Type not converted: %s" % value.__class__.__name__)
                obj[prop] = value
        return obj
    else:
        return None


def send(handler, code, data=None):
    """ Sends a response in json format, with all nedded headers """
    handler.response.headers['Content-Type'] = 'application/json'
    handler.response.headers['Access-Control-Allow-Origin'] = '*'
    handler.response.status = code
    if data is not None:
        handler.response.write(json.dumps(serialize(data)))


def read_body(handler):
    """ Reads json body """
    try:
        return json.loads(handler.request.body)
    except ValueError:
        return None
