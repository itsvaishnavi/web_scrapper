"""
This script is for scraping the data using BeautifulSoup library.
Usage: python solution1.py
"""
# Importing essential libraries
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import concurrent.futures
import time
import logging

class MainClass():
	def __init__(self):
		nltk.download('stopwords')
		self.text = []

	# function to clean the scraped text
	def clean_the_text(self,text:str):
		"""
		Parameters:
		text : str type
		"""

		# tokenizer to split the input text into words and remove punctuation symbols
		tokenizer = nltk.RegexpTokenizer(r"\w+")

		# Convert the input text to list using the tokenizer
		remove_symbol_list = tokenizer.tokenize(text)

		# Remove stopwords from remove_symbol_list
		tokens_without_stopwords = [word for word in remove_symbol_list if not word in stopwords.words()]
		
		# Keep alphabetical strings in tokens_without_stopwords
		tokens_without_stopwords = [item for item in tokens_without_stopwords if item.isalpha()]

		return tokens_without_stopwords

	# function to record the frequency of words
	def word_counter(self,word_list:list):
		"""
		Parameters:
		word_list : list type
		"""

		# Count the frequency of word in word_list
		wordfreq = [word_list.count(p) for p in word_list]

		# Return the output in dictionary format {word:word_count}
		return dict(list(zip(word_list,wordfreq)))

	# function to sort the word frequency dictionary 
	def sort_words(self,word_counter_dict:dict,descending=True, num_of_elements=10):
		"""
		Parameters:
		word_counter_dict : dict type

		Optional parameters:
		descending : bool type (default = True)
		num_of_ements : int (represents number of elements to return after sorting the word_counter_dict)
		"""

		# Form a list from word_counter_dict (format: [(word_count,word)])
		aux = [(word_counter_dict[key], key) for key in word_counter_dict]

		# Sort the list in ascending order
		aux.sort()

		if descending:
			# List formatted in descending order
			aux.reverse()
		
		# Return the output
		return aux[:num_of_elements]

	# function to get the final analysis
	def data_analysis(self):
		# Record the frequency of words
		word_counter_dict = self.word_counter(self.text)

		print("-"*100)
		print("10 most used keywords (descending order)")
		print(self.sort_words(word_counter_dict))

		print("-"*100)
		print("10 fewest used keywords (ascending order)")
		print(self.sort_words(word_counter_dict,descending=False))

# BeautifulSoupScrapper class inherited from MainClass
class BeautifulSoupScrapper(MainClass):
	# function to scrape the data from url 
	def get_data_from_url(self,url:str):
		"""
		Parameters:
		url : str type (URL)
		"""

		# headers parameter to request the data from URL
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
		
		# request the data from URL
		r = requests.get(url, headers=headers)
		try:
			# If the response status is OK
			if r.status_code == 200:
				logging.info("URL Connection OK")

				# Get the html text from the response
				soup = BeautifulSoup(r.content)

				# Extract data from <body> tag
				tag = soup.body
				
				# Iterate inside the <body> tag to extract the text
				"""
				example: 
				<body>
				<div> <p> Sample text </p> </div>
				</body>
				"""
				for string in tag.strings:
					self.text.extend(self.clean_the_text(string.lower()))

			else:
				logging.critical('URL Connection status not OK::%s',url)
		
		except Exception as e:
			logging.exception("Exception occurred")

def main():
	print("This is the official playground for this programming exercise")

	# URL list
	urls =[
		"https://innospot.de/en",
		"https://www.konux.com/",
		"https://techcrunch.com/",
		"https://www.telekom.com/en",
		"https://www.commerzbank.de/portal/en/englisch/english.html"
	]

	# Instantiating BeautifulSoupScrapper class
	beautifulSoupScrapper = BeautifulSoupScrapper()

	# Approach 1: Scraping data without multithreading (sequential execution)
	start = time.time()

	# Iterate over urls list
	for url in urls:
		# Call get_data_from_url() to scrape the data from url
		beautifulSoupScrapper.get_data_from_url(url)
	end = time.time()

	# Analysis of the scraped data
	beautifulSoupScrapper.data_analysis()

	print("-"*100)

	print("Time Required without using multithreading:", str(end-start))

	beautifulSoupScrapper.text.clear()

	print("-"*100)

	# Approach 2: Scraping data with multithreading (parallel execution)

	MAX_THREADS = 30
	threads = min(MAX_THREADS, len(urls))

	start = time.time()
	with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
		# Runs get_data_from_url() in parallel for all the urls
		executor.map(beautifulSoupScrapper.get_data_from_url, urls)
	end = time.time()
	print("Time Required using multithreading:", str(end-start))


	# Analysis of the scraped data
	beautifulSoupScrapper.data_analysis()

if __name__ == '__main__':
	main()