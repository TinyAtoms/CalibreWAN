

# CalibreWAN
A self hosted server to host your Calibre library online.

## Features

- Advanced filtering (and/or filtering with authors, tags, series, languages)
- oAuth login
- cross-platform



## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)



## License

[MIT](https://choosealicense.com/licenses/mit/)


## Roadmap

- Better UI design
- Support to read other book formats online besides PDF and EPUB
- an android app
- more languages
- theming support





# Requirements
* Linux OS or Windows with WSL. This hasn't been tested on macOS, but I forsee no reason it should not work. 
* If running this on windows/WSL, the calibre library should not be in the windows disk.  e.g. not something like `/mnt/c/Users/Massiveatoms/Documents/CalibreLibrary`.
* Docker and docker-compose
* Calibre 4.0 until 5.37. This has been confirmed working on these versions, and should theoretically work on older versions.

# Deployment

1. clone this repository
2. copy `./deploy/.env.example` to `./deploy/.env`
3. run `head /dev/urandom |  LC_ALL=C tr -dc 'A-Za-z0-9!@#%^&*(-_=+)' | head -c 50 && echo` to generate a secret key, and set the SECRET_KEY value in the environment file to this. You could also use [this website](https://djecrety.ir/) to generate your secret key.
4. Set the IP and/or url where CalibreWAN will be accessible from, seperated by commas if you will have multiple. For example: `ALLOWED_HOSTS="10.10.1.16,cwan.mydomain.com"`
5. Change the  volume mounts in the docker-compose file to reflect your environment. `"/path/to/your/calibre/library:/CWA/UserLibrary"` and `"/path/to/somewhere/to/store/persistent/data/for/CWA:/CWA/Persistent"`
6. Specify the port you want to explose CalibreWAN at in the docker-compose file. The default is port 8000
7. Build the container with docker compose and host it
7. (optional) configure your reverse proxy

# First login
The admin panel is located at /admin
1. login to the admin panel with the default user created. The username is `superuser_first_login` and the password is `aVeryStrongPassword,this-is-not`
2. Change your password. Do this by clicking on "Change" on the Users line. Change the password.

## Configuring oAuth
1. create a social application with the OAuth providers you want. Currently, github, google and microsoft are supported. 
2. Fill in the values:
### github
1. go to [this url](https://github.com/settings/applications/new)
2. Set the homepage to what you're going to host it as, for example "https://calibreserver.yourdomain.com/"  
3. Set the callback to `https://calibreserver.yourdomain.com/accounts/github/login/callback/`
4. Copy the client ID and generated client secret from github to the form
5. Key is not needed, leave it blank.
5. Select the site and click the right arrow. The site should be in the chosen site box (right side) if chosen correctly.
5. save

### google
Go to https://console.developers.google.com/ and create a new project
After you create a project you will have to create a “Client ID” and fill in some project details for the consent form that will be presented to the client.
Under “APIs & auth” go to “Credentials” and create a new Client ID. Probably you will want a “Web application” Client ID. Provide your domain name or test domain name in “Authorized JavaScript origins”. Finally fill in http://calibreserver.yourdomain.com/accounts/google/login/callback/ in the “Authorized redirect URI” field. You can fill multiple URLs, one for each test domain. After creating the Client ID you will find all details for the Django configuration on this page.
Users that login using the app will be presented a consent form. For this to work additional information is required. Under “APIs & auth” go to “Consent screen” and at least provide an email and product name.
Fill in the form as follows:
* Provider, “Google”
* Name, your pick, suggest “Google”
* Client id, is called “Client ID” by Google
* Secret key, is called “Client secret” by Google
* Key, is not needed, leave blank.
You can now log in to the application with oAuth. 

### Close user registration
By default, the registration of new users is open. To close it, change `ACCOUNT_ALLOW_SIGNUPS` in the env file. The setting applies to both local account and oAuth account registration.

### Make sure you changed the password of the default user
