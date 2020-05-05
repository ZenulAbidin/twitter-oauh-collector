#!/usr/bin/python

from flask import Flask, Response, redirect, request, session, url_for, render_template
from twython import Twython

# We can do better than this, get the twitter API key and secret from somewhere else
from consumer_credentials import consumer_key, consumer_secret

t = Twython(app_key=consumer_key, app_secret=consumer_secret)

app = Flask(__name__)

def read_secret_key(filename):
    f = open(filename, "rb");
    secret_key = f.read()
    return key

# a secret key is needed to use session
# The contents of secret.txt should be changed to some random bytes
# for security.
app.secret_key = read_secret_key("secret.txt")

tokens = []

def save_token(token, token_store):
	for x in token_store:
		if x['user_id'] == token['user_id']:
			x = token
			break
	else:
		token_store.append(token)

# So the big picture here is that we do an OAuth procedure that goes like this:
# 1 - create Twython with key/secret
# 2 - get auth tokens and supply it a callback. saving the temp auth tokens returned
# 3 - redirect app to callback
# 4 - create another Twython with key/secret and the temp auth token/secret
# 5 - call get auth tokens with the auth_verifier param that Twython put in the callback url
# 6 - this returns the real auth tokens, save them in a DB.

# All this does is gets the temporary auth tokens.
@app.route('/authorize')
def authorize():
    # These are the temporary auth tokens
	auth_tokens = t.get_authentication_tokens(callback_url=request.url_root[:-1]+url_for('callback'))
	session['rts'] = auth_tokens
	return redirect(auth_tokens['auth_url'])
	
# This route is called after going to /authorize, it shouldn't be called directly.
# This is auth_url above
@app.route('/callback')
def callback():
	if not session.has_key('rts'):
		return 'Error: no request token stored in cookie.'
		
	rts = session['rts']
			
	if request.args.has_key('oauth_token') and request.args['oauth_token'] == rts['oauth_token']:
		if request.args.has_key('oauth_verifier'):
            # We have the auth_verifier
			tu = Twython(app_key=consumer_key, app_secret=consumer_secret,
		        oauth_token=rts['oauth_token'], oauth_token_secret=rts['oauth_token_secret'])
            # These are the real auth tokens
			auth_tokens = tu.get_authorized_tokens(request.args['oauth_verifier'])

            # Instead of this put it inside a database.
			save_token(auth_tokens, tokens)
			return redirect(url_for('thanks'))
	return 'Error: getting the incorrect access tokens.'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/thanks')
def thanks():
	return render_template('thanks.html')

@app.route('/tokens')
def show_tokens():
	return render_template('show_tokens.html', tokens=tokens)

@app.route('/tokens.csv')
def tokens_csv():
	fields = ['user_id', 'screen_name', 'oauth_token', 'oauth_token_secret']
	s = ','.join(fields) + '\n'
	for token in tokens:
		s += ','.join(map(lambda field: str(token[field]), fields)) + '\n'
	return Response(s, mimetype='application/csv')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=False, port=9001)
