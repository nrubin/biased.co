from flask import Flask, session, render_template, request, redirect, url_for, abort, jsonify
import feedparser
import requests
import os
readability_key = "c439f2ebaf65caf56aad16d906d5da4a5ce21023"
readability_root_url = "http://readability.com/api/content/v1/parser"
#article_url = "http://www.aljazeera.com/news/middleeast/2014/07/gaza-lies-ruins-israel-war-201472794647457501.html"
#article_url = "http://feedproxy.google.com/~r/jpost/LBao/~3/fapMYng9Vzw/story01.htm"

app = Flask(__name__)

@app.route('/')
def home():
	
	jpost = feedparser.parse("http://www.jpost.com/Rss/RssFeedsHeadlines.aspx")
	jpost_stories = jpost.entries
	
	aljazeera = feedparser.parse('http://www.aljazeera.com/Services/Rss/?PostingId=2007731105943979989')
	aljazeera_stories = aljazeera.entries

	return render_template('home.html',jpost_stories=jpost_stories, aljazeera_stories=aljazeera_stories)

@app.route('/article')
def get_article():
	url = request.args.get("url")
	print url
	r = requests.get("%s?url=%s&token=%s" % (readability_root_url,url,readability_key))
	print r
	data = r.json()
	return data["content"]

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        app.logger.debug("%s"%e)


