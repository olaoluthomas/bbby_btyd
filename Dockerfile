# Use the official lightweight Python image.
# https://hub.docker.com/_/python
#FROM jupyter/datascience-notebook:python-3.9.2
FROM python:3.9-slim-buster

LABEL version="0.1"
LABEL image-desc=""
LABEL maintainer="Simeon Thomas"
LABEL maintainer-email="thomasolaoluwa@gmail.com"
LABEL org.opencontainers.image.source="https://github.com/olaoluthomas/ltv_btyd_demo"
LABEL org.opencontainers.image.version=""

# create worker account to run workflow
RUN groupadd -g 8910 app && useradd -rm -d /app -s /bin/bash -g app -G sudo -u 1001 app
USER app

# hardcoding port assignment so it builds in local test of docker
# ENV PORT 8080
# EXPOSE $PORT

# Declare working directory, attach volume, copy requirements file to container image,
# and install dependencies.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY --chown=app:app . ./

# add user-installed packages to PATH
ENV PATH="/app/.local/bin:${PATH}"

# Install app dependencies.
RUN pip install --user --upgrade pip
RUN pip install --user -r requirements.txt

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 0 main:app
ENTRYPOINT [ "gunicorn", "--bind", ":8080", "--workers", "1","--threads", "4", "--timeout", "0", "main:app"]