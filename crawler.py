from xgoogle.search import  GoogleSearch,SearchError
from BeautifulSoup import BeautifulSoup
import urllib,urllib2 
from urllib2 import URLError
import urlrule
from PageRepo import PageRepo,DummyRepo

def log(msg):
	print msg

class Url:
	def __init__(self,url,depth):
		self.url = url
		self.depth = depth

class Crawler:
	def __init__(self,query,repo):
		log("initializing...")
		self.query = query
		self.quene = []
		self.paths = set()
		self.count = 20
		self.current = 0
		self.success = 0
		self.repo = repo
	
	def add_quene(self,url,depth=1):
		if url not in self.paths:
			self.paths.add(url)
			self.quene.append(Url(url,depth))

	def pop(self):
		result = None 
		if len(self.quene) > self.current:
			result = self.quene[self.current]
		self.current +=1
		return result

	def start(self,count):
		self.count = count
		gs = GoogleSearch(self.query)
		gs.result_per_page=10
		result = gs.get_results()

		for r in result:
			log("init:" + r.title)
			self.add_quene(r.url)
		
		while self.count > self.success:
			obj_url = self.pop()
			if obj_url == None:
				break
			url = obj_url.url
			depth = obj_url.depth
			try:
				log("crawing:%s in depth:%d " %(url,depth))
				html = urllib2.urlopen(url,timeout=5)
				type = html.headers.get("content-type")
				if urlrule.filter.search(type):
					self.parse_link(obj_url,html)
					self.success +=1
			except URLError as e:
				log(e)
			except Exception as e:
				log(e)

	def parse_link(self,base_url,html):
		soup = BeautifulSoup(html)
		self.repo.save(base_url,soup)
		depth = base_url.depth + 1
		for ref in soup.findAll("a",href=True):
			url = urlrule.get_abs_url(base_url.url,ref["href"])
			if urlrule.match(url):
				self.add_quene(url,depth)

def main():
	c = Crawler("computer",PageRepo()).start(20)

if __name__ == "__main__":
	main()
