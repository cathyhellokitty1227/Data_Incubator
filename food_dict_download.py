import urllib
from bs4 import BeautifulSoup
import re
import json
import numpy as np
import pandas as pd 

#Import food words dictionary
url = "http://www.enchantedlearning.com/wordlist/food.shtml"
page = urllib.urlopen(url)
soup = BeautifulSoup(page,'html5lib')

#Return a food list 
food_dict = []
for tr in soup.findAll('tr')[4:-4]:
	tds = tr.findAll('td')
	food_dict.extend([e.text.strip().split('\n') for e in tds])

#Write food list into a json file 
food = [item for sub_list in food_dict for item in sub_list]
with open('food_dict.json', 'w') as f:
	json.dump(food, f)
	f.close()


