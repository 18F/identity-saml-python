Warning:
========

This sample SP has been retired.  It was used for early prototyping for integrations with login.gov and has not been maintained. It has confirmed vulnerabilities and should not be used for production itegrations.

For maintained examples of SAML integrations with login.gov please refer to:

- https://github.com/18F/identity-saml-rails
- https://github.com/18F/identity-saml-sinatra

Sample Python SP
================


[![Build Status](https://travis-ci.org/18F/identity-sp-python.svg?branch=master)](https://travis-ci.org/18F/identity-sp-python)

An example service provider (SP) written in python that integrates with 18F's
identity-idp.

This is a very simply app based the `flask` and `python-saml` which
supports SAML-based SSO and SLO.

### Setup

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

### Testing

    $ python demosp_test.py

### Running (development mode)

    $ SAML_ENV=config_local FLASK_DEBUG=1 FLASK_APP=demosp.py flask run --port=4567

### Generating a new key + self-signed cert

    openssl req -newkey rsa:2048 -nodes -keyout config/certs/sp.key \
      -x509 -out config/certs/sp.crt -config config/openssl.conf
