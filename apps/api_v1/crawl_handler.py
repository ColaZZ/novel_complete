#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests

from apps.found_handler import FoundHandler
from utils.routes import route

from crawl_35.spiders.daily import DailySpider

STATES = ['running', 'finished', 'pending']


@route('/daily_update')
class DailyUpdateHandler(FoundHandler):
    def post(self):
        payload = json.loads(self.request.body)
        state = payload.pop("state", "")
        if state == "run":
            # 执行
            response = requests.post('http://localhost:6800/schedule.json', data=payload)
        elif state == "stop":
            # 停止
            response = requests.post('http://localhost:6800/cancel.json')
        else:
            return self.write({"state": "error"})
        self.write(response.text)

    def get(self):
        # 查看状态
        job = self.get_argument("job", "")
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
        state = payload.pop("state", "")
        if state == "run":
            # 执行
            response = requests.post('http://localhost:6800/schedule.json', data=payload)
        elif state == "stop":
            # 停止
            response = requests.post('http://localhost:6800/cancel.json', data=payload)
        else:
            return self.write({"state": "error"})
        self.write(response.text)

    # 获取crawl_article状态
    def get(self):
        job = self.get_argument("job", "")
        response = requests.get('http://localhost:6800/listjobs.json?project=crawl_article').json()
        ret = {'state': None}
        for state in STATES:
            print(job)
            if job in [j['id'] for j in response[state]]:
                ret['state'] = state
                self.write(json.dumps(ret))


@route('/crawl')
class CrawlHandler(FoundHandler):
    def post(self):
        payload = json.loads(self.request.body)
        state = payload.pop("state", "")
        # spider = payload.get("spider", "")
        if state == "run":
            # 执行
            response = requests.post('http://localhost:6800/schedule.json', data=payload)
        elif state == "stop":
            response = requests.post('http://localhost:6800/cancel.json', data=payload)
        else:
            return self.write({"state": "error"})
        self.write(response.text)

    def get(self):
        job = self.get_argument("job", "")
        response = requests.get('http://localhost:6800/listjobs.json?project=crawl_article').json()
        ret = {'state': None}
        for state in STATES:
            if job in [j['id'] for j in response[state]]:
                ret['state'] = state
                self.write(json.dumps(ret))
