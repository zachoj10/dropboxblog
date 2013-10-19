# all the imports
import sqlite3
import urllib
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import os
import markdown2

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
	blogPosts = urllib.urlopen('https://dl.dropboxusercontent.com/u/9366248/blog/blogPosts')
	baseurl = 'https://dl.dropboxusercontent.com/u/9366248/blog/'
	cur = g.db.execute('select title, text from entries order by id desc')
	titles = []
	postText = []
	postURL = []
	for line in blogPosts:
		if not line.startswith('#'):
			postURL.append(baseurl + line.strip())
	blogPosts.close()
	for i in postURL:
		post = urllib.urlopen(i)
		result = ""
		title = i[49:]
		title = os.path.splitext(title)[0]
		for line in post:
			if line.startswith("<title>"):
				title = line[7:]
			else:
				result += line.strip() + "\n"
		titles.append(title)
		result = markdown2.markdown(result)
		postText.append(result)
	for i in postText:
		print(i)


	entries = [dict(title=titles[i], text=postText[i]) for i in range(len(titles))]
	return render_template('show_entries.html', entries=entries)


if __name__ == '__main__':
    app.run()