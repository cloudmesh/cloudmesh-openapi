#!/bin/bash
##########################

#md_name=`basename $PWD`
search_path="../cloudmesh/openapi"

# as a pre-req do pip install of below (uncomment line):  
# pip install sphinx sphinx-markdown-builder sphinx_rtd_theme

# run sphinx apidoc 
sphinx-apidoc -o sphinx-docs ${search_path} sphinx-apidoc --full -A 'The Cloudmesh Team' -H 'Cloudmesh OpenAPI Service Generator' --module-first -f; cd sphinx-docs;

# copy standardized conf.py and index.rst to sphinx-docs dir and overwrite auto generated ones.
cp ../conf.py .
cp ../index.rst .
