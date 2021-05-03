# syntax=docker/dockerfile:1
FROM ubuntu:20.04
RUN mkdir cm
RUN apt update
RUN apt install python3-venv python3-wheel python3-dev python3-pip build-essential -y
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip install pip -U
RUN pip install cloudmesh-installer
RUN apt install git -y
RUN cd cm; cloudmesh-installer get openapi
RUN pip install sklearn pandas
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Indiana/Indianapolis
RUN apt install tzdata -y
RUN apt install emacs -y
CMD /bin/bash