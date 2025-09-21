import json
import re

import scrapy
from scrapy import Request
from scrapy.http import Response

import config.paths

query = re.sub(r'\s+', ' ', """
query ($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      number
      state
      isDraft
      author {
        login
        __typename
      }
      authorAssociation
      title
      body
      createdAt
      updatedAt
      closedAt
      mergedAt
      labels(first: 20) {
        nodes {
          name
        }
      }
      commits(last: 1) {
        nodes {
          commit {
            oid

            statusCheckRollup {
              state
              contexts(first: 20) {
                nodes {
                  __typename
                  ... on CheckRun {
                    name
                    status
                    conclusion
                    startedAt
                    completedAt
                  }
                  ... on StatusContext {
                    context
                    state
                    targetUrl
                  }
                }
              }
            }

            checkSuites(first: 100) {
              nodes {
                app {
                  name
                }
                conclusion
                status
                createdAt
                checkRuns(first: 100) {
                  nodes {
                    name
                    status
                    conclusion
                    startedAt
                    completedAt
                  }
                }
              }
            }

            status {
              contexts {
                context
                state
                targetUrl
              }
            }
          }
        }
      }
      comments(first: 100) {
        totalCount
        nodes {
          body
          author {
            login
            __typename
          }
          authorAssociation
          createdAt
        }
      }
      reviews {
        totalCount
      }
      additions
      deletions
      changedFiles
      userContentEdits(first: 100) {
        totalCount
        nodes {
          diff
          editor {
            login
            __typename
          }
          editedAt
          deletedAt
          deletedBy {
            login
            __typename
          }
        }
      }
    }
  }
}

""").strip()


class PullDetailSpider(scrapy.Spider):
    name = 'pull_detail'
    allowed_domains = ['github.com']
    output_base = config.paths.pull_detail

    def start_requests(self):
        self.output_base.mkdir(parents=True, exist_ok=True)
        pull_numbers: dict[str, list[int]] = json.loads(config.paths.pull_numbers.read_text())
        for repo, numbers in pull_numbers.items():
            owner, name = repo.split('/')
            repo_output_base = self.output_base / f'{owner}${name}'
            repo_output_base.mkdir(exist_ok=True)
            for number in numbers:
                body = json.dumps({
                    'query': query,
                    'variables': {
                        'owner': owner,
                        'name': name,
                        'number': number,
                    }
                })
                yield Request('https://api.github.com/graphql', method='POST', body=body,
                              callback=self.parse_sample_detail, cb_kwargs={'repo': repo, 'number': number})

    def parse(self, response, **kwargs):
        raise NotImplementedError

    def parse_sample_detail(self, response: Response, repo: str, number: int):
        item = json.loads(response.body)
        item = item['data']['repository']['pullRequest']
        out = self.output_base / repo.replace('/', '$') / f'{number}.json'
        out.write_text(json.dumps(item))
