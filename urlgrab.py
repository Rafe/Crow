import urllib, htmllib, formatter
import sys,io

class LinkParser(htmllib.HTMLParser):
	def __init__(self, formatter) :        # class constructor
		htmllib.HTMLParser.__init__(self, formatter)  # base class constructor
   		self.links = []        # create an empty list for storing hyperlinks

	def start_a(self, attrs) :  # override handler of <A ...>...</A> tags
    	# process the attributes
		if len(attrs) > 0:
			for attr in attrs:
				if attr[0] == "href" :         # ignore all non HREF attributes
					self.links.append(attr[1]) # save the link info in the list

	def get_links(self) :     # return the list of extracted links
		return self.links
	

def search_keyword(keyword):
	format = formatter.NullFormatter()       # create default formatter *
	htmlparser = LinkParser(format)  # create new parser object

	data = urllib.urlopen("http://www.google.com/search?hl=en&q="+keyword+"&btnG=Google+Search")
	print data.read()
	htmlparser.feed(data.read())
	return htmlparser.get_links()

links = search_keyword("computer")
for link in links:
	print link
#STERN.NYU.EDU/~ja1517/data
