Title: Permissions for Proxy models
Date: 2018-07-16 19:00
Category: programming
Tags: django, python, django-admin, programming
Authors: Jonathan Sundqvist
Status: published

Proxy models are pretty useful if you want to create a new customized view in django admin. Let's say that you have a normal model and that you need a specific view where you can do bulk uploads. Creating a proxy model from your normal model and then using the django admin on top of your new proxy model gets you a clean separation of the regular list view and your custom django admin view.

So you've created your custom django view and you want that appropriately permissioned like the normal models are. That is, it'll have the following three permissions

* add permission
* delete permission
* change permission

To your surprise when creating and migrating your proxy model it doesn't create any permissions at all for you. It's quite an annoyance unless you know about it. There has been a [long-standing ticket][1] open for exactly this.

When the migration of your proxy model has been created, you can add the following code to the migration to get the appropriate permissions as you'd expect it to have. Then use `migrations.RunPython(create_permissions)` as an added operation. As you can see in the [django documentation][3]

```python

from django.contrib.auth.management import _get_all_permissions

def create_permissions(apps, schema_editor):
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission

    YourModel = apps.get_model('app_label', 'ModelName')
    opts = YourModel._meta
    content_type, created = ContentType.objects.get_or_create(
        app_label=opts.app_label,
        model=opts.object_name.lower(),

    )

    for codename, name in _get_all_permissions(opts):
        p, created = Permission.objects.get_or_create(
            codename=codename,
            content_type=content_type,
            defaults={'name': name}
        )
```

There is also a [gist][2] around describing how you could add a post-migrate signal so that proxy models always get their appropriate permissions.

[1]: https://code.djangoproject.com/ticket/11154
[2]: https://gist.github.com/magopian/7543724
[3]: https://docs.djangoproject.com/en/2.0/topics/migrations/#data-migrations
