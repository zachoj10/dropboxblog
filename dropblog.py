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
	titles = []
	fileNames = []
	postText = []
	postURL = []
	dates = []
	for line in blogPosts:
		if not line.startswith('#'):
			postURL.append(baseurl + line.strip())
			fileNames.append('/post/' + line.strip())
	postURL = postURL[::-1]
	fileNames = fileNames[::-1]
	blogPosts.close()
	for i in postURL:
		post = urllib.urlopen(i)
		result = ""
		title = i[49:]
		title = os.path.splitext(title)[0]
		date = ""
		for line in post:
			if line.startswith("<title>"):
				title = line[7:]
			elif line.startswith("<date>"):
				date = line[6:]
			else:
				result += line + "\n"
		titles.append(title)
		dates.append(date)
		result = markdown2.markdown(result)
		postText.append(result)
		post.close()


	entries = [dict(title=titles[i], text=postText[i], url=fileNames[i], date=dates[i]) for i in range(len(titles))]
	return render_template('show_entries.html', entries=entries)

@app.route('/post_list')
def show_list():
	blogPosts = urllib.urlopen('https://dl.dropboxusercontent.com/u/9366248/blog/blogPosts')
	baseurl = 'https://dl.dropboxusercontent.com/u/9366248/blog/'
	titles = []
	postText = []
	postURL = []
	fileNames = []
	for line in blogPosts:
		if not line.startswith('#'):
			postURL.append(baseurl + line.strip())
			fileNames.append('/post/' + line.strip())
	postURL = postURL[::-1]
	fileNames = fileNames[::-1]
	blogPosts.close()
	for i in postURL:
		post = urllib.urlopen(i)
		result = ""
		title = i[49:]
		title = os.path.splitext(title)[0]
		for line in post:
			if line.startswith("<title>"):
				title = line[7:]
		titles.append(title)
		post.close()

	entries = [dict(title=titles[i], fileName=fileNames[i]) for i in range(len(titles))]

	return render_template('post_list.html', entries=entries)

@app.route('/post/<postTitle>')
def single_post(postTitle):
	baseurl = 'https://dl.dropboxusercontent.com/u/9366248/blog/'
	post = urllib.urlopen(baseurl + postTitle)
	title = postTitle
	title = os.path.splitext(title)[0] 
	body = ""
	date = ""
	for line in post:
		if line.startswith("<title>"):
				title = line[7:]
		elif line.startswith("<date>"):
			date = line[6:]
		else:
			body += line + "\n"

	body = markdown2.markdown(body)

	return render_template('single_post.html', title=title, body=body, date=date)

@app.route('/about')
def about():
	url = 'https://dl.dropboxusercontent.com/u/9366248/blog/about.md'
	content = urllib.urlopen(url)
	title = "About"
	body = ""
	for line in content:
		body += line + "\n"

	body = markdown2.markdown(body)
	return render_template('single_post.html', title=title, body=body)





if __name__ == '__main__':
    app.run()