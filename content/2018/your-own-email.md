Title: Getting an email with your own domain
Date: 2018-07-04 23:27
Category: misc
Tags: tutorial, email
Authors: Jonathan Sundqvist
Metadescription: This guide walks through all the steps to set up your own email for your own domain. Registering your domain -> Configuring the account -> Using with gmail
Status: published
internal: #published #email #tutorial

There are many compelling reasons to have an email address with your own domain. My personal motivation is that you become a lot more independant from the tech giants. I've been using gmail for many years and stories  where google has [completely](goog1) [locked](goog2) [down](goog3) their google account are particularly frightening.

So here we are, taking the first step in becoming independant from tech giants and be among the cool kids that have their own domain. Let me tell you a secret, getting your own domain is neither particularly difficult nor expensive.

So let's get started!

## Registering your domain

There are many places where you can register a domain and I'm going to recommend [gandi](gandi). They've got helpful support, you get storage space for your email included in the domain and they've got an excellent selection of all the new fancy domains that you can get. If the domain were available you could get an email like `Iam@sleeping.today`, lot's of fun [picking out](gandi_search) a domain for yourself!

So once you've decided what domain you want and completed the checkout process at Gandi. You now own your own domain! That wasn't that difficult. So let's proceed to make sure that you have an email that you can use with your domain.

### Configuring your email

Once you're logged in you can click on "Domains" and then continue to click on the domain that you registered. Here you can see that automatic renewal is on by default. You'll definitely want that otherwise your email address would stop working after a year which is no good.

![Create your email at gandi]({filename}/images/your-own-email/create-email-address.png)

In the menu to the left you can select "Email", it'll then show you the screen you see above. Clicking on creating a gandi mail will let you create a new email address for yourself. The password will be used for logging into the [webmail](gandimail) that gandi has or for connecting the email to an email client such as Thunderbird.

Alias means that these combinations also goes to the email that you're registering. In other words, if you create the email email@world.com and you put the alias, "hello" and "test" as alias. The emails "email@world.com", "hello@world.com" and "test@world.com" will all be valid.

You're probably already using some other email. So if you want to continue doing that for a while you can forward the email from your new address to your old email address. Make sure that you also forward email to the address that you just created. Otherwise it'll skip the gandi inbox completely, the goal is to keep your email there after all.

Now is the time to ask a friend of yours to send an email to your newly created email to make sure that it works and that forwarding works as expected if you set that up!

Congrats! You now have your own domain with an email that you can use! Go forth and email your friends about this article and encourage them to create their own email address ;).

### SPF records or spam prevention

There are a couple of more things that you can do. Right now if you try to send an email to a gmail user, it'll look somewhat suspicious, as in in Gmail warns the user it can't verify whether the email was sent by you or someone else.

That's because gmail can't really tell right now whether the person who sent this is the person who actually owns the email address. You can remedy this by creating something called a [SPF record](spfwiki). In short, it's as an email validation policy which is designed to detect and block spoofing. It will prevent spammers form using your domain to send unauthorized emails.

The [SPF record](spfgandi) for gandi.net looks like this:

```
 @ 10800 IN TXT "v=spf1 include:_mailcust.gandi.net ~all"
```

To activate the SPF record. Go to `DNS Records` which you can find among the options for your particular domain. Once there add a new record. You'll arrive to a form where you can set things up. The type should be TXT. The rest of the options should be filled in like this to generate the SPF record above.

```
TTL: 10800 (seconds)
Name: @
Text value: v=spf1 include:_mailcust.gandi.net ~all
```

If you scroll down you can view all the DNS records, and you'll find that it looks like the SPF record in the stated above.


## Use your new email with Gmail

If you are a gmail user, and still hesitant to give up gmail just yet, but would still want to use the email that you just created. That's entirely possible, presumably you've already chosen to forward your email to that email address of yours. The next step is being able to send email from the email address you created from within gmail.

Go into the gmail settings. At the top there are several tabs, the tab you should be looking for is "Accounts and Import".

Right there it says that you `send email as`. If you click the link to add a new email address there will be a popup that asks you to fill in the following fields. The port should be 587.

```
SMTP server: mail.gandi.net
username: youremail@yourdomain.com
password: the password for your email
```

Once that is done gmail will send an email to that address to verify that it is yours. Click the link in the email and you can now send email using your newly created email address!

Then there is also the option of doing the opposite, forwarding email from your gmail account to your new email. Which perhaps is a better option in case you're trying to wean yourself off gmail.

Happy emailing, and send me an email if there is anything that I should clarify :)

[goog1]: https://twitter.com/search?q=google%2Baccount%2Bdisabled&src=typd
[goog2]: https://news.ycombinator.com/item?id=4013799
[goog3]: https://shkspr.mobi/blog/2015/11/the-day-google-deleted-me/
[gandi]: https://www.gandi.net
[gandi_search]: https://shop.gandi.net/en/domain/suggest
[gandimail]: https://webmail.gandi.net/
[spfwiki]: https://en.wikipedia.org/wiki/Sender_Policy_Framework
[spfgandi]: https://wiki.gandi.net/en/dns/zone/spf-record
