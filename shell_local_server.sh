#!/bin/bash
# delete all pyc files on the project
find . -name "*.pyc" -exec rm -rf {} \;
./manage.py shell --settings=config.settings.local