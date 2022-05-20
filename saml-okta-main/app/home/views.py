# -*- coding: utf-8 -*-
"""Home views."""
from flask import request, Blueprint, render_template, redirect, session, url_for
from flask_login import login_user
from saml2 import entity
from ..saml.config import metadata_url_for
from ..saml.client import saml_client_for
from ..user import user_store, User

blueprint = Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/')
def main_page():
    return render_template('main_page.html', idp_dict=metadata_url_for)


@blueprint.route("/saml/login/<idp_name>")
def sp_initiated(idp_name):
    saml_client = saml_client_for(idp_name)

    reqid, info = saml_client.prepare_for_authenticate()

    redirect_url = None
    for key, value in info['headers']:
        if key == 'Location':
            redirect_url = value
    response = redirect(redirect_url, code=302)
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


@blueprint.route("/saml/sso/<idp_name>", methods=['POST'])
def idp_initiated(idp_name):

    saml_client = saml_client_for(idp_name)
    authn_response = saml_client.parse_authn_request_response(
        request.form['SAMLResponse'],
        entity.BINDING_HTTP_POST)
    authn_response.get_identity()
    user_info = authn_response.get_subject()
    username = user_info.text
    if username not in user_store:
        user_store[username] = {
            'first_name': authn_response.ava['FirstName'][0],
            'last_name': authn_response.ava['LastName'][0],
        }
    user = User(username)
    session['saml_attributes'] = authn_response.ava
    login_user(user)
    # url = url_for('user')
    if 'RelayState' in request.form:
        url = request.form['RelayState']
    return redirect('/')
