package=bar
pyenv=ENV2
UNAME=$(shell uname)
export ROOT_DIR=${PWD}/cloudmesh/rest/server
MONGOD=mongod --dbpath ~/.cloudmesh/data/db --bind_ip 127.0.0.1
EVE=cd $(ROOT_DIR); $(pyenv); python service.py
VERSION=`head -1 VERSION`

define banner
	@echo
	@echo "###################################"
	@echo $(1)
	@echo "###################################"
endef

ifeq ($(UNAME),Darwin)
define terminal
	osascript -e 'tell application "Terminal" to do script "$(1)"'
endef
endif
ifeq ($(UNAME),Linux)
define terminal
	echo "Linux not yet supported, fix me"
endef
endif
ifeq ($(UNAME),Windows)
define terminal
	echo "Windows not yet supported, fix me"
endef
endif



setup:
	# brew update
	# brew install mongodb
	# brew install jq
	rm -rf ~/.cloudmesh/data/db
	mkdir -p ~/.cloudmesh/data/db

kill:
	killall mongod

mongo:
	$(call terminal, $(MONGOD))

eve:
	$(call terminal, $(EVE))

source:
	pip install -e .
	cms help

test:
	$(call banner, "LIST SERVICE")
	curl -s -i http://127.0.0.1:5000 
	$(call banner, "LIST PROFILE")
	@curl -s http://127.0.0.1:5000/profile  | jq
	$(call banner, "LIST CLUSTER")
	@curl -s http://127.0.0.1:5000/cluster  | jq
	$(call banner, "LIST COMPUTER")
	@curl -s http://127.0.0.1:5000/computer  | jq
	$(call banner, "INSERT COMPUTER")
	curl -d '{"name": "myCLuster",	"label": "c0","ip": "127.0.0.1","memoryGB": 16}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/computer  
	$(call banner, "LIST COMPUTER")
	@curl -s http://127.0.0.1:5000/computer  | jq


nosetests:
	nosetests -v --nocapture tests/test_mongo.py


clean:
	rm -rf *.zip
	rm -rf *.egg-info
	rm -rf *.eggs
	rm -rf docs/build
	rm -rf build
	rm -rf dist
	find . -name '__pycache__' -delete
	find . -name '*.pyc' -delete
	find . -name '*.pye' -delete
	rm -rf .tox
	rm -f *.whl


genie:
	git clone https://github.com/drud/evegenie.git
	cd evegenie; pip install -r requirements.txt

json:
	python evegenie/geneve.py sample.json
	cp sample.settings.py $(ROOT_DIR)/settings.py
	cat $(ROOT_DIR)/settings.py

install:
	cd ../common; pip install .
	cd ../cmd5; pip install .
	pip install .

######################################################################
# PYPI - Only to be exectued by Gregor
######################################################################

twine:
	pip install twine

dist: twine clean
	@echo "######################################"
	@echo "# $(VERSION)"
	@echo "######################################"
	python setup.py sdist --formats=gztar,zip
	python setup.py bdist
	python setup.py bdist_wheel

upload_test: dist
#	python setup.py	 sdist bdist bdist_wheel upload -r pypitest
	rm dist/*.zip
	twine upload --repository pypitest dist/cloudmesh.bar-*.whl	dist/cloudmesh.bar-*.tar.gz

log:
	gitchangelog | fgrep -v ":dev:" | fgrep -v ":new:" > ChangeLog
	git commit -m "chg: dev: Update ChangeLog" ChangeLog
	git push

register: dist
	@echo "######################################"
	@echo "# $(VERSION)"
	@echo "######################################"
	twine register dist/cloudmesh.$(package)-$(VERSION)-py2.py3-none-any.whl
	twine register dist/cloudmesh.$(package)-$(VERSION).macosx-10.12-x86_64.tar.gz
	twine register dist/cloudmesh.$(package)-$(VERSION).tar.gz
	twine register dist/cloudmesh.$(package)-$(VERSION).zip

upload: dist
	twine upload dist/*

#
# GIT
#

tag:
	touch README.rst
	git tag $(VERSION)
	git commit -a -m "$(VERSION)"
	git push
