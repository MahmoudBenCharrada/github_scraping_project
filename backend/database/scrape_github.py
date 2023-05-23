from bs4 import BeautifulSoup

import requests
import argparse

parser = argparse.ArgumentParser(prog='GithubScraper',
                                 description="github scraper to collect repos for provided username then add them to a database")
parser.add_argument("username", help="Username to get public repos list from")
parser.add_argument("-db", "--database", help="database path. when provided, value collected will be stored into the database")
args = parser.parse_args()

template_url = "https://github.com/{username}?tab=repositories"
github_url = template_url.format(username = args.username)

response = requests.get(github_url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

for repo in content.find_all(itemprop="name codeRepository"):
   # print(vars(repo))
   print(repo.contents[0].strip())
   break

# test = BeautifulSoup('<a href="/makerGeek/makergeek.github.io" itemprop="name codeRepository">makergeek.github.io</a>', 'html.parser')
# print(test.a.contents[0])

