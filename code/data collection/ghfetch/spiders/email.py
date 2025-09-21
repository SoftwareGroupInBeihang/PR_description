import csv
import json

import scrapy
from scrapy import Request
from scrapy.http import Response

import config.paths


class EmailSpider(scrapy.Spider):
    name = 'email'
    allowed_domains = ['github.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.emails = []

    def start_requests(self):
        participants = json.loads(config.paths.participants.read_text('utf8'))
        for participant in participants:
            yield Request(f'https://api.github.com/users/{participant}',
                          callback=self.parse_user, dont_filter=True, cb_kwargs={'user': participant})

    def parse(self, response, **kwargs):
        raise NotImplementedError

    def parse_user(self, response: Response, user: str):
        data = json.loads(response.body)
        email = data.get('email')
        self.emails.append((user, email))

    def closed(self, reason):
        self.emails.sort()
        with open(config.paths.emails, 'w', encoding='utf-8-sig', newline='') as f:
            csv.writer(f).writerows(self.emails)
