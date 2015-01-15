#!/usr/bin/env bash
# See ~/.pypirc
#pandoc docs/index.md -f markdown -t rst -o DESCRIPTION.rst
python setup.py register
