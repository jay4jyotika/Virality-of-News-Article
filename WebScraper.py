import bs4 as bs
import urllib.request
import re
import os
import datetime
import string
import json
'''WebScraper - CNN International.
This WebScraper is designed to scrape the content from the CNN-International URLS which were gathered
from the WebCrawler.
'''

saveLocation = "articles/"
createTextDoc = False
body_text = ""
para_string = ""

counter = 1

with open("links/_Wanted_URLS.txt") as f:
	url_list = f.readlines()

url_list = [x.strip() for x in url_list]

for url in url_list[0: ]:
	print (url)
	try:
		#Selecting URL
		sauce = urllib.request.urlopen(url).read()
		soup =  bs.BeautifulSoup(sauce, 'lxml')		
		
		#Find title 
		title = soup.h1.string
	
		#Finding date of article 
		article_date = soup.find_all("meta", {"name": "pubdate"})
		article_ID = re.search("\"(.*?)\"",str(article_date))[0]
		article_ID = re.sub('[!#?,.:";-]', '', article_ID)
		print(article_ID)

		article_date = re.findall(r'(\d+-\d+-\d+)', str(article_date))
		
		article_date = article_date[0]
		article_date = re.sub(r'-', '/', article_date)

		try:
			for item in soup.find_all('div',{"class":"zn-body__paragraph"}):
				paragraph = re.findall(r'>(.*?)<', str(item))
				for i in paragraph:
					para_string = para_string + i
				body_text = body_text + para_string	
				para_string = ""
		except Exception as e:			
			print("ERROR SCRAPING BODY TEXT!!" + str(e))
				
		content = "#" + title + "#. " + body_text
		content = re.sub(r'<(.*?)>', '', content)


		try:
			my_details = {
				'article_ID': article_ID,
				'publish_date': article_date,
				'title': title,
				'body': content
			}

			with open('articles/{}.json'.format(counter), 'w') as json_file:
				json.dump(my_details, json_file)
		except Exception as e:
			print("URL PRESENT: " + str(e))

		body_text = ""
		content = ""
		title = ""		
		print (counter)
		counter += 1
	except Exception as e:			
		print("MAIN SCRAPE ERROR!!" + str(e))

