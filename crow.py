from xgoogle.search import  GoogleSearch,SearchError
from BeautifulSoup import BeautifulSoup
import urllib,urllib2 
from urllib2 import URLError
import urlrule
from log import log
from Pipeline import SqlitePipeline
from twisted.internet import reactor

class ExecutionQueue:
	def __init__(self,queue=[]):
		self.queue = queue
		self.current = 0
		self.paths = set()

	def size(self):
		return len(self.queue)

	def add_link(self,link):
		if link.url not in self.paths:
			self.paths.add(link.url)
			self.queue.append(link)
	
	def get_next_link(self):
		if self.size() > self.current:
			result = self.queue[self.current]
			self.current +=1
			return result
		else:
			return None

class Link:
	def __init__(self,url,depth):
		self.url = url
		self.depth = depth

class Crow:
	cid = 0
	def __init__(self,url):
		Crow.cid += 1
		self.cid = Crow.cid
		log("[init Crow%d]" % self.cid)
		self.async = False
		self.queue = ExecutionQueue([Link(url,1)])
		self.count = 20
		self.success = 0
	
	def to(self,pipe):
		self.pipe = pipe
		return self

	def select(self,rule):
		self.rule=rule
		return self

	def start(self,count):
		if(self.async == True):
			self.pipe = SqlitePipeline()

		if(self.pipe==None or self.rule==None):
			print "please set the target and rules"
		self.count = count
		
		while self.count > self.success:
			link = self.queue.get_next_link()
			if link == None:
				break
			url = link.url
			depth = link.depth
			try:
				log("[Crow%d crawling]%s in depth:%d " %(self.cid,url,depth))
				#getPage(url).addCalback(self.pipe.process)
				html = urllib2.urlopen(url,timeout=5)
				type = html.headers.get("content-type")
				if urlrule.filter.search(type) and html.getcode() == 200:
					self.parse_link(link,html)
					self.success +=1
			except URLError as e:
				log(str(e))
			except Exception as e:
				log(str(e))
		return self.stat()

	def stat(self):
		MB = lambda x:x/1024/1024
		log("[Crow%d]total %.2f MB data in database" % (self.cid,MB(self.pipe.size())))
		log("[Crow%d]%.2f MB saved in this session" % (self.cid,MB(self.pipe.session_size())))
		return self

	def parse_link(self,base_url,html):
		soup = BeautifulSoup(html)
		self.pipe.process(self,base_url,soup)
		depth = base_url.depth + 1
		for ref in self.rule(soup):
			url = urlrule.get_abs_url(base_url.url,ref["href"])
			if urlrule.match(url):
				self.queue.add_link(Link(url,depth))
	
	def async_start(self,count):
		self.async = True
		reactor.callInThread(self.start,count)
	
	@staticmethod
	def run():
		reactor.run()
		

def main():
	#the hardcoded search query:
	gs = GoogleSearch("computer")
	gs.result_per_page=10
	results = gs.get_results()

	for r in results:
		Crow(r.url).select(lambda s:s.findAll("a",href=True)
				).to(SqlitePipeline()).async_start(50)

	Crow.run()
	f.close()

if __name__ == "__main__":
	main()
