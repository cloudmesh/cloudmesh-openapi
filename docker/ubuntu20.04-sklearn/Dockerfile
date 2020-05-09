FROM ubuntu:20.10

ENV DEBIAN_FRONTEND noninteractive

# ################################################################
# SYSTEM UPDATE
# ################################################################

RUN apt-get -y update --fix-missing
RUN apt-get -y dist-upgrade
RUN apt-get install -y --no-install-recommends apt-utils

# ################################################################
# DEVELOPMENT TOOLS
# ################################################################

RUN apt-get install -y build-essential checkinstall --fix-missing
RUN apt-get install -y \
    lsb-core \
    dnsutils \
    libssl-dev \
    libffi-dev \
    libreadline-gplv2-dev \
    libncursesw5-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    libffi-dev \
    zlib1g-dev
RUN apt-get install -y \
    git-core \
    git \
    wget \
    curl

# ################################################################
# INSTALL CLOUDMESH
# ################################################################

# TODO: MAKE python point to python3
# TODO: UPDATE pip3 to get latests pip
# possibly use venv

RUN pip install cloudmesh-installer
WORKDIR /usr/local/code
RUN cloudmesh-installer get cloud openapi
WORKDIR /root
COPY . /root
RUN ["chmod", "+x", "/root/cloudmesh-init.sh"]
RUN ["chmod", "+x", "/root/start-server.sh"]
RUN ["chmod", "+x", "/root/stop-server.sh"]
RUN /root/cloudmesh-init.sh
EXPOSE 8080
WORKDIR /usr/local/code/cloudmesh-openapi
CMD ["/bin/bash"]
