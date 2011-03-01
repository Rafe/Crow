
2011s Web Search Engine assignment#1
Arthor: Te-Chun Chao

Project Structure:

crow.py          -- Main Crawler engine
urlrule.py       -- Rules written by regex to filter links
Pipeline.py      -- The pipeline class use to process the web page Item,
                    save the content to sqlite3 database.
log.py           -- The log module use to save log and output on console
setting.py       -- The setting file for database name and others.
server.py        -- It open a demo server interface which can be access from localhost:80
                    it shows a basic search function and can view the crawled pages.
testUrl.py       -- Test cases for urlrule.py
BeautifulSoup.py -- The beautiful Soup parsing library. http://www.crummy.com/software/BeautifulSoup/

xgoogle          -- XGoogle library, https://github.com/pkrumins/xgoogle
itty             -- Simple web framework, https://github.com/toastdriven/itty
html             -- static html files for web server.

dependency	
Python 2.7
Twisted		 -- This project use Twistedmatrix Library,http://twistedmatrix.com/trac/
		    you need to install it to run asynchronously

How to run it?

1. setting up a crowler:
Crow("http://poly.edu"
	).select(lambda s:s.findAll("a",href="true") # the parse query for BeautifulSoup
	).to(SqlitePipeline()).start(50)

2. run it async:
Crow("http://poly.edu"
	).select(lambda s:s.findAll("a",href="true")
	).to(SqlitePipeline()).start_async(50)
Crow.run()

3. use xgoogle library, search keyword and run it

gs = GoogleSearch("computer")
results = gs.get_results()

for r in results:
	Crow(r.url).select(lambda s:s.findAll("a",href=True)
		).to(SqlitePipeline()).start(50)


 

Q for assignment:

1.Downloading Pages:
It use the urllib.urlopen() to download the pages.
Timeout is setting to 5 second.

2.Parsing:
The html file is parsed by BeautifulSoup Library, 
it's great parsing ability reduce a lots of difficulty.

The query is injected to crawler by calling .select()
for example, if you want to parse every link on the page,
you should query the BeautifulSoup Object like this:

soup.findAll("a",href=True)

for the crawler, you have to inject this query to it by calling:

c = Crow(url)
c.select(lambda s:s.findAll("a",href=True))

3.Ambiguity of URLs:

The url ambiguity is handled by urllib.urljoin

4.Different Type of Files:

The urlrule.py will filter the filetype in URL.

eg: //img1.jpg , //shrak.mov

and the crawler will also check the response header,
make sure the filetype is text/html

5.Stack and Queues:
6.Checking for Earlier Visits:

The ExecutionQuene class in crow.py is handling these two parts,
it have a set() object for recording the visited paths
and a quene to implement to BFS search.

7.Password-Protected Pages:
The crawler will check to responce code, ignore any response other than
200 (which might also ignore some 303 redirect response)



