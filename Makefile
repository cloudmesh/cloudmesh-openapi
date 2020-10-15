package=openapi
UNAME=$(shell uname)
VERSION=`head -1 VERSION`

ifeq ($(UNAME),Linux)
    OPEN=gopen
else
    OPEN=open
endif

define banner
	@echo
	@echo "############################################################"
	@echo "# $(1) "
	@echo "############################################################"
endef


view:
	$(OPEN) docs/index.html

doc:
	pip install sphinx_rtd_theme
	mkdir -p docs
	rm -rf sphinx/sphinx-docs/_build/
	cd sphinx; sh gen_apidocs.sh
	pandoc README.md -o sphinx/sphinx-docs/README.rst
	pandoc README-Scikitlearn.md -o sphinx/sphinx-docs/README-Scikitlearn.rst
	pandoc README.md -o docs/README.rst
	cd sphinx/sphinx-docs; make html
	cp -r sphinx/sphinx-docs/_build/html/* docs
	rm -rf sphinx/sphinx-docs/_build/
	touch docs/.nojekyll

doc-real:
	mkdir -p docs
	cd sphinx; gen_apidoc.sh
	cp sphinx/sphinx_docs/_build/html/docs

source:
	cd ../cloudmesh-common; make source
	$(call banner, "Install cloudmesh-cmd5")
	pip install -e . -U
	cms help

requirements:
	echo "cloudmesh-common" > tmp.txt
	echo "cloudmesh-cmd5" >> tmp.txt
	pip-compile setup.py
	fgrep -v "# via" requirements.txt | fgrep -v "cloudmesh" >> tmp.txt
	mv tmp.txt requirements.txt
	git commit -m "update requirements" requirements.txt
	git push

clean:
	$(call banner, "CLEAN")
	rm -rf dist
	rm -rf *.zip
	rm -rf *.egg-info
	rm -rf *.eggs
	rm -rf docs/build
	rm -rf build
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
	rm -rf .tox
	rm -f *.whl

######################################################################
# PYPI
######################################################################


twine:
	pip install -U twine

dist:
	python setup.py sdist bdist_wheel
	twine check dist/*

patch: clean
	$(call banner, "patch")
	bump2version --allow-dirty patch
	python setup.py sdist bdist_wheel
	git push origin master --tags
	twine check dist/*
	twine upload --repository testpypi  dist/*
	# $(call banner, "install")
	# sleep 10
	# pip install --index-url https://test.pypi.org/simple/ cloudmesh-$(package) -U

minor: clean
	$(call banner, "minor")
	bump2version minor --allow-dirty
	@cat VERSION
	@echo

release: clean
	$(call banner, "release")
	git tag "v$(VERSION)"
	git push origin master --tags
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --repository pypi dist/*
	$(call banner, "install")
	@cat VERSION
	@echo
	# sleep 10
	# pip install -U cloudmesh-common


dev:
	bump2version --new-version "$(VERSION)-dev0" part --allow-dirty
	bump2version patch --allow-dirty
	@cat VERSION
	@echo

reset:
	bump2version --new-version "4.0.0-dev0" part --allow-dirty

upload:
	twine check dist/*
	twine upload dist/*

pip:
	pip install --index-url https://test.pypi.org/simple/ cloudmesh-$(package) -U

#	    --extra-index-url https://test.pypi.org/simple

log:
	$(call banner, log)
	gitchangelog | fgrep -v ":dev:" | fgrep -v ":new:" > ChangeLog
	git commit -m "chg: dev: Update ChangeLog" ChangeLog
	git push

######################################################################
# DOCKER
######################################################################

image:
	docker build -t cloudmesh/cmd5:1.0 .

shell:
	docker run --rm -it cloudmesh/cmd5:1.0  /bin/bash

cms:
	docker run --rm -it cloudmesh/cmd5:1.0

dockerclean:
	-docker kill $$(docker ps -q)
	-docker rm $$(docker ps -a -q)
	-docker rmi $$(docker images -q)

push:
	docker push cloudmesh/cmd5:1.0

run:
	docker run cloudmesh/cmd5:1.0 /bin/sh -c "cd technologies; git pull; make"
