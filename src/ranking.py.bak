#!/usr/bin/env python
# coding=utf-8

# Copyright 2019
#
# Workshop Ninja Python

import webapp2
import logging
from itertools import groupby
from google.appengine.ext import ndb

from src import model

from src.utils import send


class Ranking(webapp2.RequestHandler):

    def ninja_info(self, ranking, ninja):
        if ninja is not None:
            ranking['_id'] = ninja.key.id()
            ranking['name'] = ninja.name
            ranking['department'] = ninja.department
            ranking['email'] = ninja.email
            ranking['building'] = ninja.building
            ranking['image'] = ninja.image

    def sum_moocs(self, moocs):
        return sum(m.points for m in moocs)

    def ranking(self):
        # Obtengo todos los moocs pero ordenados por el ID del ninja
        moocs = model.Mooc.query().order(model.Mooc.ninja_id).fetch()

        # Solution 1
        ranking = sorted([
            {'ninja_id': ninja_id, 'points': self.sum_moocs(ninja_moocs)}
            for ninja_id, ninja_moocs in groupby(moocs, key=lambda x: x.ninja_id)
        ], key=lambda n: - n['points'])

        # Solution 2
        #points = {}
        #for mooc in moocs:
        #    if mooc.ninja_id in points:
        #        points[mooc.ninja_id] += mooc.points
        #    else:
        #        points[mooc.ninja_id] = mooc.points
        #ranking = []
        #for ninja in points:
        #    ranking.append({'ninja_id': ninja, 'points': points[ninja]})
        #ranking = sorted(ranking, key=lambda n: - n['points'])

        # Recuperar información de cada usuario
        ninjas = ndb.get_multi([ndb.Key(model.Ninja, id) for id in map(lambda x: x['ninja_id'], ranking)])
        for i in range(len(ranking)):
            self.ninja_info(ranking[i], ninjas[i])

        send(self, 200, ranking)

    def points(self, ninja_id):
        moocs = model.Mooc.query(model.Mooc.ninja_id == int(ninja_id)).fetch()
        points = {'ninja_id': int(ninja_id), 'points': self.sum_moocs(moocs)}
        self.ninja_info(points, model.Ninja.get_by_id(int(ninja_id)))
        send(self, 200, points)
