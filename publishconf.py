#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://www.argpar.se'

RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = ('.gitignore', 'CNAME')

DRAFT_URL = 'drafts/{slug}'
DRAFT_SAVE_AS = ''

# Following items are often useful when publishing

DISQUS_SITENAME = "argparse"
GOOGLE_ANALYTICS = "UA-9947703-3"
