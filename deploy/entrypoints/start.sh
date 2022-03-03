APPDIR="/CWA"
USER_DIR="/CWA/UserLibrary"
PERSISTENT="/CWA/Persistent"
export DJANGO_SUPERUSER_PASSWORD="aVeryStrongPassword,this-is-not"
export DJANGO_SUPERUSER_USERNAME="superuser_first_login"
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

python "${APPDIR}/manage.py" migrate sites
python "${APPDIR}/manage.py" makemigrations
python "${APPDIR}/manage.py" migrate
chown -R unit:unit /CWA


# simple error handling, https://stackoverflow.com/a/25180186/11585371
function try()
{
    [[ $- = *e* ]]; SAVED_OPT_E=$?
    set +e
}

function throw()
{
    exit $1
}

function catch()
{
    export ex_code=$?
    (( $SAVED_OPT_E )) && set +e
    return $ex_code
}


try
(  
  python "${APPDIR}/manage.py" createsuperuser --noinput 
)
catch || {
  echo "superuser already exists"
}