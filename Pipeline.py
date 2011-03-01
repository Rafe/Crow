import sqlite3
import datetime
import sys
from log import log
import setting

class DummyPipeline:
	def process(self,url,page):
		pass
	
	def size(self):
		return 0
	
	def session_size(self):
		pass

class SqlitePipeline:

	def __init__(self):
		self.conn = sqlite3.connect(setting.get("DB"))
		self.readed = 0
		try:
			self.conn.execute("""
				create table pages (
					id INTEGER PRIMARY KEY,
					title text,
					html text,
					content_hash integer,
					url text,
					depth real,
					created_date text);
			""")
			self.conn.execute("""
				create index pages_title on pages(title desc);
				create index pages_url on pages(url desc);
			""")
		except:
			pass

	def process(self,crow,link,page):
		content = unicode(page)
		self.conn.execute(
				"insert into pages(html,title,content_hash,url,depth,created_date) values(?,?,?,?,?,?);",
				(content,unicode(page.title.text),
					hash(content),
					link.url,
					link.depth,
					datetime.datetime.now()))
		self.conn.commit()
		self.readed += sys.getsizeof(content)
		log("[Crow%d save]%s" %(crow.cid,link.url))

	def size(self):
		return float(self.conn.execute("select sum(length(html)) from pages;").fetchone()[0])
	
	def session_size(self):
		return float(self.readed)
	
	def truncate(self,content, length=50, suffix='...'):
		if len(content) <= length:
			return content
		else:
			return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix
