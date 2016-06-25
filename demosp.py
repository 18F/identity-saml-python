"""
Demo Relying Party based on python and flask
"""

import os

from flask import Flask, render_template, redirect, request, make_response, session
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from urlparse import urlparse

app = Flask(__name__)
app.secret_key = os.urandom(24)

CONFIG_PATH = os.environ.get('SAML_ENV', 'config')
print 'Using config from: %s' % CONFIG_PATH


def build_saml_req():
    """ Build a request object suitable for python-saml, based on the
    flask request object."""
    req = {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': urlparse(request.url).port,
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy(),
        'query_string': request.query_string
    }
    return req


def build_saml_auth():
    req = build_saml_req()
    return OneLogin_Saml2_Auth(req, custom_base_path=CONFIG_PATH)


@app.route('/')
def index():
    if 'email' in session:
        return redirect('/success')
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    '''SAML SSO End-Point
    '''
    print 'Login recieved'

    authn = build_saml_auth()
    login_url = authn.login()

    return redirect(login_url)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/metadata')
def metadata():
    '''SAML Metadata End-Point
    '''
    auth = build_saml_auth()
    saml_settings = auth.get_settings()
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)
    if errors:
        print auth.get_last_error_reason()
        return make_response(', '.join(errors), 500)

    resp = make_response(metadata, 200)
    resp.headers['Content-Type'] = 'text/xml'
    return resp


@app.route('/consume', methods=['POST'])
def consume():
    '''SAML ACS End-Point
    '''
    auth = build_saml_auth()
    auth.process_response()
    errors = auth.get_errors()
    if errors:
        print auth.get_last_error_reason()
        return make_response(', '.join(errors), 500)

    if not auth.is_authenticated():
        return make_response('Auth failed'.join(errors), 500)

    session['email'] = auth.get_attribute('email')[0]
    return redirect('/success')


@app.route('/logout')
def logout():
    name_id = None
    session_index = None
    auth = build_saml_auth()
    session.clear()
    return redirect(auth.logout(name_id=name_id, session_index=session_index))
