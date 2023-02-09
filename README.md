# learning-datastructures

This repository contains a list of implementation of datastructures for learning purposes. They can be implemented in any language and any format (scripts, Jupyter notebook, etc)

## Python

### Setup

You can setup an environement by using the poetry package manager.

```bash
poetry install
```

```bash
poetry shell
```

### Launching tests

Inside the python directory, you can use pytest with the cov plugin. Using directly pytest might use your system pytest installation which might not be in the correct virtual env.

```bash
python -m pytest --cov-report xml:coverage.xml --cov-report term --cov .
```

Coverage is available as both a coverage.xml file and in the terminal. You can install VSCode Gutter to inspect which line has been covered.