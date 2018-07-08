# -*- coding: utf-8 -*-
"""
Post Statistics
========================

This plugin calculates various statistics about a post and stores them in an
article.stats dictionary:

wc: how many words
read_mins: how many minutes to read this article, based on 250 wpm
(http://en.wikipedia.org/wiki/Words_per_minute#Reading_and_comprehension)
word_counts: frequency count of all the words in the article; can be used
for tag/word clouds/

"""

from pelican import signals
from bs4 import BeautifulSoup
import re
from collections import Counter


def calculate_stats(instance):

    if instance._content is not None:
        stats = {}
        content = instance._content

        # How fast do average people read?
        WPM = 180

        # Use BeautifulSoup to get readable/visible text
        raw_text = BeautifulSoup(content, 'html.parser').getText()

        # Process the text to remove entities
        entities = r'\&\#?.+?;'
        raw_text = raw_text.replace('&nbsp;', ' ')
        raw_text = re.sub(entities, '', raw_text)

        # Process the text to remove punctuation
        drop = u'.,?!@#$%^&*()_+-=\|/[]{}`~:;\'\"‘’—…“”'
        raw_text = raw_text.translate(dict((ord(c), u'') for c in drop))

        # Count the words in the text
        words = raw_text.lower().split()
        word_count = Counter(words)

        # Return the stats
        stats['word_counts'] = word_count
        stats['wc'] = sum(word_count.values())

        # Calulate how long it'll take to read, rounding up
        stats['read_mins'] = (stats['wc'] + WPM - 1) // WPM
        if stats['read_mins'] == 0:
            stats['read_mins'] = 1

        instance.stats = stats


def register():
    signals.content_object_init.connect(calculate_stats)
