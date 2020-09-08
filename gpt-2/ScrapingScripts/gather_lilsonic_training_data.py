import requests
from bs4 import BeautifulSoup

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

r = requests.get('https://www.fanfiction.net/u/3140134/Lil-Soniq')
soup = BeautifulSoup(r.text, 'html.parser')


stories = []
for div in soup.find_all('div'):
	div_class = div.get('class')
	if not div_class:
		continue
	for d_class in div_class:
		if d_class == 'mystories':
			for content in div.children:
				try:
					if content.attrs['class'] and content.attrs['class'][0] == 'stitle':
						stories.append(content.attrs['href'])
				except:
					continue

site = 'https://www.fanfiction.net'

num_stories = len(stories)
story_num = 0

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '..\\ScrapedData\\Lil-Soniq.txt')

with open(filename, "w", encoding="utf-8") as f:
	for story in stories:
		print("Story " + str(story_num) + " of " + str(num_stories))
		full_path = site + story
		r = requests.get(full_path)
		story_text = BeautifulSoup(r.text, 'html.parser')
		select = story_text.find_all('select')
		pages = 0
		for s in select:
			for option in s.find_all('option'):
				pages += 1
		pages = int(pages / 2)
		story_id = story.split('/')[2]
		story_name = story.split('/')[4]

		for i in range(pages):
			full_path = site + '/s/' + story_id + "/" + str(i+1) + "/" + story_name
			r = requests.get(full_path)
			story_text = BeautifulSoup(r.text, 'html.parser')
			print(story_name + " Page " + str(i) + " of " + str(pages))
			for text in story_text.find_all('p'):
					em_list = text.find_all('em')
					if not em_list:
						parsed_text = remove_html_tags(str(text.contents[0])) + '\n\n'
						f.write(parsed_text)
		f.write("<|endoftext|>\n\n")
		story_num += 1
