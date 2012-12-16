import os
from flask import Flask, redirect, request, session, url_for, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
BASE_URL = 'https://api.box.com/'


@app.route('/')
def redirect_to_folder():
    return redirect(url_for('box_folder', folder_id='0'))


@app.route('/box-folder/<folder_id>')
def box_folder(folder_id):
    if 'oauth_credentials' not in session:
        return redirect(url_for('login'))
    box_folder = get_box_folder(folder_id)
    return jsonify(box_folder)


@app.route('/box-auth')
def box_auth():
    oauth_response = get_token(code=request.args.get('code'))
    set_oauth_credentials(oauth_response.json)
    return redirect(url_for('box_folder', folder_id=0))


@app.route('/login')
def login():
    return redirect(build_box_authorization_url())


def get_box_folder(folder_id):
    if oauth_credentials_are_expired():
        refresh_oauth_credentials()
    resource = '2.0/folders/%s' % folder_id
    url = '%s%s' % (BASE_URL, resource)

    bearer_token = session['oauth_credentials']['access_token']
    auth_header = {'Authorization': 'Bearer %s' % bearer_token}

    api_response = requests.get(url, headers=auth_header)
    return api_response.json


def oauth_credentials_are_expired():
    return datetime.now() > session['oauth_expiration']


def refresh_oauth_credentials():
    refresh_token = session['oauth_credentials']['refresh_token']
    oauth_response = get_token(grant_type='refresh_token',
                               refresh_token=refresh_token)
    set_oauth_credentials(oauth_response.json)


def set_oauth_credentials(oauth_response):
    token_expiration = oauth_response['expires_in']
    session['oauth_expiration'] = (datetime.now()
                                   + timedelta(seconds=token_expiration - 100))
    session['oauth_credentials'] = oauth_response


def get_token(**kwargs):
    endpoint = 'oauth2/token'
    url = '%s%s' % (BASE_URL, endpoint)
    if 'grant_type' not in kwargs:
        kwargs['grant_type'] = 'authorization_code'
    kwargs['client_id'] = os.environ['BOX_CLIENT_ID']
    kwargs['client_secret'] = os.environ['BOX_CLIENT_SECRET']
    token_response = requests.post(url, data=kwargs)
    return token_response.json


def build_box_authorization_url():
    endpoint = 'oauth2/authorize'
    url = ('%s%s?response_type=code&client_id=%s'
           % (BASE_URL, endpoint, os.environ['BOX_CLIENT_ID']))
    return url


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.secret_key = os.environ['SECRET_KEY']
    app.run(host='0.0.0.0', port=port)
