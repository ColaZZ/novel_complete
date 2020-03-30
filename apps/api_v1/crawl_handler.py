#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests

from apps.found_handler import FoundHandler
from lib.routes import route

from crawl_35.spiders.daily import DailySpider

STATES = ['running', 'finished', 'pending']


@route('/daily_update')
class DailyUpdateHandler(FoundHandler):
    def post(self):
        payload = json.loads(self.request.body)
        response = requests.post('http://localhost:6800/schedule.json', data=payload)
        self.write(response.text)

    def get(self, job=None):
        response = requests.get('http://localhost:6800/listjobs.json?project=crawl_35').json()
        ret = {'state': None}
        for state in STATES:
            if job in [j['id'] for j in response[state]]:
                ret['state'] = state
                self.write(json.dumps(ret))


@route('/crawl_article')
class CrawlArticleHandler(FoundHandler):
    def post(self):
        payload = json.loads(self.request.body)
        print(payload)
        response = requests.post('http://localhost:6800/schedule.json', data=payload)
        self.write(response.text)

    def get(self, job=None):
        response = requests.get('http://localhost:6800/listjobs.json?project=crawl_article').json()
        ret = {'state': None}
        for state in STATES:
            if job in [j['id'] for j in response[state]]:
                ret['state'] = state
                self.write(json.dumps(ret))
