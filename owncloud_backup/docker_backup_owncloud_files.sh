#!/bin/bash
# Script for backup a volume from a container


CONTAINER_NAME=owncloud_owncloud_1
VOLUME_NAME=/mnt/data/
PATH_TO_BACKUPS=/backup/owncloud_files

docker stop ${CONTAINER_NAME};
docker run --rm --volumes-from ${CONTAINER_NAME} -v ${PATH_TO_BACKUPS}:/backup busybox tar cvf /backup/files_$(date +%Y%m%d_%H-%M-%S).tar $VOLUME_NAME;
docker start ${CONTAINER_NAME}
