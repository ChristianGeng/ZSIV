#!/usr/bin/env bash
# python manage.py syncdb --noinput
# python manage.py test  ZSIV  --keepdb

# start the container from the host's command line
function start_container {
    docker run -p 3306:3306 \
           --name=ZSIV \
           -v "$(pwd)":/ZSIV \
           -v /media/win-d/myfiles/2017/django/IVs/:/dumps \
           -e MYSQL_ROOT_PASSWORD=SQLADMIN \
           -e MYSQL_DATABASE=ZSIV \
           -d  mysql/mysql-server:latest
        }

# usage:
# log into the machine with docker exec -it -u christian ZSIV /bin/bash
# From the shell in the container run
#  source this file with . munge.sh and
# run restore_db
function restore_db {
    mysql -u root  -p ZSIV < /dumps/fixdb.sql
    mysql -u root  -p ZSIV < /dumps/dumps/ZSIV-realmas.dump
}
