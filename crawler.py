from xgoogle.search import  GoogleSearch,SearchError
from BeautifulSoup import BeautifulSoup
import urllib,urllib2,re 

def log(msg):
	print msg

class Crawler:
	
	def __init__(self,query):
		log("initializing...")
		self.query = query
		self.quene = []
		self.paths = {}
		self.count = 20
		self.current = 0
	
	def add_quene(self,url):
		self.quene.append(url)

	def pop(self):
		result = ""
		if len(self.quene) > self.current:
			result = self.quene[self.current]
			self.current +=1
		return result

	def search(self,count):
		self.count = count
		rule = re.compile(r"http://*")
		goog = GoogleSearch(self.query)
		goog.results_per_page=self.count
		self.result = goog.get_results()

		for r in self.result:
			log("init:" + r.title)
			self.add_quene(r.url)
		
		while self.count > self.current:
			url = self.pop()
			log("crawing:"+url)
			
			if rule.match(url):
				html = urllib.urlopen(url)
				self.parse_a(url,html)
	
	def inspect(self):
		if self.result:
			for r in self.result:
				print r.title
				print r.url
	
	def parse_a(self,base_url,html):
		self.soup = BeautifulSoup(html)
		for ref in self.soup.findAll("a","href"):
			log(ref)
			self.quene.append(ref["href"])

c = Crawler("computer")
c.search(20)
