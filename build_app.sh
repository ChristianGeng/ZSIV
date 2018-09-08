#!/usr/bin/env bash

python manage.py syncdb --noinput
python manage.py test  ZSIV  --keepdb
