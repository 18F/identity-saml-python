# Set SAML_ENV=config_local to run aginst local running version identity-idp

run: venv
	FLASK_DEBUG=1 FLASK_APP=demosp.py flask run --port=4567

test: venv
	python demosp_test.py

setup: venv
	pip install -r requirements.txt

freeze: venv
	pip freeze > requirements.txt

venv: venv
	virtualenv venv

.PHONY: freeze setup test freeze
