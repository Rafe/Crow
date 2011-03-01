from itty.itty import *
import sqlite3
import setting
import json

@get('/')
def index(request):
	return open('html/search.html','r').read()

@get('/page/(?P<page_id>\d+)')
def html(request,page_id):
	conn = sqlite3.connect(setting.get("DB"))
	page = conn.execute("select html from pages where id = %s;" % page_id).fetchone()
	if page:
		return page[0]
	else: return "<h1>no current id!</h1>"

@get('/search/(?P<query>\w+)')
def search(request,query):
	conn = sqlite3.connect(setting.get("DB"))
	conn.row_factory = json_factory
	cur = conn.cursor()
	offset = (int(request.GET.get('page', '1')) - 1) * 10
	result = cur.execute("""
		select url,title from pages where title like '%s' limit 10 offset %d;
		""" % (('%'+query+'%'),offset)).fetchall()
	return Response(json.dumps(result),content_type="application/json")

def json_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

run_itty(port=80)

