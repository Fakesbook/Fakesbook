#!/bin/bash

pyinstaller --add-data ./templates:templates --add-data ./static:static --add-data ./db:db --hidden-import _cffi_backend --onefile fakesbook.py
