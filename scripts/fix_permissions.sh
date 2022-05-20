#!/bin/bash

# It fixes permissions of the web server after a git pull is made using local user
#       It's made to work properly with apache server
# Execution: (djangomain): scripts/fix_permissions.sh

sudo chown -R :www-data ../imhea
sudo chmod -R 750 ../imhea
sudo chown -R :www-data ../venv_imhea
sudo chmod -R 750 ../venv_imhea
sudo chmod -R 770 media
sudo chmod -R 750 static

#sudo chmod 770 /media/backup/archivos
#sudo chown :www-data /media/backup/archivos
#sudo chmod 770 /media/backup/archivos/tmp
#sudo chown :www-data /media/backup/archivos/tmp