FROM continuumio/miniconda3:4.9.2

# conda setup
RUN conda config --set safety_checks disabled

# apt-get setup
RUN apt-get update && apt-get -y install \
 libgtk2.0-dev

WORKDIR .

# create mount alias
RUN mkdir mount_drive

# env setup
ARG ENV_PATH

# copy web api
COPY web_api /web_api
RUN conda env create --file web_api/base_env.yml

# copy necessary environment to root folder (to be executed further)
COPY $ENV_PATH /.
RUN conda env create --file $ENV_PATH

EXPOSE 8080

ENTRYPOINT conda run --no-capture-output -n base_env python web_api/api.py
