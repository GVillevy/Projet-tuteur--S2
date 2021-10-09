import requests
from bs4 import BeautifulSoup 
import time
from datetime import datetime
import mariadb
import sys

#On ajoute l'url de notre site web à notre URL
url='https://www.boursorama.com/cours/NVDA/'
    

try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        port=3306,
        database="bourse"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
cur = conn.cursor() 


#Déclaration de notre booléen afin de faire une boucle infinie
b = True
type(b)


#Tant que b est true (boucle infinie)
while b:

    #On fait une requête à notre URL
    response=requests.get(url)

    #Si le reponse de la requête est ok, on éxécute notre programme
    if response.ok:


        #On précise à notre plugin de webscrapping (Bs4) qu'on utiliser l'html parser
        soup = BeautifulSoup(response.text,'html.parser')



        #SCRAPPING DE LA VALEUR BOURSIERE
        #On cherche les div avec la class "c-ticker__item c-ticker__item--value". On prend le premier élément et on prend que le texte
        valeur_boursiere=soup.findAll('div', attrs={"class":u"c-ticker__item c-ticker__item--value"})[0].text
        #On supprime les espaces au début du string
        valeur_boursiere=valeur_boursiere.strip()
        #On supprime le "USD" du String
        valeur_boursiere=valeur_boursiere.replace(' USD','')




        #SCRAPPING DU POURCENTAGE
        #On cherche les div avec la class "c-ticker__item c-ticker__item c-ticker__item--variation-percent u-color-stream-up". On prend le premier élément et on prend que le texte
        pourcentage=soup.findAll('span', attrs={"class":u"c-instrument c-instrument--variation"})[0].text
        #On supprime les espaces au début du string
        pourcentage=pourcentage.strip()






        #SCRAPPING DE LA VALEUR INDICATIVE
        #On cherche les span avec la class "c-faceplate__indicative-value". On prend le premier élément et on prend que le texte
        valeur_indicative=soup.findAll('span', attrs={"class":u"c-faceplate__indicative-value"})[0].text
        #On supprime les espaces du string
        valeur_indicative=valeur_indicative.replace(' ','')
        #On supprime les retours à la ligne
        valeur_indicative=valeur_indicative.replace('\n',' ')




        #SCRAPPING DE L'OUVERTURE
        #On cherche les span avec la class "c-instrument c-instrument--open". On prend le premier élément et on prend que le texte
        ouverture=soup.findAll('span', attrs={"class":u"c-instrument c-instrument--open"})[0].text




        #SCRAPPING DE LA CLOTURE VEILLE
        #On cherche les span avec la class "c-instrument c-instrument--previousclose". On prend le premier élément et on prend que le texte
        cloture_veille=soup.findAll('span', attrs={"class":u"c-instrument c-instrument--previousclose"})[0].text




        #SCRAPPING DU VOLUME
        #On cherche les span avec la class "c-instrument c-instrument--totalvolume". On prend le premier élément et on prend que le texte
        volume=soup.findAll('span', attrs={"class":u"c-instrument c-instrument--totalvolume"})[0].text
        
        #PRISE DE LA DATE
        date_now = datetime.now()
        date=date_now.strftime("%d/%m/%y, %H:%M:%S")
        
        print(str(datetime.now()) + " : \n prix de la bourse : " + valeur_boursiere + "\n pourcentage : " + pourcentage + "\n valeur Indicative : "
               + valeur_indicative + "\n valeur d'ouverture : " +ouverture + "\n valeur de cloture de la veille : " + cloture_veille + "\n volume : " + volume+ "\n date : " + date)

        try: 
            cur.execute(
            "INSERT INTO nvidia (valeur_boursiere,pourcentage,valeur_indicative,ouverture,cloture_veille,volume,date) VALUES (?, ?, ?, ?, ?, ?,?)", 
            (valeur_boursiere,pourcentage,valeur_indicative,ouverture,cloture_veille,volume,date))
        except mariadb.Error as e: 
            print(f"Error: {e}")

        conn.commit()
        
    #On stop le programme 10 minutes ( mettre 1 pour voir + rapidement les résultats)
    time.sleep(600)