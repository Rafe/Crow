from xgoogle.search import GoogleSearch,SearchError
from BeautifulSoup import BeautifulSoup
from collections import deque
import urllib

gs = GoogleSearch("quick and dirty")
gs.results_per_page = 10
results = gs.get_results()
quene = deque()
for result in results:
	try:
		print "start parsing..."
		data = urllib.urlopen(result.url)
		soup = BeautifulSoup(data)
		quene.append(result.url)
		#print soup.prettify
	except:
		print "Error"

for url in quene:
	print url
