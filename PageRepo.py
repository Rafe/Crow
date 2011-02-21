import sqlite3
import datetime

class DummyRepo:
	def save(self,url,page):
		pass

class PageRepo:

	def __init__(self):
		self.conn = sqlite3.connect('CrawlerBase')
		try:
			self.conn.execute("""
				create table pages (
					id INTEGER PRIMARY KEY,
					html text,
					url text,
					depth real,
					created_date text)
			""")
		except:
			pass

	def save(self,url,page):
		self.conn.execute("insert into pages(html,url,depth,created_date) values(?,?,?,?);",
				(unicode(page),url.url,url.depth,datetime.datetime.now()))
		self.conn.commit()
		print("saved: "+url.url)

	def find(self,id):
		pass

	def size(self):
		pass
