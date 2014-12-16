#!/usr/bin/env bash
pandoc docs/index.md -f markdown -t rst -o DESCRIPTION.rst
python setup.py register