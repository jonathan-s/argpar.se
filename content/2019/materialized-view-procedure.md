Title: Creating a materialized view with SQL procedures
date: 2019-12-04 16:00
Category: programming
Tags: #SQL, #mysql
Slug: creating-a-materialized-view
Authors: Jonathan Sundqvist
Metadescription:
Status: published
image: images/mysql-procedure.png
internal: #published

In newer versions of MySQL you can create materialized views directly without any SQL procedures. However I recently had to work with a database that used MySQL 5.6 and in that version it's not possible to create materialized views.

To give some context of what the problem at hand was. There was a huge table with around 1.3 billion entries. In this table there were URLs that had the flag `green` either set as true or false. The URLs are not unique. Depending on the date a URL could be flagged either as `green` or not.

What I needed was to get the distinct set of all URLs flagged as `green`. If a URL got flagged as `green` and then at a later date got unflagged as `green` it should not show up in the final set of results.

There isn't any particularly elegant way of creating a performant query to get that data. So I landed in creating a stored procedure to solve the problem.

This stored procedure was then later used to backfill the table called `green_presenting`.

Let's walk through what's actually happening in this stored procedure.


```sql
delimiter //
CREATE PROCEDURE insert_urls(IN url VarChar(255), IN green TinyInt(2), IN id_hp INT(11), IN datum datetime)
BEGIN
    DECLARE hostname VARCHAR(255);
    DECLARE hostwebsite VARCHAR(255);
    DECLARE hostpartner VARCHAR(255);

    IF (green = 0) THEN
        DELETE FROM green_presenting WHERE url = url;
    ELSE
        SELECT name, partner, website INTO hostname, hostpartner, hostwebsite
        FROM hostingproviders WHERE id = id_hp;

        INSERT INTO green_presenting
        (`modified`, `green`, `hosted_by`, `hosted_by_id`, `hosted_by_website`, `partner`, `url`)
        VALUES (datum, green, hostname, id_hp, hostwebsite, hostpartner, url)
        ON DUPLICATE KEY UPDATE
        modified = datum;
    END IF;
END
//
delimiter ;
```

Before we start with the signature of the procedure. The very first we need to do is to change the delimiter, from using `;` to `//` that way it won't parse new `;` as the end of a statement when we create the procedure.

Let's continue with the signature of the procedure.

```sql
CREATE PROCEDURE insert_urls(IN url VarChar(255), IN green TinyInt(2), in id_hp INT(11), IN datum datetime)
BEGIN
    ...
END
```

The way to define paramaters is to use the keyword `IN` followed by the parameter name and last the type of the parameter. You can also use the keyword `OUT` or `INOUT`. If you don't need to change the parameter in the procedure and have that changed propagated in the database there is no need to use anything else than `IN`.

A stored procedure always need to begin with `BEGIN` and end with `END`

```sql
DECLARE hostname VARCHAR(255);
```

This is how a new variable is created. Which you can then assign something to.

```sql
IF (green = 0) THEN
    ...
ELSE
    ...
END IF;
```

The above is the outline of what an IF statement looks like. Make sure not to forget `THEN` :).

```sql
SELECT name, partner, website INTO hostname, hostpartner, hostwebsite
FROM hostingproviders WHERE id = id_hp;
```

This is where we assign the values to the variables we created earlier. It's done with `INTO` keyword.

That's it!

The above procedure just takes one entry. Since I also needed to backfill all data. I had to create a new procedure that iterates through all entries of the table.

What's noteworthy here is how we create a cursor and loop through it. Otherwise it's pretty much self-explanatory.


```sql
delimiter //
CREATE PROCEDURE backfill()
BEGIN
  DECLARE done INT DEFAULT FALSE;

  DECLARE gdatum DATETIME;
  DECLARE ggreen TINYINT(2);
  DECLARE gid_hp INT(11);
  DECLARE gurl VARCHAR(255);
  DECLARE cur CURSOR FOR SELECT datum, green, id_hp, url FROM greencheck where id_hp > 0;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  OPEN cur;

  read_loop: LOOP
    FETCH cur INTO gdatum, ggreen, gid_hp, gurl;
    IF done THEN
      LEAVE read_loop;
    END IF;
    call insert_presenting(gurl, ggreen, gid_hp, gdatum);
  END LOOP read_loop;

  CLOSE cur;
END;
//
delimiter ;
```

The last missing bit would be to create a trigger, that calls the procedure `insert_urls`. After that we more or less have everything what a materialized view usually does.
