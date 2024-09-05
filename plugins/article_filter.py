"""
The most basic way to filter out articles from the index page.

Ideally it would be nice if we could come up with a more elaborate filtering
mechanism, that can be defined in settings.

ARTICLE_FILTER is the setting name.

The structure.
{
    "index_articles": {"exclude": ["photography"]}
}

Possibly take inspiration from this.
https://github.com/pelican-plugins/feed-filter
"""

from urllib.parse import urlparse

from jinja2 import Markup
from pelican import signals
from pelican.utils import set_date_tzinfo
from pelican.writers import Writer


def load_template(generator):
    """Load 'feed' template and store its macros in CustomWriter."""
    try:
        tpl_macros = generator.get_template("feed").make_module(generator.context)
        CustomWriter.macros = tpl_macros
    except Exception:
        pass


class CustomWriter(Writer):
    """
    The functionality of this writer does two things.
    - Allowing you to customize feeds using template macros.
    - Filter out the "photography" category from index.html
    """
    macros = None  # Template macros

    def _add_item_to_the_feed(self, feed, item):
        if self.macros is None:
            # Fall back to default behaviour if macros was not loaded
            return Writer._add_item_to_the_feed(self, feed, item)

        title = Markup(item.title).striptags()
        link = '%s/%s' % (self.site_url, item.url)
        content = item.get_content(self.site_url)

        content = item.get_content(self.site_url)
        description = item.summary
        if description == content:
            description = None

        feed.add_item(
            title=self.macros.title(item) if hasattr(self.macros, 'title') else title,
            link=self.macros.link(item).strip() if hasattr(self.macros, 'link') else link,
            unique_id='tag:{},{}:{}'.format(
                urlparse(link).netloc,
                item.date.date(),
                urlparse(link).path.lstrip('/')
            ),
            content=self.macros.description(item) if hasattr(self.macros, 'description') else content,
            description=description,
            categories=item.tags if hasattr(item, 'tags') else None,
            author_name=getattr(item, 'author', ''),
            pubdate=set_date_tzinfo(
                item.modified if hasattr(item, 'modified') else item.date,
                self.settings.get('TIMEZONE', None)
            )
        )

    def write_file(
        self,
        name,
        template,
        context,
        relative_urls=False,
        paginated=None,
        template_name=None,
        override_output=False,
        url=None,
        **kwargs
    ):
        articles = kwargs.get("articles")
        page_name = kwargs.get("page_name")
        if page_name == 'index':
            articles = [a for a in articles if not a.category == 'photography']
            kwargs["articles"] = articles

        super().write_file(
            name=name,
            template=template,
            context=context,
            relative_urls=relative_urls,
            paginated=paginated,
            template_name=template_name,
            override_output=override_output,
            url=url,
            **kwargs
        )


def get_writer(sender):
    return CustomWriter


def register():
    """Register the new plugin"""
    signals.article_generator_init.connect(load_template)
    signals.get_writer.connect(get_writer)
