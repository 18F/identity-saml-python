# Makefile for building and running the project.
# The purpose of this Makefile is to avoid developers having to remember
# project-specific commands for building, running, etc.  Recipes longer
# than one or two lines should live in script files of their own in the
# bin/ directory.

run: venv
	FLASK_DEBUG=1 FLASK_APP=demosp.py flask run

run_local: venv
	SAML_ENV=config_local FLASK_DEBUG=1 FLASK_APP=demosp.py flask run --port=4567

deploy: venv
	cf push

test: venv
	python demosp_test.py

setup: venv
	pip install -r requirements.txt

freeze: venv
	pip freeze > requirements.txt

venv: venv
	virtualenv venv

.PHONY: freeze setup test freeze
