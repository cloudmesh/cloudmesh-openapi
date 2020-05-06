#!/bin/sh
mkdir ".ssh"
ssh-keygen -t dsa -N "OPENAPI3" -f .ssh/id_rsa
cms help
cms config set cloudmesh.profile.user=admin
cms config set cloudmesh.data.mongo.MONGO_AUTOINSTALL=True
cms config set cloudmesh.data.mongo.MONGO_PASSWORD=OPENAPI3
cms admin mongo install
export PATH="$PATH:/root/local/mongo/bin"
cms init
