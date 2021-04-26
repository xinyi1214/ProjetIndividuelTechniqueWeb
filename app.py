import streamlit as st
from scrape import getHotelName, getData, find_item

#Création de l'app

st.markdown("""
	<style>
	body{
	background:#F8FEFE
	}
	</style>
	""", unsafe_allow_html=True) #change la couleur du backgroud 

#crée un sidebar pour faire une petite présentation de cette application et ajoute un choix entre deux pages
st.sidebar.header("À propos")
st.sidebar.write("Cette application vous propose deux options.")
st.sidebar.write("La première, les hôtels Eco-friendly de l'Hotel Group.")
st.sidebar.write("La deuxième, un dictionaire des langues peu-dotées.")
st.sidebar.write("")
status = st.sidebar.radio("Quelle page voulez-vous voir ?", ("Hôtels Eco-friendly", "Dictionaire des langues peu-dotées"))
st.sidebar.write("")
st.sidebar.subheader("Auteur:")
st.sidebar.write("Xinyi Shen")

#commence à créer la première page
if status =="Hôtels Eco-friendly":
	st.title("Hôtels Eco-friendly")
	st.subheader("Dans cette page, nous proposons les hôtels Eco-friendly de l'Hotel Group pour faciliter votre voyage.")
	st.text("")
	st.info("Vous pouvez chosir le pays dans lequel vous voulez voyager, nous rechercherons pour vous les informations pertinentes puis nous vous affichons dans un graphique les hôtels Eco-friendly et les hôtels non Eco-friendly.")
	st.text("")
	#ajoute le module de recherche
	country = st.text_input("Pays dans lequel vous voulez voyager (en français)")
	if country != '':
		try:
			avec, sans, info = getData()
			st.subheader("Tous les hôtels dans ce pays:")
			st.table(info) #insére le tableau qu'on a crée par pandas
			st.text("")
			plt.bar(["Hôtels non Eco-friendly", "Hôtels Eco-friendly"], [sans, avec])
			st.subheader("Nous comparons les hôtels qui ont plus de 3 étoiles:")
			st.set_option('deprecation.showPyplotGlobalUse', False)
			st.pyplot() #ajoute la graphique

		except:
			st.error("Désolé, l'Hotel Group ne propose pas d'hôtels dans ce pays. ")

#commence à créer la deuxième page
else:
	if status == "Dictionaire des langues peu-dotées":
		st.title("Dictionaire des langues peu-dotées")
		st.text("")
		st.info('En 2007, le cabinet de recherche Computer Industry Almanac1 estimait le nombre d’ordinateurs personnels en circulation dans le monde a un milliard de machines, soit un ordinateur pour 6,6 personnes en moyenne. Ce chiffre est accompagné de tendances qui montrent que la progression de l’informatisation des foyers diminue légèrement dans les pays dits développés, et augmente très fortement depuis quelques années dans les pays en voie de développement, nouveaux moteurs de la croissance de ce march´e. Dès lors, le développement rapide de technologies de traitement numérique du langage, dans les langues de ces pays, est un enjeu essentiel. (Thomas Pellegrini. Transcription automatique de langues peu dotées. Informatique [cs]. Université Paris Sud - Paris XI, 2008. Français. fftel-00619657f)')

		st.write("Dans ce cas, nous introduisons un dictionaire en ligne qui présente les langues peu-dotées, par exemple, yemba, swahili, yangben, etc.")
		st.text("")
		st.write("Pour vous montrer ce dictionaire, nous extrayons quelques exemples en yemba.")
		st.text("")
		#crée un choix pour représente les articles qui sont extrait
		word = st.selectbox("Vous voulez chosir quel mot yemba ?",("a", "á", "alá pū", "alēm"))
		if word != '':
			try:
				dic = find_item(word)
				for key, value in dic.items():
					st.info(
						'''
						{} : {}
	 					'''.format(key, value)
	 					) #affiche le dictionnare
			except:
				st.error("Erreur de connexion. L'accès au siteweb du dictionaire étant difficile, il est normal de devoir reessayer plusieurs fois pour avoir un résultat. Merci de reessayer.")
		st.write("")
		st.text("Pour plus d'informations:" )
		st.markdown(
    """<a href="https://ntealan.net">https://ntealan.net</a>""", unsafe_allow_html=True,
) #affiche l'url du site original