#!/bin/bash
APPDIR="/CWA"
USER_DIR="/CWA/UserLibrary"
PERSISTENT="/CWA/Persistent"
export DJANGO_SUPERUSER_PASSWORD="Default-Password1"
export DJANGO_SUPERUSER_USERNAME="DefaultUsername"
export DJANGO_SUPERUSER_EMAIL="thishasnoeffect@whatsoever.com"
if [ ! -d "$USER_DIR" ]; then
  echo "Calibre Library not mounted at the correct location."
  echo "Mount it at /CWA/UserLibrary/"
  echo "Exiting..."
  exit 1
fi

if [ ! -d "$PERSISTENT" ]; then
  echo "A data directory not mounted at the correct location, exiting"
  echo "This is used to store the database and logs"
  echo "mount something at /CWA/Persistent/"
  echo "exiting"
  exit 1
fi

python "${APPDIR}/manage.py" makemigrations
python "${APPDIR}/manage.py" migrate sites
python "${APPDIR}/manage.py" migrate

usermod -u $DUID CWA
groupmod -g $DGID CWA
chown -R CWA:CWA /CWA


FILE="/CWA/Persistent/su.created"
if [[ -f "$FILE" ]]; then
  echo "superuser already created"
else
  python "${APPDIR}/manage.py" createsuperuser --noinput
  touch "$FILE"
fi
