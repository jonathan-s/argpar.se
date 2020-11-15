Title: How to configure github actions for a python package
date: 2020-11-14 20:00
Category: programming
Tags: CI, python, open source, github
Slug: configure-github-actions-for-python-package
Authors: Jonathan Sundqvist
Metadescription: A starting point on how to use github actions for python packages. Explains how to work with matrices and how that integrates with TOX.
status: published
image: images/chain.jpg

This is what a build action for running a test matrix in github actions looks like in python. The yaml file is saved in `.github/workflows/<your_name>.yml`.

```yaml
name: Running unittests

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.6, 3.7, 3.8]
        django: ["2.2", "3.0", "3.1"]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-tests.txt
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Linting
      run: flake8
    - name: Run unittests
      env:
        TOX_ENV: py${{ matrix.python-version}}-django${{ matrix.django }}
      run: |
        tox -e $TOX_ENV
```

In the matrix we define the python versions and in this case also the django versions. `django` in this case will be set as an environment variable.

Further down I've set a TOX env to set exactly how I expect the tox environment variable to be set. So that is what I'm relying `tox` to use in the end.

The python package [tox-gh-actions](https://github.com/ymyzk/tox-gh-actions) may help mapping the python versions with the tox versions. In this case I chose to do it directly with github actions to keep things simpler. One less dependency, one less worry so to speak.

For the full documentation of all the things you can do with github actions there is the [official documentation](https://docs.github.com/en/free-pro-team@latest/actions).
