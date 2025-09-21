# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import math
import time
from contextlib import suppress
from logging import getLogger
from typing import Generator

from scrapy import Request, Spider
from scrapy.downloadermiddlewares.retry import get_retry_request
from scrapy.http import Response

import config.crawler

logger = getLogger(__name__)


class AccessTokenDownloaderMiddleware:
    def __init__(self):
        self.reset_times = {k: 0 for k in config.crawler.tokens}
        self.select_token = self._token_getter()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request: Request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        if 'Authorization' not in request.headers:
            token = next(self.select_token)
            request.headers.setlist('Authorization', [f'token {token}'])

    def process_response(self, request: Request, response: Response, spider: Spider):
        # Called with the response returned from the downloader.

        # Must either:
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        if not self._is_rate_limited(request, response):
            return response
        headers = request.headers
        if 'Authorization' not in headers:
            return response

        auth = headers.get('Authorization').decode()
        token = auth[6:]
        if len(token) != 40:
            return response

        if response.status == 401:
            logger.warning(f'Token {token} is invalid!')
            self.reset_times[token] = float('inf')
            request = request.copy()
            del request.headers['Authorization']
            return get_retry_request(request, spider=spider, reason='invalid_token')

        if 'Retry-After' in response.headers:
            sleep_time = int(response.headers.get('Retry-After')) + 10
            reset_time = time.time() + sleep_time
        elif 'X-RateLimit-Reset' in response.headers:
            reset_time = int(response.headers.get('X-RateLimit-Reset')) + 10
        else:
            sleep_time = 120
            reset_time = time.time() + sleep_time

        self.reset_times[token] = max(self.reset_times[token], math.ceil(reset_time))
        request = request.copy()
        del request.headers['Authorization']
        return get_retry_request(request, spider=spider, reason='token_rate_limit')

    def _token_getter(self) -> Generator[str, None, None]:
        while True:
            min_reset_time = float('inf')
            has_valid = False
            for token in list(self.reset_times):
                reset_time = self.reset_times[token]
                if time.time() > reset_time:
                    has_valid = True
                    yield token
                else:
                    min_reset_time = min(min_reset_time, reset_time)
            if not has_valid and (sleep_time := min_reset_time - time.time()) > 0:
                time_str = time.strftime('%H:%M:%S', time.localtime(min_reset_time))
                logger.info(f'All tokens are sleeping! Wait until {time_str}')
                time.sleep(sleep_time)
                time_str = time.strftime('%H:%M:%S', time.localtime())
                logger.info(f"{time_str}, I'm awake")

    @classmethod
    def _is_rate_limited(cls, request: Request, response: Response):
        if response.status in [429, 403, 401]:
            return True
        if request.url.endswith('/graphql') and response.status == 200 and b'"errors"' in response.body:
            with suppress(TypeError, KeyError, ValueError):
                body = json.loads(response.body)
                errors = body.get('errors', [])
                if any(x.get('type') == 'RATE_LIMITED' for x in errors):
                    return True
        return False
