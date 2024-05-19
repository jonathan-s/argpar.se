To run the dev server type in

```bash
make devserver
```

## Changing CSS styles interactively.

Using the five server vs code plugin. Start the server, and go to

```
http://localhost:8080/output
```

To install the simple-a theme do the following. It'll symlink the theme
so you can work on it.

`pelican-themes -s ~/projects/argpar.se/themes/simple-a`

Generating pygments css

```bash
pygmentize -S monokai -f html -a .highlight > pygment.css
```

