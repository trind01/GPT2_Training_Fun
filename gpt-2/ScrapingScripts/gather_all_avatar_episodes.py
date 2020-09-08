import requests
from bs4 import BeautifulSoup
import os

all_transcripts = []

base_address_atla = "http://atla.avatarspirit.net/transcripts.php?num="
seasons_atla = [1,2,3] 
episodes_atla = [20,20,21]

base_address_korra = "http://korra.avatarspirit.net/transcripts.php?num="
seasons_korra = [1,2,3,4] 
episodes_korra = [12,14,13,13]

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def gather_episode_quotes(quote_list,base_address,season,ep):
	full_address = base_address + str(season) +  f"{ep:02d}"
	print(full_address)
	r = requests.get(full_address)
	soup = BeautifulSoup(r.text, 'html.parser')
	episode_transcripts = ""		
	for bq in soup.find_all('blockquote'):
		start_tag = bq.find_all('b')[0]
		tag_type = type(start_tag)
		while(start_tag.next_sibling):
			if start_tag.name:
				if start_tag.name == 'br':
					episode_transcripts = episode_transcripts + "\n"
				elif not(start_tag.contents):
					start_tag = start_tag.next_sibling
					continue
				elif type(start_tag.contents[0]) == tag_type:
					child_tag = start_tag.contents[0]
					while(type(child_tag.contents[0]) == tag_type):
						child_tag = child_tag.contents[0]
					episode_transcripts = episode_transcripts + child_tag.contents[0]
				else:
					episode_transcripts = episode_transcripts + start_tag.contents[0]
			else:
				episode_transcripts = episode_transcripts + start_tag
			start_tag = start_tag.next_sibling
	quote_list.append(episode_transcripts)

def gather_season_quotes(quote_list,base_address,season,num_ep):
	for i in range(num_ep):
		gather_episode_quotes(quote_list,base_address,season,i+1)

for s_num in range(len(seasons_atla)):
	gather_season_quotes(all_transcripts,base_address_atla,seasons_atla[s_num],episodes_atla[s_num])

for s_num in range(len(seasons_korra)):
	gather_season_quotes(all_transcripts,base_address_korra,seasons_korra[s_num],episodes_korra[s_num])

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '..\\ScrapedData\\avatar_episodes.txt')

with open(filename, "w", encoding="utf-8") as f:
	for quote in all_transcripts:
		f.write(quote)
		f.write("\n <|endoftext|> \n")