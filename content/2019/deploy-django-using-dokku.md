Title: Deploying Django using Dokku
Date: 2019-05-1 20:00
Category: programming
Tags: django, devops, dokku, python
Slug: deploy-django-using-dokku
Authors: Jonathan Sundqvist
Metadescription: Make your first steps in devops as you learn how to debug and deploy Django using dokku on a vps of your choice.
Status: published
internal: #published #django #devops #dokku #python

## I want to see my site on the web!

That's what I've thought many times, but the thought of deploying things often seems prohibitively complex (unless you go with heroku, which hides most of the complexities at the expense of your wallet). The world of operations is vast and it's sometimes difficult to get a grasp of where to start to achieve what you want; to deploy the site you built.

So this guide should provide that foot in the door while simultanously feeling rewarding with achieving something in the very end, because spending hours without seeing any sort of result is no fun. Let's get started!

## Getting started with Dokku

Unless you already have a server where you can develop your project I would suggest that you give [scaleway][1] a try. Once you've installed something like debian on your server. The very first thing to do is to configure [fail2ban][2]. If you don't your server is bound to be hacked in no time, I learnt the hard way on a digital ocean droplet. You'd be surprised how often someone tries to login to your server.

Now that you're ready to install Dokku follow the [official instructions][3]. Once you've executed the bash command for the latest version, set up your _public_ SSH key and added an [A record][5] for your server IP address you are ready to deploy your application.

## Configuring Dokku for deployment

If you don't yet have a Django project that you would like to deploy I would suggest that you use the following template which [dockerizes django][4]. It's a good starting point for any django project and already has sane defaults.

Once you've executed the following commands you'll be able to run django locally. This is also what I'll be using as a base for deploying Django using Dokku.

```bash
pip3 install cookiecutter
cookiecutter https://gitlab.com/thiras/cookiecutter-docker-django
```

SSH into your server and run the following commands

```bash
# this is how you will refer to your app when using dokku
dokku apps:create your-django-app

# install the postgres plugin to be able to use postgres with dokku
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git

# creates a database for your app.
dokku postgres:create djangodb

# link the above database to your app
dokku postgres:link djangodb your-django-app

# configure which domain you'll be using for your app
# I'd recommend using a fully qualified domain
domains:add your-django-app subdomain.yourdomain.com
```

If you're using the django app from the cookiecutter template you'll notice that it doesn't contain any `Procfile`. Dokku does require a Procfile. So go ahead and add and commit a file named `Procfile` containing:

> web: gunicorn appname.wsgi:application --log-file

You're now set and can try to deploy your django app!

## Debugging deployment issues

Dokku promises that you'll be able to deploy using git. Isn't that a treat. In the [dokku documentation][6] it details how you should add the remote to git. These commands are

```bash
# if you're using a subdomain
git remote add dokku dokku@yourdomain.com:subdomain

# if you're deploying to the root domain
git remote add dokku dokku@dokku.me:dokku.me

git push dokku master
```

**Problem**: You fail to deploy. Because the host isn't recognized.

```bash
fatal: 'yourapp' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

**Solution**: If you're facing this problem, perhaps because you're using a subdomain you can change the remote to contain the your public server IP instead. So the remote would look something like this instead `dokku@41.151.12.3:subdomain`

**Problem**: It doesn't find a `Procfile` even though you added one.

**Solution**: You might have file called `.dockerignore`. If procfile is named there the container won't pick up your procfile. Removing that should fix that issue.

We try to deploy again, and now it should actually deploy successfully.

**Problem**: While it successfully deploys the only thing you see is 400 Bad request. When you browse your site. How odd!

**Solution**: In `settings.py` you need to change `ALLOWED_HOSTS` to your own domain. Once you've done this, you can now deploy your site again and that particular problem will go away.

**Problem**: You try to view the site. All static files such as CSS files returns 404. The site looks horrendous.

**Solution**: The development server serves static files for you. The gunicorn server does not. There is a management command `collectstatic` that you need to run every time on deployment.

Create a file called `app.json`. There you can define commands that should run before deployment. You can read more about it in the [dokku documentation][7]

```json
{
  "scripts": {
    "dokku": {
      "predeploy": "python manage.py collectstatic --noinput"
    }
  }
}
```

This will move your static files to the static folder you defined in [django settings][8].

If you try to deploy again, thinking it is enough, it is not. These files need to be served as well. Nginx normally serves these files. So let's make that happen!

Every deployment [Dokku generates][9] an `nginx.conf` file in `~home/dokku/appname`. So we can't really edit that file. However if we take a look at the file it contains the following:

```bash
include /home/dokku/appname/nginx.conf.d/\*.conf;
```

So if we place any conf file in the folder `nginx.conf.d` it should work. We'll place a file `static.conf` containing the following:

```bash
location /static {
    autoindex on;
    alias   /home/dokku/appname/static;
}
```

However the above path is not where our static files are generated. They are generated inside our container. Also wouldn't it be nice if our `static.conf` were in source control. You can accomplish that with the dokku plugin [`supply-config`][10].

In other words, we need a way to access the static files generated in our container. We can do that by mounting a volume where the static files are located.

```bash
dokku docker-options:add your-django-app deploy "-v /home/dokku/appname/static:/app/appname/static"
```

The path after the colon is where your staticfiles are located after you run the command to collect your static files, and the path before the colon is the same path as in `static.conf`.

When you deploy this time, even the static files should work. I'll let you in on a secret though. Instead of fiddling with nginx you could also use the django package [whitenoise][11] which is probably a more appropriate solution in this case.

But if I told you directly you wouldn't have learnt about all the other Nginx configuration which might be useful for another day.

As a complementary reading, I'd recommend checking out this guide on [deploying django using Dokku][12]

[1]: https://www.scaleway.com/en/
[2]: https://www.scaleway.com/en/docs/protect-server-fail2ban/
[3]: http://dokku.viewdocs.io/dokku/getting-started/installation/#installing-the-latest-stable-version
[4]: https://gitlab.com/thiras/cookiecutter-docker-django
[5]: https://my.bluehost.com/hosting/help/whats-an-a-record
[6]: http://dokku.viewdocs.io/dokku/deployment/application-deployment/#deploying-to-subdomains
[7]: http://dokku.viewdocs.io/dokku/advanced-usage/deployment-tasks/#deployment-tasks
[8]: https://docs.djangoproject.com/en/2.2/howto/static-files/#managing-static-files-e-g-images-javascript-css
[9]: http://dokku.viewdocs.io/dokku/configuration/nginx/#customizing-via-configuration-files-included-by-the-default-tem
[10]: https://github.com/dokku-community/dokku-supply-config
[11]: http://whitenoise.evans.io/en/stable/
[12]: https://www.stavros.io/posts/deploy-django-dokku/
