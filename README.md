## build-python-dist

[![.github/workflows/main.yml](https://github.com/OpenAstronomy/build-python-dist/actions/workflows/test_action.yml/badge.svg)](https://github.com/OpenAstronomy/build-python-dist/actions/workflows/test_action.yml)

A GitHub action to build and test a source distribution for
a Python package, and optionally a wheel for pure Python packages.

To build wheels for packages with extensions, you should instead use
[cibuildwheel](https://github.com/pypa/cibuildwheel) which also includes
a GitHub action for convenience.

## Examples

### Build a source distribution with no testing:

```yaml
jobs:
  build_sdist:
    name: Build source distribution
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - id: build
        uses: OpenAstronomy/build-python-dist@v1
```

### Build a source distribution with testing

```yaml
jobs:
  build_sdist:
    name: Build source distribution
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - id: build
        uses: OpenAstronomy/build-python-dist@v1
        with:
          test_extras: test
          test_command: pytest --pyargs test_package
```

The ``test_extras`` option, if specified, should contain a string (e.g. ``test`` or ``test,all``) that will be used to determine which 'extras' should be installed when testing. The ``test_command`` option should contain the full command to use for testing the installed package (this is run from an empty temporary directory).

### Build a source distribution and wheel for a pure-Python package

```yaml
jobs:
  build_sdist_and_wheel:
    name: Build source distribution and pure-Python wheel
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - id: build
        uses: OpenAstronomy/build-python-dist@v1
        with:
          pure_python_wheel: true
          test_extras: test
          test_command: pytest --pyargs test_package
```

## Notes

If you want to use the latest available version of this action instead
of hard-coding a specific version, you can replace
``OpenAstronomy/build-python-dist@v1`` by ``OpenAstronomy/build-python-dist@main``.
