 #!/bin/env python

'''
Auteur : Xinyi Shen (copyright)
Date : 26 avril 2021

La commande pour lancer le script : streamlit run app.py
Utilisation:
C'est une application streamlit. Il y a deux partie: la première partie est une recherche d'hôtels par les pays.
La deuxième partie est un exemple pour un dictionnaire des langues peu dotées.
'''

import requests
from bs4 import BeautifulSoup
import re

from unidecode import unidecode
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
import time

#La preimère partie

#pré-requis: un pays
#résultat : une partie d'urls de toutes les hôtels de ce pays

def getHotelName(country):
	countryName = country.lower()
	countryName = unidecode(countryName) #normalise les noms de pays
	url = "https://www.nh-hotels.fr/hotels/" + countryName #crée l'url pour accéder la page
	header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',} #passing header info in request
	response = requests.get(url, headers = header) #récupere les infos de l'url
	soup = BeautifulSoup(response.content, 'html.parser') #parse la page html
	hotels = [] 

	#le boucle pour trouver tous les urls de chaque hôtel de ce pays dans la page html
	for eachHotel in soup.find_all("div", class_="block-body"):
		for all_a in eachHotel.find_all("a"): 
			hotelUrl = all_a.get("href") 
			hotels.append(hotelUrl)

	return hotels

#résultat: Les informations utilis des hôtels que le client cherche

def getData():
	info = [] #initialisation d'une liste de dictionnaire pour stocker tous les information de l'hôtels de ce pays
	hotels = getHotelName(country)

	#Pour tous les hôtels dans la liste hotels, on récupére les informations (nom hôtel, eco-friendly ?, étoiles et l'url) puis on stock dans la liste info
	for hotel in hotels:
		url = "https://www.nh-hotels.fr"+hotel
		header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',} #passing header info in request
		response = requests.get(url, headers = header)
		soup = BeautifulSoup(response.content, 'html.parser')		
		#scraping the info
	
   		#hotel name
		title = soup.find('title').contents[0].split("|")[0] #prend le premier élément "title" et récupere le nom de l'hôtel et le pays
		hotel= title

		#eco-friendly ?
		#cherche la présence de l'image eco-friendly dans l'élement "color-primary"
		color_primary = soup.find(id = "services") 

		if color_primary.select_one('img[alt="Eco-friendly"]'):
			ecofriendly = "Oui"
		else:
			ecofriendly =  "Non"

		#étoiles
		#cherche la classe "stars" et compte les étoiles
		stars = soup.find(class_='stars')
		star = len(stars.select('span'))
					
		#url
		plusinfo = url

		#crée un dictionnaire de tous les informations de l'hôtel et ajoute ce dictionnaire à la liste info
		info.append({"Hôtel": hotel, "Eco-friendly": ecofriendly, "Étoiles" : star, "Plus d'informations" : plusinfo})
		#fin boucle

	info = pd.DataFrame(info) #prépare l'affchiage des informations sous la forme graphique avec pandas

	leninfo = len(info) #compte les hôtels dans ce pays
	eco_stars = info[(info[u"Eco-friendly"] == "Oui") &(info[u"Étoiles"] > 3)] #trouve les hôtels qui sont à la fois eco-friendly et plus de trois étoiles
	avec = len(eco_stars) #compte les hôtels eco-friendly et plus de 3 étoiles
	sans = leninfo - avec #compte les hôtels qui sont pas eco-friendly ou moin de 3 étoiles

	return avec, sans, info

#La deuxième partie

#pré-requis: un mot en yemba
#résultat : les informations de ce mot et ses traductions en français

def find_item(word):
	#id_mots : enregistre tous les mots qui vont être extraité comme les valeurs et tous les id des mots sur le page html
	id_mots = {"ad964222-efbb-48a5-bb23-ae9fd606ecdb" : "a","796760e0-1557-4ad0-8daa-139c3c4391f7":"á", "6c97a20b-f271-4f8e-912e-3bfe2db1a494" : "alá pū", "93ecdcd3-c570-4891-94ac-e4c7d449a7bc" : "alēm"}
	#option : afin de scraper le site sans ouvrir le navigateur
	option = webdriver.ChromeOptions() 
	option.add_argument("headless")
	#commence à scraper le site
	driver = webdriver.Chrome(chrome_options=option)
	driver.get("https://ntealan.net")

	time.sleep(2) #wait the page to load

	#close the little window
	try:
		windows = driver.find_element_by_class_name("modal-bottom")
		windows_button = windows.find_element_by_tag_name("button")
		windows_button.click() 
	except:
		pass

	#find the items
	time.sleep(3) #wait the page to load
	#parcourir les éléments dans la page html avec plusieurs méthodes différents afin de trouver les informations pertinnat
	flex_container = driver.find_element_by_class_name("flex-container")
	bar = flex_container.find_element_by_tag_name("app-bar-left")
	barleft = bar.find_element_by_class_name("barLeft")
	listeUL = barleft.find_element_by_xpath("div/div/div/ul")

	for key, value in id_mots.items():
		if word == value: #si le mot cherché par le client est identique que celui dans le dictionnaire
			item = listeUL.find_element_by_id(key) #on recherche le même id dans la page html
			item.click() #entre dans la page d'article
			time.sleep(3) #attend la page active
			main = driver.find_element_by_class_name("main")
			app_central = main.find_element_by_xpath("div/div/div/app-central")
			contenu = app_central.find_element_by_class_name("contenu")
			div= contenu.find_element_by_xpath("div[1]/div[1]/div[1]")
			article = div.find_element_by_class_name("article")
			entry = article.find_element_by_xpath("div[1]")

			#variant
			variant = entry.find_element_by_class_name("variant")
			radical = variant.find_element_by_class_name("radical").text
			forme = variant.find_element_by_class_name("forme").text
			type_ = variant.find_element_by_class_name("type").text

			#category
			category = article.find_element_by_class_name("category")
			cat_part = category.find_element_by_class_name("cat_part").text

			#translation
			translation = article.find_element_by_class_name("translation")
			group_equiv = translation.find_element_by_class_name("group_equiv")
			number = group_equiv.find_element_by_class_name("number").text		
			equivalent = translation.find_elements_by_class_name("equivalent")
			traduction = [] #initialise une liste afin d'ajouter toutes les traductions
			for item in equivalent:			
				traduction.append(item.text)
			lang = translation.find_element_by_class_name("lang").text
			
			#crée un dictionnaire et ajoute tous les informations dedans
			dic = {"radical": radical, "forme":forme, "type":type_, "pos":cat_part, "traduction en français":traduction }
	driver.close()
	return dic	