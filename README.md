box-oauth2-example
==================

A simple app showing how to use OAuth2 with Box. Designed for use with [Heroku](http://www.heroku.com/), though you can obviously host it however you like.

# Setup

First create a virtual environment, and activate it

    >>> virtualenv venv --distribute
    >>> source venv/bin/activate
    
Install all dependencies with pip

    >>> pip install -r requirements.txt
    
Create an instance on Heroku

    >>> heroku create
    
Push to Heroku with git

    >>> git add .
    >>> git commit -m 'init'
    >>> git push heroku master
    
Start up a dyno on Heroku

    >>> heroku ps:scale web=1
    
Go to your newly launched app!

    >>> heroku open
