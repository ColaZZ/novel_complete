#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests

from apps.found_handler import FoundHandler
from lib.routes import route

from crawl_35.spiders.daily import DailySpider


@route('/daily_update')
class DailyUpdateHandler(FoundHandler):
    def post(self):
        payload = json.loads(self.request.body)
        response = requests.post('http://scrapyd:6800/schedule.json', data=payload)
        self.write(response.text)

    def get(self, job=None):
        response = requests.get('http://scrapyd:6800/listjobs.json?project=crawl_35').json()
        states = ['running', 'finished', 'pending']
        ret = {'state': None}
        for state in states:
            if job in [j['id'] for j in response[state]]:
                ret['state'] = state
                self.write(json.dumps(ret))



