#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python


from google.appengine.api import namespace_manager


def get_name_ns():
    return namespace_manager.get_namespace() if namespace_manager.get_namespace() else 'default'