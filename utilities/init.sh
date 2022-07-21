#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

# Get environment variables to show up in SSH session
# hack taken form https://stackoverflow.com/a/65988789/3778792
eval $(printenv | sed -n "s/^\([^=]\+\)=\(.*\)$/export \1=\2/p" | sed 's/"/\\\"/g' | sed '/=/s//="/' | sed 's/$/"/' >> /etc/profile)

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
