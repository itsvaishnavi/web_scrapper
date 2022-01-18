"""
This script is for scraping the data using BeautifulSoup library.
Usage: python solution2.py
"""
# Importing essential libraries
import scrapy
from scrapy.crawler import CrawlerProcess
from  scrapy.selector  import  Selector
import logging
import nltk
from nltk.corpus import stopwords

# Remove unwanted logs from scrapy
logging.getLogger('scrapy').setLevel(logging.WARNING)

# TestSpider class inherited from scrapy.Spider
class TestSpider(scrapy.Spider):
  # variable to gather the processed text in the list format
  text = []

  def __init__(self):
    # headers variable for the url
    self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    nltk.download('stopwords')

  # function to clean the scraped text
  def process_extracted_text(self,extracted_text:list):
    """
    Parameters:
    extracted_text : list type
    """

    # To remove the javascript code elements from the scraped text
    extracted_text = [element for element in extracted_text if ('{' not in element and '}' not in element)]
    
    # tokenizer to split the input text into words and remove punctuation symbols
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    for element in extracted_text:
      if '\n' in element or '\r':
        element = element.replace('\n','')
        element = element.replace('\r','')

      # Convert the input text to list using the tokenizer
      remove_symbol_list = tokenizer.tokenize(element.lower())

      # Keep alphabetical strings in remove_symbol_list
      remove_symbol_list = [item for item in remove_symbol_list if item.isalpha() and len(item)>1]

      # Add remove_symbol_list to text variable
      self.text.extend(remove_symbol_list)

    # Remove the stopwords from the text variable
    self.text = [word for word in self.text if not word in stopwords.words()]

  def start_requests(self):
    # URLS to data scrape
    start_urls = ["https://innospot.de/en",
      "https://www.konux.com/",
      "https://techcrunch.com/",
      "https://www.telekom.com/en",
      "https://www.commerzbank.de/portal/en/englisch/english.html"]

    for url in start_urls:
      yield scrapy.Request(url, headers=self.headers)

  def parse(self,response):
    try:
      # Extract the body from response
      body = response.body
      extracted_text = Selector(text = body).css('body ::text').extract()

      # Process the extracted text
      self.process_extracted_text(extracted_text)

    except Exception as e:
      logging.exception("Exception occurred: %s %s %s",response.url, response.status, e)

# Class to analyze scraped data
class DataAnalysisClass():

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
  def data_analysis(self,text):
    """
    Parameters:
    text : list type
    """

    # Record the frequency of words
    word_counter_dict = self.word_counter(text)

    print("-"*100)
    print("10 most used keywords (descending order)")
    print(self.sort_words(word_counter_dict))

    print("-"*100)
    print("10 fewest used keywords (ascending order)")
    print(self.sort_words(word_counter_dict,descending=False))

if __name__ == "__main__":
  process = CrawlerProcess({ 'LOG_LEVEL': 'ERROR'})
  process.crawl(TestSpider)
  spider = next(iter(process.crawlers)).spider
  process.start()

  dataAnalysisClass = DataAnalysisClass()
  dataAnalysisClass.data_analysis(spider.text)