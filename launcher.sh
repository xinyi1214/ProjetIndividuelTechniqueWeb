#bash launcher.sh
#!/bin/bash
#Projet personnel -Xinyi Shen
#Install the dependencies and run the application

echo "******** Projet Personnel - Xinyi SHEN *********"
echo "--- Installation des dépendances ---"
pip3 install -r requirements.txt
echo "--- Run the application ---"
streamlit run app.py