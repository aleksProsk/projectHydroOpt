# start in linux via
# cd  /cygdrive/c/Users/SEC/Eigene Dateien/MyDashFiles
# export FLASK_APP=minimal-flask.py
# flask run

# start in windows via
# set FLASK_APP=minimal-flask.py
# flask run

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Index page'

@app.route('/hello')
def hello():
    return 'Hello, World'	
	
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id