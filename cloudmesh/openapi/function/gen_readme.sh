#!/bin/bash
##########################

md_name=`basename $PWD`

# do pip install of sphinx and sphinx-markdown-builder:  
# pip install sphinx sphinx-markdown-builder

# run sphinx apidoc 
sphinx-apidoc -o sphinx-docs . sphinx-apidoc --full -A 'sp20-516-ai' -H 'AI Project' --module-first; cd sphinx-docs;

# update conf.py to be able to find your code and support magic methods
echo "" >> conf.py
echo " 
import os
import sys
sys.path.insert(0,os.path.abspath('../../'))
sys.path.insert(0,os.path.abspath('../'))

def skip(app, what, name, obj,would_skip, options):
    if name in ( '__init__',):
        return False
    return would_skip

def setup(app):
    app.connect('autodoc-skip-member', skip)  
 " >> conf.py  

# make markdown files
make markdown

# copy generated markdown to permanent location as README and cleanup

cp _build/markdown/${md_name}.md ../
cd ..; rm -r sphinx-docs;
