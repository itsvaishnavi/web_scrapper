import requests
from bs4 import BeautifulSoup
import scrapy
from scrapy.crawler import CrawlerProcess
from  scrapy.selector  import  Selector
import nltk
from nltk.corpus import stopwords
import concurrent.futures
import time
import logging

class MainClass():
	def __init__(self):
		nltk.download('stopwords')
		self.text = []

	def clean_the_text(self,text:str):
		tokenizer = nltk.RegexpTokenizer(r"\w+")
		remove_symbol_list = tokenizer.tokenize(text)
		tokens_without_stopwords = [word for word in remove_symbol_list if not word in stopwords.words()]
		
		tokens_without_stopwords = [item for item in tokens_without_stopwords if item.isalpha()]

		return tokens_without_stopwords

	def word_counter(self,word_list:list):
		wordfreq = [word_list.count(p) for p in word_list]
		return dict(list(zip(word_list,wordfreq)))

	def sort_words(self,word_counter_dict:dict,descending=True, num_of_elements=10):
		aux = [(word_counter_dict[key], key) for key in word_counter_dict]
		aux.sort()
		if descending:
			aux.reverse()
		return aux[:num_of_elements]

	def data_analysis(self):
		word_counter_dict = self.word_counter(self.text)

		print("-"*100)
		print("10 most used keywords (descending order)")
		print(self.sort_words(word_counter_dict))

		print("-"*100)
		print("10 fewest used keywords (ascending order)")
		print(self.sort_words(word_counter_dict,descending=False))

class BeautifulSoupScrapper(MainClass):
	def get_data_from_url(self,url):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
		r = requests.get(url, headers=headers)
		try:
			if r.status_code == 200:
				logging.info("URL Connection OK")
				soup = BeautifulSoup(r.content)

				tag = soup.body
				
				for string in tag.strings:
					self.text.extend(self.clean_the_text(string.lower()))

			else:
				logging.critical('URL Connection status not OK::%s',url)
		
		except Exception as e:
			logging.exception("Exception occurred")

class ScrapyScrapper(scrapy.Spider):
	text = []
	def __init__(self):
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
		self.extracted_text = []

	def process_extracted_text(self,extracted_text):
		extracted_text = [element for element in extracted_text if ('{' not in element and '}' not in element)]
		tokenizer = nltk.RegexpTokenizer(r"\w+")
		for element in extracted_text:
			if '\n' in element or '\r':
				element = element.replace('\n','')
				element = element.replace('\r','')

			remove_symbol_list = tokenizer.tokenize(element.lower())
			remove_symbol_list = [item for item in remove_symbol_list if item.isalpha() and len(item)>1]
			self.text.extend(remove_symbol_list)
		self.text = [word for word in self.text if not word in stopwords.words()]
		return self.text

	def start_requests(self):
		start_urls = ["https://innospot.de/en",
		"https://www.konux.com/",
		"https://techcrunch.com/",
		"https://www.telekom.com/en",
		"https://www.commerzbank.de/portal/en/englisch/english.html"]

		for url in start_urls:
			yield scrapy.Request(url, headers=self.headers)

	def parse(self,response):
		try:
			body = response.body
			extracted_text = Selector(text = body).css('body ::text').extract()
			self.text = self.process_extracted_text(extracted_text)
		except Exception as e:
			logging.exception("Exception occurred: %s %s %s",response.url, response.status, e)

def main():
	print("This is the official playground for this programming exercise")

	urls =[
		"https://innospot.de/en",
		"https://www.konux.com/",
		"https://techcrunch.com/",
		"https://www.telekom.com/en",
		"https://www.commerzbank.de/portal/en/englisch/english.html"
	]

	MAX_THREADS = 30
	threads = min(MAX_THREADS, len(urls))

	# print('='*100)
	print('=========BeautifulSoup Scrapper=========')
	beautifulSoupScrapper = BeautifulSoupScrapper()
	# start = time.time()
	# for url in urls:
	# 	beautifulSoupScrapper.get_data_from_url(url)
	# end = time.time()

	# print("-"*100)

	# print("Time Required without using multithreading:", str(end-start))

	# print("-"*100)

	start = time.time()
	with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
		executor.map(beautifulSoupScrapper.get_data_from_url, urls)
	end = time.time()
	print("Time Required using multithreading(BeautifulSoup):", str(end-start))

	beautifulSoupScrapper.data_analysis()

	
	print('=========Scrapy Scrapper=========')
	start = time.time()
	process = CrawlerProcess({ 'LOG_LEVEL': 'ERROR'})
	process.crawl(ScrapyScrapper)
	spider = next(iter(process.crawlers)).spider
	process.start()

	mainClass = MainClass()
	mainClass.text=spider.text
	mainClass.data_analysis()
	end = time.time()
	print("Time Required using Scrapy:", str(end-start))

if __name__ == '__main__':
	main()