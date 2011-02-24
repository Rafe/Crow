import codecs
from datetime import datetime

f = codecs.open('log.txt','a',encoding="UTF-8")
def log(msg):
	print msg
	f.write(now()+msg+"\r\n")

def now():
	return datetime.now().strftime("%y%m%d %H%M%S:")
