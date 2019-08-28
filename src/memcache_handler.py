#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python


import logging
from google.appengine.api import memcache


def list_stats_memcache():
    stats = memcache.get_stats()
    logging.info('WPN: Memcache Hits: %s', format(stats['hits']))
    logging.info('WPN: Memcache Misses: %s', format(stats['misses']))
    logging.info('WPN: Memcache Items: %s', format(stats['items']))