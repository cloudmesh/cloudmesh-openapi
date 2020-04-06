FROM ubuntu:19.10
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update --fix-missing
RUN apt-get -y dist-upgrade
RUN apt-get install -y --no-install-recommends apt-utils
# DEVELOPMENT TOOLS
RUN apt-get install -y build-essential checkinstall --fix-missing
RUN apt-get install -y lsb-core \
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
 zlib1g-dev \
 git-core \
 git \
 wget \
 curl \
 rsync \
 graphviz
# INSTALL PYTHON 3.8 FROM SOURCE
WORKDIR /usr/src
RUN wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz
RUN tar xzf Python-3.8.2.tgz
WORKDIR /usr/src/Python-3.8.2
RUN ./configure --enable-optimizations
RUN make altinstall
# INSTALL PACKAGED PYTHON 3.8
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.8 10
RUN update-alternatives --config python
RUN update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.8 10
RUN update-alternatives --config pip
RUN yes '' | update-alternatives --force --all && python --version
RUN pip install -U pip && pip --version
RUN pip install connexion[swagger-ui] \
 cloudmesh-cloud \
 cloudmesh-installer \
 docstring_parser
WORKDIR /usr/local/code
RUN git clone https://github.com/cloudmesh/cloudmesh-openapi.git
WORKDIR /usr/local/code/cloudmesh-openapi
RUN cloudmesh-installer get openapi
WORKDIR /root
COPY . /root
EXPOSE 8080
ENTRYPOINT /root/openapi3.sh
