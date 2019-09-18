#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

from webapp2 import WSGIApplication, Route

from src.ninjas import Ninjas
from src.moocs import Moocs

# [START app]
app = WSGIApplication([
    Route('/ninjas', handler=Ninjas, handler_method='list', methods=['GET']),
    Route('/ninjas', handler=Ninjas, handler_method='create', methods=['POST']),
    Route('/ninjas/<ninja_id>', handler=Ninjas, handler_method='retrieve', methods=['GET']),
    Route('/ninjas/<ninja_id>', handler=Ninjas, handler_method='update', methods=['PUT']),
    Route('/ninjas/<ninja_id>', handler=Ninjas, handler_method='delete', methods=['DELETE']),

    Route('/ninjas/<ninja_id>/moocs', handler=Moocs, handler_method='list', methods=['GET']),
    Route('/ninjas/<ninja_id>/moocs', handler=Moocs, handler_method='create', methods=['POST']),
    Route('/ninjas/<ninja_id>/moocs/<mooc_id>', handler=Moocs, handler_method='retrieve', methods=['GET']),
    Route('/ninjas/<ninja_id>/moocs/<mooc_id>', handler=Moocs, handler_method='delete', methods=['DELETE']),
    ], debug=True)
# [END app]
