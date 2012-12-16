box-oauth2-example
==================

A simple app showing how to use OAuth2 with Box. Designed for use with [Heroku](http://www.heroku.com/), though you can obviously host it however you like.

# Pre-Setup

Before you can do anything with the Box API, you need to [register to get a Client ID and Client Secret](http://bit.ly/boxapikey) to make API calls with. 

![Box Developers](https://www.evernote.com/shard/s146/sh/8c772c78-86d7-4e62-8fed-3dfec3b4a8a2/c7347e5579c1b6374b00e745ae8b2b39/res/8ecd666e-3820-4f5e-be09-eb46e75e243a/skitch.png)

# Setup

First create a virtual environment, and activate it

    >>> virtualenv venv --distribute
    >>> source venv/bin/activate
    
Install all dependencies with pip

    >>> pip install -r requirements.txt
    
Create an instance on Heroku

    >>> heroku create
    
Set environment variables for the client id and client secret so that your app can make API calls to Box (replace with your own id/secret)

    >>> heroku config:add BOX_CLIENT_ID={your client id} BOX_CLIENT_SECRET={your client secret}
    
Push to Heroku with git

    >>> git add .
    >>> git commit -m 'init'
    >>> git push heroku master
    
Start up a dyno on Heroku

    >>> heroku ps:scale web=1
    
Go to your newly launched app!

    >>> heroku open
