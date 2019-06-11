#!/bin/bash

# Write below path to folder(s) for clean
BACKUP_FOLDER="/backup/folder_template*"
DAYS_TO_KEEP_BACKUPS=30

find ${BACKUP_FOLDER} -type f \( -name "*.tar" -o -name "*.sql" \) -mtime +${DAYS_TO_KEEP_BACKUPS} -exec rm -f {} \;
