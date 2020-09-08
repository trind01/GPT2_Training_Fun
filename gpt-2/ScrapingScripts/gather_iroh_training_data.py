import requests
from bs4 import BeautifulSoup

iroh_quotes = []

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
	for bq in soup.find_all('blockquote'):
		start_tag = bq.find_all('b')[0]
		while(start_tag.next_sibling):
			if not(start_tag.name) or (not('Iroh' in start_tag.contents) and not('Uncle Iroh:' in start_tag.contents)):
				start_tag = start_tag.next_sibling
				continue
			curr_tag = start_tag.next_sibling
			prev_tag = start_tag.previous_sibling
			quote = start_tag.contents[0]
			#Get all the quote after
			while True:
				if curr_tag.name == 'br' and curr_tag.next_sibling.name == None and curr_tag.next_sibling.next_sibling.name == 'br':
					break;
				if curr_tag.name:
					if curr_tag.name == 'br':
						quote = quote + "\n"
					else:
						quote = quote + curr_tag.contents[0]
				else:
					quote = quote + curr_tag
				curr_tag = curr_tag.next_sibling
			#Get all the quote before
			while True:
				if prev_tag.name == 'br' and prev_tag.next_sibling.name == None and prev_tag.next_sibling.next_sibling.name == 'br':
					break;
				if prev_tag.name != 'u':
					break
				if prev_tag.name == 'br':
					quote = "\n" + quote
				elif prev_tag.name:
					quote = prev_tag.contents[0] + quote
				else:
					quote = prev_tag + quote
				prev_tag = prev_tag.previous_sibling
			if prev_tag.name == 'b' or prev_tag.name == 'i':
				quote = prev_tag.contents[0] + quote

			quote = quote.replace('  ','')
			quote_list.append(quote)
			start_tag = curr_tag

def gather_season_quotes(quote_list,base_address,season,num_ep):
	for i in range(num_ep):
		gather_episode_quotes(quote_list,base_address,season,i+1)

for s_num in range(len(seasons_atla)):
	gather_season_quotes(iroh_quotes,base_address_atla,seasons_atla[s_num],episodes_atla[s_num])

for s_num in range(len(seasons_korra)):
	gather_season_quotes(iroh_quotes,base_address_korra,seasons_korra[s_num],episodes_korra[s_num])

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '..\\ScrapedData\\iroh_quotes.txt')

with open(filename, "w", encoding="utf-8") as f:
	for i in range(100):
		print("Writing quotes :" + str(i))
		for quote in iroh_quotes:
			f.write(quote)
			f.write("\n <|endoftext|> \n")
