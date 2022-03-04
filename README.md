

# CalibreWAN
A self hosted server to host your Calibre library online.

# Features

- Advanced filtering (and/or filtering with authors, tags, series, languages)
- oAuth login
- cross-platform
- reading books in your browser


# Screenshots

## Advanced filtering
![App Screenshot](https://i.imgur.com/t540Es6.png)

## View books by author, publisher, rating, etc
![App Screenshot](https://i.imgur.com/tEBKWVj.png)

## View book information
![App Screenshot](https://i.imgur.com/rXmLTf7.png)  
  
## Read book in your browser (supported formats are PDF and epub)
![App Screenshot](https://i.imgur.com/b6hoqc4.png) 

## View all authors, publishers, tags, etc
![App Screenshot](https://i.imgur.com/jsxRH4z.png)  
  
## Browse all books
![App Screenshot](https://i.imgur.com/dFqmekL.png)  
  

# Requirements
* Linux OS or Windows with WSL. This hasn't been tested on macOS, but there's no reason it shouldn't work.
* If running this on windows/WSL, the calibre library should be on WSL. e.g. not something like `/mnt/c/Users/Massiveatoms/Documents/CalibreLibrary`.
* Docker and docker-compose
* Calibre 4.0 until 5.37. This has been confirmed working on these versions, and should theoretically work on older versions.

# Deployment

1. clone this repository
2. copy `./deploy/.env.example` to `./deploy/.env`
3. run `head /dev/urandom |  LC_ALL=C tr -dc 'A-Za-z0-9!@#%^&*(-_=+)' | head -c 50 && echo` or go to [this website](https://djecrety.ir/) to generate a secret key
4. Set the `SECRET_KEY` value in the .env file to the generated key. 
5. `ALLOWED_HOSTS` ahould be set to the url and/or IP you will be hosting this server, seperated by a comma. For example: `ALLOWED_HOSTS="10.10.1.16,cwan.mydomain.com"`
6. Change the  volume mounts in the docker-compose file to reflect your environment. `"/path/to/your/calibre/library:/CWA/UserLibrary"` and `"/path/to/somewhere/to/store/persistent/data/for/CWA:/CWA/Persistent"`
7. Specify the port you want to explose CalibreWAN at in the docker-compose file. The default is port 8000
8. Build the image. `docker-compose build`
9. Host the image. `docker-compose up`
7. (optional) configure your reverse proxy

# First login
The admin panel is located at http://yourdomain.or.ip.addr:port/admin
1. login to the admin panel with the default user created. The username is `superuser_first_login` and the password is `aVeryStrongPassword,this-is-not`
2. Change your password. Do this by clicking on "Change" on the Users line, then selecting the user, and clicking on the link to change the password.
![](https://i.imgur.com/Otc7cTJ.png)
![](https://i.imgur.com/o3lMtE6.png)


## Configuring OAuth
1. create a social application with the OAuth providers you want. Currently, github and google are supported.
2. Generate the needed secrets for whichever provider you want to use.
### github
1. go to [this url](https://github.com/settings/applications/new)
2. Set the homepage to what you're going to host it as, for example "https://calibreserver.yourdomain.com/"  
3. Set the callback to `https://calibreserver.yourdomain.com/accounts/github/login/callback/`
4. Copy the client ID and generated client secret from github to the form
5. Key is not needed, just leave it blank.
6. Select the site and click the right arrow. The site should be in the chosen site box (right side) if chosen correctly.
![](https://i.imgur.com/FQi0ZIl.png)
7. save

### google
1.  Go to https://console.developers.google.com/ and create a new project. 
2.  Go to `APIs & Services > Credentials`, select `Create credentials` and select `OAuth Client ID` to generate one.
3. Select `Web Application`
4. Fill out the form. The name can be whatever you desire.
5. Set the domain name in `Authorized JavaScript origins`.
6. Finally, fill in `https://calibreserver.yourdomain.com/accounts/google/login/callback/` in the `Authorized redirect URI` field.
7. Copy the shown value over to the CalibreWAN Social Application creation form.
* Provider:  “Google”
* Name: Whatever you want “Google”
* Client id: The `Client ID` shown on the google page.
* Secret key: The `Client Secret` shown on the google page.
* Key is not needed, leave it blank.
* Select the site and click the right arrow. The site should be in the chosen site box (right side) if chosen correctly.
![](https://i.imgur.com/FQi0ZIl.png)
7. save

You can now log in to the application with oAuth. 

### Close user registration
By default, the registration of new users is open For security reasons, it is better to close registration after your users have registered to the application. To close it, change `ACCOUNT_ALLOW_SIGNUPS` to `0` in the .env file. The setting applies to both local account and oAuth account registration.

### Make sure you changed the password of the default user



# License

[MIT](https://choosealicense.com/licenses/mit/)


# Roadmap

- Better UI design
- Support to read other book formats online besides PDF and EPUB
- an android app
- more languages
- theming support
