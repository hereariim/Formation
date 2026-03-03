# Deploying the Plugin to PyPI and Napari Hub

This section explains how to publish your napari plugin on PyPI so that it automatically becomes available on the Napari Hub.

Napari Hub indexes plugins directly from PyPI. Once your package is published, it will be detected and listed automatically.

## Build the package

Install the build tool:
```
pip install build
```
Then build the package:
```
python -m build
```
This will generate:
```
dist/
   formation-0.0.1.tar.gz
   formation-0.0.1-py3-none-any.whl
```

## Upload to PyPI

Install the PyPI upload tool:
```
pip install twine
```
Upload the package:
```
twine upload dist/*
```
You will be prompted for your PyPI username and password.

Once uploaded, your plugin becomes installable with:
```
pip install formation
```