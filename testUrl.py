import unittest
import urlrule

class UrlTest(unittest.TestCase):

	def test_get_abs_url_can_return_abs_url(self):
		base = "http://www.google.com"
		rel_url = "/test.html"
		abs_url = "http://www.google.com/test.html"
		self.assertEqual(urlrule.get_abs_url(base,rel_url),abs_url)

	def test_match_can_block_image_file(self):
		url = "http://www.google.com.tw/image.jpg"
		self.assertFalse(urlrule.match(url))

	def test_match_can_block_uncomplete_url(self):
		url = "www.google.com"
		url2 = "/testhttp://.html"
		url3 = "test.html"
		self.assertFalse(urlrule.match(url),urlrule.match(url2))
		self.assertFalse(urlrule.match(url3))
