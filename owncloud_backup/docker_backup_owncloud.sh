#!/bin/bash
# Script for backup a volume from a container

CONTAINER_NAME_OWNCLOUD=owncloud_owncloud_1
# Path to files inside Docker container:
PATH_TO_FILES=/mnt/data
PATH_TO_BACKUPS_FILES=/backup/owncloud_data
# MySQL:
CONTAINER_NAME_MYSQL=owncloud_db_1
MYSQL_PASSWORD=password
PATH_TO_BACKUPS_MYSQL=/backup/owncloud_mysql

# Make dir if does not exist:
for PATH_VAR in ${PATH_TO_BACKUPS_FILES} ${PATH_TO_BACKUPS_MYSQL}
do
  if [[ ! -d ${PATH_VAR} ]]; then
    mkdir ${PATH_VAR}
  fi
done

docker stop ${CONTAINER_NAME_OWNCLOUD};
docker run --rm --volumes-from ${CONTAINER_NAME_OWNCLOUD} -v ${PATH_TO_BACKUPS_FILES}:/backup busybox tar cvf /backup/files_$(date +%Y%m%d_%H-%M-%S).tar ${PATH_TO_FILES};
docker start ${CONTAINER_NAME_OWNCLOUD};
docker exec ${CONTAINER_NAME_MYSQL} /usr/bin/mysqldump -u owncloud --password=${MYSQL_PASSWORD} owncloud > ${PATH_TO_BACKUPS_MYSQL}/mysql_$(date +%Y%m%d_%H-%M-%S).sql
