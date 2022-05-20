import requests
from flask import url_for
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
)
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
from .config import metadata_url_for


def saml_client_for(idp_name=None):

    if idp_name not in metadata_url_for:
        raise Exception("Settings for IDP '{}' not found".format(idp_name))
    acs_url = url_for("home.idp_initiated", idp_name=idp_name, _external=True)
    https_acs_url = url_for("home.idp_initiated", idp_name=idp_name, _external=True, _scheme='https')

    rv = requests.get(metadata_url_for[idp_name])

    settings = {
        'entityid': 'http://127.0.0.1:5000/saml/sso/example-okta-com',
        'metadata': {
            'inline': [rv.text],
        },
        'service': {
            'sp': {
                'endpoints': {
                    'assertion_consumer_service': [
                        (acs_url, BINDING_HTTP_REDIRECT),
                        (acs_url, BINDING_HTTP_POST),
                        (https_acs_url, BINDING_HTTP_REDIRECT),
                        (https_acs_url, BINDING_HTTP_POST)
                    ],
                },
                'allow_unsolicited': True,
                'authn_requests_signed': False,
                'logout_requests_signed': True,
                'want_assertions_signed': True,
                'want_response_signed': False,
            },
        },
    }
    sp_config = Saml2Config()
    sp_config.load(settings)
    sp_config.allow_unknown_attributes = True
    saml_client = Saml2Client(config=sp_config)
    return saml_client
