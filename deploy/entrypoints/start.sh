APPDIR="/CWA"
USER_DIR="/CWA/UserLibrary"
PERSISTENT="/CWA/Persistent"
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

#cp -R -u -p "/CWA/Persistent/db.sqlite3" "/CWA/Persistent/"
ls -l /CWA
# RUN chmod a+rw /CWA /CWA/*
chown -R unit:unit /CWA
python "${APPDIR}/manage.py" makemigrations
python "${APPDIR}/manage.py" migrate
ls -l /CWA/static