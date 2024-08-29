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

from pelican import signals
from pelican.writers import Writer


class ExcludeWriter(Writer):

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
    return ExcludeWriter


def register():
    """Register the new plugin"""
    signals.get_writer.connect(get_writer)
