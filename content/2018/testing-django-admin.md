Title: Testing Django admin
Date: 2018-07-08 14:10
Category: programming
Tags: python, django, programming, django-admin
Authors: Jonathan Sundqvist
Status: published

It's not exactly crystal clear how to test the functionalities that you add to django admin without diving into the source code of Django. So here are a few tips and snippets that'll help.

## Testing ModelAdmin methods

When you come to the point that you need to override any of the [ModelAdmin methods](admin_methods) how do you go about testing them? You could do it through the `client` and make a POST request to the view that saves the model, but that is a lot of work.

Most of the ModelAdmin methods require a request. So if we mock that out, we can quite easily test the method without taking much else into account.

```python
from django.contrib.admin.sites import AdminSite
from django.test import TestCase


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()

class MyAdminTest(Testcase):

    def setUp(self):
        site = AdminSite()
        self.admin = MyAdmin(MyModel, site)

    def test_delete_model(self):
        obj = MyModel.objects.get(pk=1)
        self.admin.delete_model(request, obj)

        deleted = MyModel.objects.filter(pk=1).first()
        self.assertEqual(deleted, None)
```

This way you don't need to focus much at all on the request argument and can focus on asserting on any side effects or other functionalities that your modified ModelAdmin methods does.

## Testing a file upload in Django admin

If you're about to test an admin view where you upload some file, you'll need to use the test `Client` that django has in the `TestCase` class. Django has [some documentation](admin_post) around how that works.

The post method takes a path and a dictionary of DATA arguments. If one of these arguments is a file like object you'll be able to access it as `request.FILES` in the response.

To test your file upload it would look like this.

```python
from django.test import TestCase
from io import BytesIO  # you could use StringIO as well

class FileTest(TestCase):

    def setUp(self):
        # the file in this case is modeled as a simple csv
        self.file = BytesIO(b'model_id\n1\n2\n')

    def test_file_upload(self):
        # each admin url consits of the following three things
        # the app name, the name of the model and the name of the view
        url = reverse('admin:appname_modelname_viewname')
        resp = self.client(url, {'form_filefield': self.file})

        # Here you'll want to do extra assertions, ie are you
        # saving the file in a model, streaming something back in
        # streamingresponse or doing something else.
        self.assertEqual(resp.status_code, 200)
```

The file like object you also be a file handler as in this example.

```python
with open('some_file.csv') as f:
    self.client.post(url, {'form_filefield': f})
```

Though I find that if you just want to test something not too complex it's easier to use either `BytesIO` or `StringIO` and construct the file content in place rather than having file fixtures.

Do you find that there are other tricky bits testing the django admin, [tweet me](argparse) and I'll add it!

[admin_methods]: https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#modeladmin-methods
[admin_post]: https://docs.djangoproject.com/en/2.0/topics/testing/tools/#django.test.Client.post
[argparse]: https://www.twitter.com/argparse
