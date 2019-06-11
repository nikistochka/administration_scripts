#!/bin/bash
# Script for restore Owncloud MySQL database

# MySQL:
CONTAINER_NAME_MYSQL=owncloud_db_1
MYSQL_USERNAME=username
MYSQL_PASSWORD=password
PATH_TO_BACKUPS_MYSQL=/backup/owncloud_db


cat ${PATH_TO_BACKUP_MYSQL}/$1 | docker exec -i ${CONTAINER_NAME_OWNCLOUD} /usr/bin/mysql -u ${MYSQL_USERNAME} --password=${MYSQL_PASSWORD} owncloud
