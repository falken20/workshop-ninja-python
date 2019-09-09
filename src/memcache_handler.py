#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python


import logging
from google.appengine.api import memcache


def list_stats_memcache():
    stats = memcache.get_stats()
    logging.info('WNP: Memcache Items: %s', format(stats['items']))


def add_key_memcache(key, value, time=3600):
    memcache.set(format(key), value, time)
    logging.info('WNP: Valor añadido a memcache: {0}, {1}'.format(key, value))
    list_stats_memcache()