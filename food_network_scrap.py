import re
from bs4 import BeautifulSoup
import html5lib
import urllib
import json
import numpy as np
import pandas as pd 
import requests


#Pull Data from foodnetwork 

url = ["http://www.foodnetwork.com/recipes/a-z.123.","http://www.foodnetwork.com/recipes/a-z.A.",\
	  "http://www.foodnetwork.com/recipes/a-z.B.","http://www.foodnetwork.com/recipes/a-z.C.",\
	  "http://www.foodnetwork.com/recipes/a-z.D.", "http://www.foodnetwork.com/recipes/a-z.E.",\
	  "http://www.foodnetwork.com/recipes/a-z.F.", "http://www.foodnetwork.com/recipes/a-z.G.",\
	  "http://www.foodnetwork.com/recipes/a-z.H.","http://www.foodnetwork.com/recipes/a-z.I.",\
	  "http://www.foodnetwork.com/recipes/a-z.J.","http://www.foodnetwork.com/recipes/a-z.K.",\
	  "http://www.foodnetwork.com/recipes/a-z.L.","http://www.foodnetwork.com/recipes/a-z.M.",\
	  "http://www.foodnetwork.com/recipes/a-z.N.","http://www.foodnetwork.com/recipes/a-z.O.",\
	  "http://www.foodnetwork.com/recipes/a-z.P.","http://www.foodnetwork.com/recipes/a-z.Q.",\
	  "http://www.foodnetwork.com/recipes/a-z.R.","http://www.foodnetwork.com/recipes/a-z.S.",\
	  "http://www.foodnetwork.com/recipes/a-z.T.","http://www.foodnetwork.com/recipes/a-z.U.",\
	  "http://www.foodnetwork.com/recipes/a-z.V.","http://www.foodnetwork.com/recipes/a-z.W.",\
	  "http://www.foodnetwork.com/recipes/a-z.XYZ."]

url_page = [2,14,41,67,8,9,19,31,15,5,4,5,13,26,5,9,38,3,24,64,23,1,7,11,3]
url_page_visit = [6,15,15,15,15,15,15,15,15,12,15,12,15,15,15,15,15,12,15,15,15,12,12,15,15]


def category(soup):
	names = soup.findAll('li',{'itemprop':'recipeCategory'})
	if names!=None:
		name_list = [name.get_text() for name in names]
	else:
		print("no such category")
	return name_list 

def ingredients(soup):
	ingredients_html = soup.findAll('li', {'itemprop': "ingredients"})
	return [ingredient.get_text() for ingredient in ingredients_html]


def read_text_alpha(i):
	for j in range(1,url_page[i]+1):
		url_add = url[i] + str(j) + ".html"
		main_page = urllib.urlopen(url_add)
		soup=BeautifulSoup(main_page,'html5lib')
		links = soup.select('span.arrow a[href^=/recipes]')
		#List of sublink
		link = [a.attrs.get('href') for a in links]
		#Go through sublink 
		rand_link_no = np.random.randint(1,len(link)+1,url_page_visit[i])
		link_rand = [link[a-1] for a in rand_link_no]
		Category = []
		Ingredients = []
		Dict = {}
		for sublink in link_rand:
			request = requests.get("http://www.foodnetwork.com"+sublink)
			if request.status_code == 200:
				soup = BeautifulSoup(request.text,'html5lib')
				Category.append(category(soup))
				Ingredients.append(ingredients(soup))
			else:
				print("webpage doesn't exit")
		Dict['cat']=Category
		Dict['ing']=Ingredients

		with open('recipe_{}_{}.json'.format(i,j), 'w') as f:
			json.dump(Dict, f)
	print("link {} is done".format(i))

for m in range(25):
	read_text_alpha(m)