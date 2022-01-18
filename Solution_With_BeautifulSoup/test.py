"""
This script is for unit testing purpose.
Usage: python -m unittest
"""

# Importing essential libraries
import requests
import unittest
from playground import MainClass #Importing class 'MainClass' from the python file with name 'playground.py'

# class Test inherited from unittest.TestCase
class Test(unittest.TestCase):
	start_urls = ["https://innospot.de/en",
		"https://www.konux.com/",
		"https://techcrunch.com/",
		"https://www.telekom.com/en",
		"https://www.commerzbank.de/portal/en/englisch/english.html"]

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
	# Test 1: to check the Api response status code
	def test_api_status(self):
		for url in self.start_urls:
			self.resp=requests.get(url, headers=self.headers)
			self.assertTrue(self.resp.status_code == 200, 'API not working. Check the url '+url)

	# Test 2: to check the Api response content
	def test_api_content(self):
		for url in self.start_urls:
			self.resp=requests.get(url, headers=self.headers)
			self.assertTrue('text/html' in self.resp.headers['Content-Type'], 'API response is not text/html')

	# Test 3: to check the functions written in MainClass of playground.py
	def test_functions_in_Main_Class(self):
		m = MainClass()

		test_text = """
		Web scraping, web harvesting, or web data extraction is data scraping used for extracting data 
		from websites. The web scraping software may directly access the World Wide Web using the Hypertext Transfer Protocol or a web browser. While web scraping can be done manually by a software user, the term typically refers to automated processes implemented using a bot or web crawler. It is a form of copying in which specific data is gathered and copied from the web, typically into a central local database or spreadsheet, for later retrieval or analysis.
		"""

		cleaned_text = m.clean_the_text(test_text.lower())

		assert isinstance(cleaned_text,list) == True

		word_counter_dict = m.word_counter(cleaned_text)
		assert isinstance(word_counter_dict,dict) == True
		assert word_counter_dict['web']==9
		assert word_counter_dict['scraping']== 4

		desc_sorted_words = m.sort_words(word_counter_dict)
		assert desc_sorted_words[0][1] == 'web'
		assert isinstance(desc_sorted_words,list) == True

		asc_sorted_words = m.sort_words(word_counter_dict,descending=False)
		assert asc_sorted_words[0][1] == 'access'
		assert isinstance(asc_sorted_words,list) == True

if __name__ == '__main__':
	unittest.main()