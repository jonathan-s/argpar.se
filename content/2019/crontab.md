Title: Troubleshoot why crontab is not working
date: 2019-05-09 16:00
Category: programming
Tags: crontab, devops, dokku
Slug: troubleshoot-why-crontab-is-not-working
Authors: Jonathan Sundqvist
Metadescription: Why is crontab not working?! What to look out for and how to quickly get crontab run smooth as butter and never skip a beat.
Status: published
internal: #published #crontab #devops #dokku

Crontab is a particularly finicky unix tool. It's not always the easiest to figure out why on earth your scheduled job is not running as it should.

There are a number of things that could go wrong. The very first thing to do is of course to double check that the crontab syntax is doing what you expect it to do. [Crontab guru][1] helps exactly with that.

And as a reminder for what the stars and numbers signify.

```bash
# m   h   dom mon dow   username command
# *   *   *   *   *     dokku    command to be executed
# -   -   -   -   -
# |   |   |   |   |
# |   |   |   |   +----- day of week (0 - 6) (Sunday=0)
# |   |   |   +------- month (1 - 12)
# |   |   +--------- day of month (1 - 31)
# |   +----------- hour (0 - 23)
# +----------- min (0 - 59)
```

The crontab is located at `/etc/crontab`, however **don't** go and edit that file. Instead you can create a specific file related to the cronjob in `/etc/cron.d`. Creating a specific file helps if you are running multiple applications on a host for instance. So you've edited the file and it's still not running.

If you create a new file in `/etc/cron.d`. Make sure that the file does **not** contain any dot or else it won't run. It's also important that it has the correct permissions. The correct permissions for the file should be `-rw-r--r-- root root`. Those permissions are the outcome of the following two commands.

```bash
chown root:root yourcronfile
chmod 644 yourcronfile
```

You might need to restart the cron service for it to pick up the changes you made. You can do that with `sudo service cron restart`.

You can check the cron logs to make sure that the crontab is working correctly. The logs are by default located in `/var/log/syslog`. And running the following grep command will get you all the cron logs.

```bash
grep cron /var/log/syslog
```

Even if the job is logged there, any errors won't show up there. So it's helpful to log those separately. If you add the following snippet at the end of your crontab `>> /var/log/myjob.log 2>&1`, it will do just that. You're bound to thank me later ;).

Your cronjob will fail at some point. A service such as [Dead man's snitch][2] will most certainly help you knowing _when_ it failed. The premise is that you'll send a request to their service and if no request has been sent in the last X minutes, it will notify you that your cronjob likely failed and you need to check it out.

## Dokku interlude

Having your crontab checked in with git is certainly helpful. If you're using dokku there is the helpful plugin `supply-config` that does almost that. There is an [open PR][3] that amends that gap. [Dokku documentation][4] also have some helpful reminders on what to keep in mind when configuring a crontab.

Have you stumbled upon any other ways that crontab could fail?


[1]: https://crontab.guru/
[2]: https://deadmanssnitch.com/cases/89b251ba-1c4a-40a4-88e3-25cc65b908c2/snitches
[3]: https://github.com/dokku-community/dokku-supply-config/pull/7
[4]: http://dokku.viewdocs.io/dokku/deployment/one-off-processes/
