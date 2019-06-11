#!/bin/bash
# Script for restore Owncloud user files in Docker container

CONTAINER_NAME_OWNCLOUD=owncloud_owncloud_1
# Path to files inside Docker container:
PATH_TO_FILES=/mnt/data
PATH_TO_BACKUPS_FILES=/backup/owncloud_files

# Restore user files
docker stop ${CONTAINER_NAME_OWNCLOUD};
docker run --rm --volumes-from ${CONTAINER_NAME_OWNCLOUD} -v ${PATH_TO_BACKUPS_FILES}:/backup ubuntu bash -c "cd ${PATH_TO_FILES} && tar xvf /backup/$1 --strip 1";
docker start ${CONTAINER_NAME_OWNCLOUD}
