To run the dev server type in

```bash
make devserver
```

To stop it type in

```
make stopserver
```

Add the following in the in git hooks to publish the website on every commit.

```
make publish && make github
```

When upgrading to pelican 3.7 you need to check the settings for markdown
http://docs.getpelican.com/en/stable/settings.html

You also need to make sure that the markdown plugin is upgraded to 3.something.
These are breaking changes, so it might take some time to fiddle with it.

To install the simple-a theme do the following. It'll symlink the theme
so you can work on it.

`pelican-themes -s ~/projects/argpar.se/themes/simple-a`
