#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import json

DEVELOPMENT = True

AUTHOR = 'Jonathan Sundqvist'
SITENAME = 'Argparse'
SITEURL = ''
SLUGIFY_SOURCE = 'title'
IGNORE_FILES = ['template.md']
THEME = 'themes/simple-a'
WITH_FUTURE_DATES = False
LOAD_CONTENT_CACHE = False        # if you are developing a theme turn these off.
AUTORELOAD_IGNORE_CACHE = False   # if you are developing a theme turn these off.

PATH = 'content'
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'article_filter',
    'post_stats',
    'obsidian'
]

TIMEZONE = 'Europe/Berlin'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# URL structure on site
ARTICLE_URL = 'posts/{category}/{slug}'
ARTICLE_SAVE_AS = 'posts/{category}/{slug}/index.html'

DRAFT_URL = 'drafts/{slug}'
DRAFT_SAVE_AS = 'drafts/{slug}/index.html'

TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}/index.html'

# authors won't be generated as it uses '' for save_as
AUTHOR_URL = 'author/{slug}'
AUTHOR_SAVE_AS = ''

CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

SITEMAP_SAVE_AS = 'sitemap.xml'
STATIC_PATHS = [
    'images',
    'extra/robots.txt',
    'extra/favicon.ico',
    'extra/CNAME',
    'extra/.gitignore'
]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
    'extra/.gitignore': {'path': '.gitignore'},
    'content/pages/404.md': {'path': '404.html'}  # not sure this will work
}

# Pagination and stuff
DEFAULT_LANG = 'en'
DEFAULT_CATEGORY = 'misc'
DEFAULT_PAGINATION = 18
DEFAULT_ORPHANS = 1
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

DELETE_OUTPUT_DIRECTORY = True

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# ########## THEME RELATED ############


def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


def jsonarray(value):
    return json.dumps([str(v) for v in value])


JINJA_FILTERS = {
    'datetimeformat': datetimeformat,
    'jsonarray': jsonarray
}
TWITTER_USERNAME = '@argparse'
EMAIL = 'jonathan@argpar.se'
