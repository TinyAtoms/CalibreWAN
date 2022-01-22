
# Deployment instructions

## configure the following settings
create a file named `.env`. See example env file in `.env.example`
It is important to set your own secret key.
You can generate a secret key by opening python and running the following:  
```
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
```
copy that over to the `.env` file.
Set the DEBUG to false.

## create superuser
1.create a Persistent folder in the repo
2. run `./manage.py makemigrations`
3. run `./manage.py migrate`
4. run `./manage.py createsuperuser`. this will be your admin account

## create docker image
build with this while being in the root folder of the repo
```
sudo docker build --tag calibrewan:1.0 . -f ./deploy/Dockerfile
```

Run docker with these mounts.
`/CWA/UserLibrary` is where the desired calibre library should be mounted, and `/CWA/Persistent` is where the 
django db will be generated/stored. Plus eventual logs, i think i need more info for logs.
```
sudo docker run --publish 80:80 \
-v '/path/to/calibre/library/you/want/to/mount:/CWA/UserLibrary' \
-v '/path/to/some/Persistent/storage:/CWA/Persistent' \
--name cw calibrewan:1.0
```
copy over the database from ./Persistent to the volume you're mounting as /CWA/Persistent

Here's an example:
```
sudo docker run --publish 80:80 \
-v '/home/massiveatoms/demo/CalibreWAN/UserLibrary:/CWA/UserLibrary' \
-v '/home/massiveatoms/demo/CalibreWAN/Persistent:/CWA/Persistent' \
--name cw calibrewan:1.0
```

## Setting up OAuth

1. login to the admin panel
3. create a social app with the OAuth providers you want. Currently, github, google and microsoft are supported. Make sure to select the site when adding social applications


### github
go to [this url](https://github.com/settings/applications/new)
Set the homepage to what you're going to host it as, for example
"https://calibreserver.yourdomain.com/"  
Set the callback to `https://calibreserver.yourdomain.com/accounts/github/login/callback/`

Copy the client ID and generated client secret from github to the form
save




