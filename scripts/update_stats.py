#!/usr/bin/env python3
"""Refresh local GitHub statistics SVG from GitHub's own public REST API.

Dependencies: Python 3 standard library; uses GITHUB_TOKEN when set.
The generated SVG does not make requests or load any external assets.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from render_profile import ASSETS, stats_card, write_if_changed


def github_json(endpoint: str, params: dict | None = None) -> dict | list:
    url = 'https://api.github.com' + endpoint
    if params:
        url += '?' + urlencode(params)
    token = os.environ.get('GITHUB_TOKEN', '').strip()
    headers = {
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'dil3mm4-profile-local-stats/1.0',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        with urlopen(Request(url,headers=headers),timeout=25) as response:
            return json.load(response)
    except HTTPError as exc:
        detail=exc.read(400).decode('utf-8',errors='replace')
        raise RuntimeError(f'GitHub API returned HTTP {exc.code} for {endpoint}: {detail}') from exc
    except URLError as exc:
        raise RuntimeError(f'GitHub API unavailable: {exc}') from exc


def search_count(route: str, query: str) -> int:
    payload=github_json(route,{'q':query,'per_page':1})
    if not isinstance(payload,dict) or not isinstance(payload.get('total_count'),int):
        raise RuntimeError(f'Invalid GitHub search response for {query!r}')
    # GitHub search returns total_count even when only one match is requested.
    return payload['total_count']


def public_repos(login: str) -> tuple[int,int]:
    count=0
    stars=0
    page=1
    while True:
        repos=github_json(f'/users/{login}/repos',{'type':'owner','sort':'full_name','per_page':100,'page':page})
        if not isinstance(repos,list):
            raise RuntimeError('Invalid GitHub repository list response')
        # The owned list can contain forks; count all owned public repositories.
        for repo in repos:
            if not repo.get('private',False):
                count+=1
                stars+=repo.get('stargazers_count',0)
        if len(repos)<100:
            break
        page+=1
        if page>50:
            raise RuntimeError('Unexpectedly large repository pagination')
    return count,stars


def gather(login: str) -> dict:
    repos,stars=public_repos(login)
    # Search counts are public, all-time and search-indexed; they don't include private work.
    commits=search_count('/search/commits',f'author:{login}')
    authored=search_count('/search/issues',f'is:pr author:{login}')
    merged=search_count('/search/issues',f'is:pr author:{login} is:merged')
    reviews=search_count('/search/issues',f'is:pr reviewed-by:{login}')
    merge_percent=round(100*merged/authored) if authored else 0
    return dict(commits=commits,repositories=repos,stars=stars,
                merge_percent=merge_percent,reviews=reviews,
                updated_utc=datetime.now(timezone.utc).strftime('%Y-%m-%d'))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--login',default='dil3mm4',help='GitHub username')
    args=parser.parse_args()
    try:
        data=gather(args.login)
    except Exception as exc:
        print(f'Stats update skipped: {exc}',file=sys.stderr)
        sys.exit(1)   # Never overwrite a valid SVG with missing values.
    if write_if_changed(ASSETS/'github-stats.svg',stats_card(data)):
        print('Updated assets/github-stats.svg:',data)
    else:
        print('GitHub stats unchanged')


if __name__=='__main__':
    main()
