import re
from urlparse import urljoin

positive_rules = [
		re.compile(r"^http://")
		]

negative_rules = [
		re.compile(r"(\.jpg|\.jpeg|\.png|\.gif)$",re.I)
		]

filter = re.compile(r"text/html")

def match(url):
	for r in positive_rules:
		if not r.search(url):
			return False
	
	for r in negative_rules:
		if r.search(url):
			return False
	return True

def get_abs_url(domain,url):
	return urljoin(domain,url)
