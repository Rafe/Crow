Crow is a simple and easy to use crawler.

The target of this project is to implement a crawler with simple jQuery like selector and chain call.

How to run it?

Crow("http://www.yahoo.com").select("a").to(SqlitePipeline()).start(50)

Run it in async mode:

Crow("http://www.yahoo.com").select("a").to(SqlitePipeline()).async_start(50)
Crow.run()

TODO:

unittest
integrate twisted for internet connection
add more jQuery like selector syntax
add @property selector for pipeline:
ex: 
@select("img")
def saveImage(self):
   if elem.size > MB(2):
	save(elem)  
