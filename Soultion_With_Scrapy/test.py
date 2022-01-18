"""
This script is for unit testing purpose.
Usage: python -m unittest
"""

# Importing essential libraries
import requests
import unittest
import nltk
from nltk.corpus import stopwords
import re
import string
from playground import DataAnalysisClass #Importing class 'DataAnalysisClass' from the python file with name 'playground.py'

# class Test inherited from unittest.TestCase
class Test(unittest.TestCase):
	# Test 1: to check the functions written in DataAnalysisClass of playground.py
	def test_functions_in_DataAnalysisClass(self):
		d = DataAnalysisClass()

		test_text = """
		Web scraping, web harvesting, or web data extraction is data scraping used for extracting data 
		from websites. The web scraping software may directly access the World Wide Web using the Hypertext Transfer Protocol or a web browser. While web scraping can be done manually by a software user, the term typically refers to automated processes implemented using a bot or web crawler. It is a form of copying in which specific data is gathered and copied from the web, typically into a central local database or spreadsheet, for later retrieval or analysis.
		"""
		
		# ---------------Text processing-------------------------------
		
		regex = re.compile('[%s]' % re.escape(string.punctuation))

		test_text = regex.sub('', test_text)
		
		extracted_text = test_text.lower().split()
		# -------------------------------------------------------------
		assert isinstance(extracted_text,list) == True

		word_counter_dict = d.word_counter(extracted_text)
		assert isinstance(word_counter_dict,dict) == True

		assert word_counter_dict['web']==9
		assert word_counter_dict['scraping']== 4

		desc_sorted_words = d.sort_words(word_counter_dict)
		assert desc_sorted_words[0][1] == 'web'
		assert isinstance(desc_sorted_words,list) == True

		asc_sorted_words = d.sort_words(word_counter_dict,descending=False)
		assert asc_sorted_words[0][1] == 'access'
		assert isinstance(asc_sorted_words,list) == True

if __name__ == '__main__':
	unittest.main()