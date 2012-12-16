import os
from flask import Flask, redirect, request, session, url_for, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
BASE_URL = 'https://api.box.com/'


@app.route('/box-folder/<folder_id>')
def box_folder(folder_id='0'):
    resource = '2.0/folders/%s' % folder_id
    url = '%s%s' (BASE_URL, resource)

    bearer_token = session['oauth_credentials']['access_token']
    auth_header = {'Authorization': 'Bearer %s' % bearer_token}

    box_folder = requests.get(url, headers=auth_header)
    return jsonify(box_folder)


@app.route('/box-auth')
def box_auth():
    session['oauth_credentials'] = get_access_token(request.args.get('code'))
    session['oauth_expiration'] = datetime.now() + timedelta(seconds=3600)
    return redirect(url_for(box_folder))


@app.route('/login')
def login():
    return redirect(build_box_authorization_url())


def get_access_token(code):
    endpoint = 'oauth2/token'
    url = '%s%s' % (BASE_URL, endpoint)
    form_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': os.environ['BOX_CLIENT_ID'],
        'client_secret': os.environ['BOX_CLIENT_SECRET']
    }
    oauth_response = requests.post(url, data=form_data)
    return oauth_response


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
