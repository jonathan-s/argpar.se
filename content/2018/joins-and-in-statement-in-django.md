Title: Making a custom join in django or foregoing IN
Date: 2018-11-13 23:00
Category: misc
Tags: python, django, sql, performance
Slug: making-custom-join-django-foregoing-in
Authors: Jonathan Sundqvist
Metadescription: Some meta description
Status: draft
internal: #draft #python #django #sql #performance

# NEED PROOF READING

Have you ever thought about how joins are being made in Django? Have you ever felt the urge to make your own custom joins? Have you ever wracked your head around a more complicated query that you know exactly how you would write in SQL, but you can't simply convey it in within the constraints of the Django ORM. That's when you're forced to drop down to pure SQL and use `Model.objects.raw(...)` or `cursor.execute(...)` to accomplish your dirty deeds.

As you write your performant SQL you also make a sigh that you now have to forego the nice abstractions that the Django ORM gives you. Your motto is speed above beauty, but you'd rather have both.

One of the more common, but sadly not particularly performant idioms in Django is using the SQL `IN` statement as in `Model.objects.filter(id__in=[1..100])`. This is generally fine as long as the array of ids are small. When the array grows big the query starts to become slower and slower.

My experience is that if the array approaches 10k entries you'll no longer have a performant query, it'll take a second or two to complete the query.

Another common, but not particularly performant idiom is using `LIMIT 100 OFFSET 200` or in Django parlance `Model.objects.all()[100:200]`. As long as you don't need to page through your entire table that range in the millions it's completely fine to use. However, once you need to execute something in batches and you actually need to do it for your entire table, that's when you'll start to get slow queries. If you're curious of why this is the case I'd recommend that you delve deeper into this [here][1].

You search deep on the web to alleviate your performance woes and you come up with the following answer from the wise crowd at [StackExchange][2]. Ah, a pure breeze, this could solve both of the two problems above, but then no nice django abstractions :(

The answer suggests that we use a temporary table. That should be easy enough to create in pure SQL. Could we join this with our django model? How is it again that django makes joins. `select_related` something something. Not particularly helpful. So let's take a deep dive behind the scenes!

10 years ago this is [how you did it][3]. Django changed a bit since then. To make a join in Django now you'd need to use their Join datastructure which would look something like this. You can find the code for this in the [django repo][4].

```python
from django.db.models.sql.datastructures import Join
from django.db.models.sql.constants import INNER, LOUTER

qs = Model.objects.all()
connection = Join(
    table_name=JoiningTable._meta.db_table,
    parent_alias=qs.query.get_initial_alias(),
    table_alias=None,
    join_type=INNER,
    join_field=Model.joining_set.field,
    nullable=False
)
qs.query.join(connection, reuse=None)
```

The join datastructure will effectively generate the following SQL.

```SQL
INNER JOIN "joining_table" ON ("model"."id" = "joining_table"."model_id")
```

And once you use `query.join(connection)` it will create the correct query for you. Since the `Join` datastructure is a bit opaque, let's break it down a little.

The `table_name` is a normal string which needs to be a table in the database. Then following `parent_alias` is the string of the table that should be joined together. `table_alias` may be `None` without causing any issues.

The join type may either be one of the two django constants. Which corresponds to `INNER JOIN` or `LEFT OUTER JOIN`. The tricky bit here is that if `nullable` is `True` when you use the join function it will always default to make a `LEFT OUTER JOIN` rather than an `INNER JOIN`.

Going back to the answer at StackExchange we are bit closer to achieving a join with a temporary table. The leap of thought that we need to make here is that even a temporary table may be allowed to have a model. The key here is to make a model that is not managed by django and has the table name defined by us.

This is what the code would look like in the end.

```python

sql = '''
    DROP TABLE IF EXISTS temp_stuff;
    DROP INDEX IF EXISTS temp_stuff_id;
    CREATE TEMPORARY TABLE temp_stuff AS {query};
    CREATE INDEX temp_stuff_id ON temp_stuff (id);
'''.format(query=str(query))

with connection.cursor() as cursor:
    cursor.execute(sql)

class TempModel(models.Model):
    temp_key = models.ForeignKey(
        'Model',
        on_delete=models.DO_NOTHING,
        db_column='id'
    )

    class Meta:
        managed = False
        db_table = 'temp_stuff'
```

Now that we have model to the temporary table and a corresponding foreign key we can use the `Join` datastructure to make a join with a table.

Wouldn't it be nice if we could do something like this.

```python
qs = Model.objects.filter(filter_criteria='my_criteria').join()
```

The code above would create a temporary table of the first part of the queryset, the part before `.join()`. It would join that temporary table with the table for `Model` accomplishing the filtered criteria.

Similarly if we could add another queryset that is related to the model in the following way.

```python
user_qs = User.objects.filter(some_criteria='criteria')
qs = Model.objects.filter().join(qs=user_qs)
```

So in this case we would only get Model objects that fulfill the given criteria.

This looks just like the abstractions that we were looking for, and it also solves our earlier performance woes. The following code will always perform the same, there is admittedly still some paging involved, but it's limited to the ids, so the impact is minimized.

```python
qs = Model.objects.all()[1:10000]
qs.join()
```

The same can be applied when using django's `__in` and improve the performance.

```python
user_qs = User.objects.filter(...)
qs = Model.objects.filter(user_id__in=[q.id for q in user_qs])

# vs the faster variant

user_qs = User.objects.filter(...)
qs = Model.objects.all().join(qs)
```

So enough teasing. Here is [the gist][5] to the custom QuerySet that can accomplish this. If you're keen on reading similar tips and deep dives, sign up to my newsletter and get reminded once a new post is ready.

My next post will be about a 10x boost in performance and some strategies on how to find where to make improvements in the code.

[1]: https://use-the-index-luke.com/no-offset
[2]: https://dba.stackexchange.com/a/91254/132631
[3]: https://www.caktusgroup.com/blog/2009/09/28/custom-joins-with-djangos-queryjoin/
[4]: https://github.com/django/django/blob/master/django/db/models/sql/datastructures.py
[5]: https://gist.github.com/jonathan-s/c5cddffe73c573f11720df4094351ea4
