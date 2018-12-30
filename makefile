SHELL:=/bin/bash
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON_VERSION:=python3.7

all: dependencies

dependencies:
	if [ ! -d $(ROOT_DIR)/env ]; then $(PYTHON_VERSION) -m venv $(ROOT_DIR)/env; fi
	source $(ROOT_DIR)/env/bin/activate; yes w | python -m pip install -r $(ROOT_DIR)/requirements.txt

package: clean_package dependencies
	mkdir -p dist
	cd env/lib/$(PYTHON_VERSION)/site-packages/ && \
	zip -r9 ../../../../dist/function.zip . -x pip\* __pycache__\* fire\* setuptools\* pkg_resources\* && \
	cd $(ROOT_DIR) && \
	zip -g ./dist/function.zip app.py

clean_package:
	rm -rf dist

clean:
	rm -rf dist
	rm -rf env
