import re

import scrapy
from scrapy import Request
from scrapy.http import Response

import config.paths


class RawPullListSpider(scrapy.Spider):
    name = 'raw_pull_list'
    allowed_domains = ['github.com']
    output_base = config.paths.raw_pull_list

    def start_requests(self):
        self.output_base.mkdir(parents=True, exist_ok=True)
        for repo in config.paths.repos.read_text().splitlines():
            repo_output_base = self.output_base / repo.replace('/', '$')
            repo_output_base.mkdir(exist_ok=True)
            url = f'https://api.github.com/repos/{repo}/pulls?state=all&direction=asc&per_page=100'
            yield Request(url, callback=self.parse_page, cb_kwargs={'repo': repo, 'page': 1})

    def parse(self, response, **kwargs):
        raise NotImplementedError

    def parse_page(self, response: Response, repo: str, page: int):
        out = self.output_base / repo.replace('/', '$') / f'{page}.json'
        out.write_bytes(response.body)

        link: bytes = response.headers.get('link')
        if link:
            for item in link.decode().split(','):
                match = re.match(r'^<(.+)>; rel="next"$', item.strip())
                if match:
                    yield Request(match.group(1), callback=self.parse_page,
                                  cb_kwargs={'repo': repo, 'page': page + 1})
