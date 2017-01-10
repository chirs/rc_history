#!/usr/bin/env python3

# Compliments of Stanley Zheng and [I forgot who; somebody from the previous batch]

# Not actually used in this project; but potentially useful if you don't want to manually input 500+ names

import os
import requests
from requests_oauthlib import OAuth2Session


def main():

    # set these in a .sh file; 
    CLIENT_ID     = os.environ.get('CLIENT_ID', None) 
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET', None)

    # local access to RC api
    REDIRECT_URI  = "urn:ietf:wg:oauth:2.0:oob"

    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)

    authorization_url, state = oauth.authorization_url('https://www.recurse.com/oauth/authorize')

    print('Please go to %s and authorize access.' % authorization_url)
    authorization_response = input('Enter the full callback URL')

    token = oauth.fetch_token(
        'https://www.recurse.com/oauth/token',
        authorization_response=authorization_response,
        client_secret=CLIENT_SECRET
        )

    r = oauth.get('https://www.recurse.com/api/v1/people/me')

    print(r)


if __name__ == "__main__":
    main()
