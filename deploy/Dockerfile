
## pull official base image
FROM nginx/unit:1.22.0-python3.9
EXPOSE 80


## set work directory
WORKDIR /CWA

## install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
## copy project
COPY ./CalibreWAN ./CalibreWAN
COPY ./library ./library
COPY ./templates ./templates
COPY ./static ./static
COPY ./manage.py ./manage.py

# perms
RUN chown -R unit:unit /CWA
COPY ./deploy/entrypoints/* /docker-entrypoint.d/
RUN chmod +x /docker-entrypoint.d/start.sh
