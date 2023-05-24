"""
Script to collect repos list for a user and store data locally

All this script does is get list of repos for a given user from github and store them locally in an sqlite database if path is given.
This script does not support updating list of repos for a user that's already existing in the database.
"""


from contextlib import contextmanager
from collections import namedtuple
from pathlib import Path

import requests
import argparse
import sqlite3


parser = argparse.ArgumentParser(prog='GithubScraper',
                                 description="github scraper to collect repos for provided username then add them to a database")
parser.add_argument("username", help="Username to get public repos list from")
parser.add_argument("-db", "--database", help="database path. when provided, value collected will be stored into the database")
args = parser.parse_args()


# get user details
user_details_url = f"https://api.github.com/users/{args.username}"

user_details = requests.get(user_details_url, timeout=5).json()

user_id = user_details["id"]
user_name = user_details["login"]
user_repos = f"https://api.github.com/users/{args.username}/repos"

# user entry to be stored into Users table
user_entry = [user_id, user_name]

# get repo details
repos = requests.get(user_repos, timeout=10).json()

# contain all repo entries to be stored into Repositories table
repo_entires = []
RepoEntry = namedtuple("RepoEntry", "repo_id repo_name repo_url")

for repo in repos:
    repo_id = repo["id"]
    repo_name = repo["name"]
    repo_url = repo["html_url"]
    
    repo_entry = RepoEntry(repo_id, repo_name, repo_url)
    repo_entires.append(repo_entry)

print("Collected repository data: " + str(len(repos)))


@contextmanager
def get_cursor(db_name) -> sqlite3.Cursor:
    """Get a cursor to the sqllite db within a contex manager"""
    con = sqlite3.connect(db_name)
    curs = con.cursor()
    try:
        yield curs
    finally:
        curs.close()
        con.commit()
        con.close()

if (args.database):
   db_name = args.database
   if not Path(db_name).exists():
      print(f"Database {db_name} does not exist. Exiting")
      exit
   with get_cursor(db_name) as cur:
      cur.execute(f'INSERT INTO Users VALUES({user_id}, "{user_name}")')
      for repo in repo_entires:
         cur.execute(
               'INSERT INTO Repositories VALUES({repo_id}, "{repo_name}", "{repo_url}", {repo_user_id})'.format(repo_id=repo.repo_id, repo_name=repo.repo_name, repo_url=repo.repo_url, repo_user_id=user_id)
         )
   print("Stored data into database successfully")
