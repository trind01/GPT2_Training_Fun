from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import requests

base_transcript_url = 'https://factba.se'
speech_list_url = 'https://factba.se/transcripts/speeches'
speech_list = []

dirname = os.getcwd() + '\\ScrapingScripts\\phantomjs.exe'
driver = webdriver.PhantomJS(executable_path=dirname)
driver.get(speech_list_url)
lastHeight = driver.execute_script("return document.body.scrollHeight")
pause = 2
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight

html = driver.page_source
soup = BeautifulSoup(html, "html5lib")

for li in soup.find_all('li'):
	for a in li.find_all('a',href=True):
		if '/transcript/' in a['href']:
			if not(a['href'] in speech_list):
				speech_list.append(a['href']) 

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '..\\ScrapedData\\trump_speeches.txt')
with open(filename, "w", encoding="utf-8") as f:
	for speech in speech_list:
		print(speech)
		url = base_transcript_url + speech
		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		for div in soup.find_all("div", class_="transcript-text-block"):
			f.write(div.a.text)
			f.write('\n -------------------------------- \n')
		f.write("\n <|endoftext|> \n")