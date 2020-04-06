FROM ubuntu:19.10
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update --fix-missing
RUN apt-get -y dist-upgrade
RUN apt-get install -y --no-install-recommends apt-utils
# DEVELOPMENT TOOLS
RUN apt-get install -y build-essential checkinstall --fix-missing
RUN apt-get install -y lsb-core
RUN apt-get install -y dnsutils
RUN apt-get install -y libssl-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y libreadline-gplv2-dev
RUN apt-get install -y libncursesw5-dev
RUN apt-get install -y libsqlite3-dev
RUN apt-get install -y libgdbm-dev
RUN apt-get install -y libc6-dev
RUN apt-get install -y libbz2-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y git-core
RUN apt-get install -y git
RUN apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install -y rsync
RUN apt-get install -y graphviz
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
RUN yes '' | update-alternatives --force --all
RUN python --version
RUN python --version
RUN pip install -U pip
RUN pip --version
RUN pip install connexion[swagger-ui]
RUN pip install cloudmesh-cloud
RUN pip install cloudmesh-installer
RUN pip install docstring_parser
RUN cms help
WORKDIR /usr/local/code
RUN git clone https://github.com/cloudmesh/cloudmesh-openapi.git
WORKDIR /usr/local/code/cloudmesh-openapi
RUN cloudmesh-installer get openapi
WORKDIR /root
COPY . /root
EXPOSE 8080
ENTRYPOINT /root/openapi3.sh
