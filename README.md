# pals-analysis

## Contexte
Palworld (ou Eidolon Parlu), qui a rapidement gagné en popularité dans le monde entier début janvier 2024, est un jeu de crafting et de survie multijoueur en monde ouvert, du développeur japonais Pocket Pair.  
Avec son gameplay innovant, ce jeu a attiré un grand nombre de joueurs et de fans, attirant l'attention sur les Pals, ces créatures fantastiques peuplant le monde virtuel du jeu.  
Vous apprivoisez et collectionnez ces mystérieuses créatures afin de construire, se battre, cultiver et travailler dans des usines afin de développer votre campement !  
N’étant pas insensible Nous-même à ce jeu, Nous avez consacré des heures interminables à ce jeu !  
Notre nature d’analyste de données aussi important que notre nature d’amateur de jeux vidéo, nous souhaitons réaliser une étude de Nos chers Pals.  
L'étude des caractéristiques et du comportement de ces créatures peut se montrer utile pour développer une expérience de jeu plus attrayante.

----------------

## Présentation du projet
Nous somme donc parti de données récoltées du jeux afin d'étudier ces données et déterminer quelles pals étaient les meilleurs.

----------------

### 1ère étape : importer les données
Après avoir récupérer les données sous forme de fichier csv, ils nous fallaient les importer sur nos ordinateur. Nous sommes donc parti sur une base de données MySQL car nous étions familliés avec cette outil.  
/// suspens attendre parti fini

----------------

### 2ème étape : analyse exploratoire
Une fois nos données enregistré sur notre base de données MySQL, Nous réalisons une analyse exploratoire de notre base de données afin d’identifier les informations contenues dans l'ensemble des données de Palworld, permettant une optimisation plus efficace de notre stratégie de jeu.  
Pour ce faire, nous utilisons sqlite3 afin d'effectuer des requettes divers nous permettant d'étoffer notre analyse tel que la distribution de la taille des Pals ou encore la répartition des zones d’apparition, ainsi que des bibliothèques python comme matplotlib afin d'ajouter du visuel sur nos observations.    
Notre analyse est disponible dans le notebook pals_notebook.ipynb.  

----------------

### 3ème étape : streamlit
Après avoir explorer nos données, il est temps de déterminer quels pals seront le plus utils au combat et sur le camp.  
Nous avons donc utilisé streamlit afin de dévelloper une api web interactif proposant plusieurs graphiques nous permettant de résoudre notre problématique.  
Ici les graphiques sont créées à l'aide de plotly car plus interactif que matplotlib.  
Les 2 premiers filtres sont utilisées pour le 1èr graphiques tandis que le 3ème pour le dernier.  

----------------

## Les meilleurs Pals
Grâce à nos merveilleux outils, nous pouvons donc établir une équipe parfaite selon ces critères : La répartition des types, prendre les pals dont le type est super efficace sur les types les plus présent du jeux. Et le total de statistique à savoir HP, melee ATK, remote ATK et defense.  
Cela nous donnerait donc cette équipe :  
* Jormuntide ignis, de types dragon et feu il contre les 2 types les plus présents dans le jeux ténèbres et bois. Il a un total de stat de 510 et peut être considéré comme le meilleur pals du jeux.
* Jormuntide, cousin de Jormuntide ignis de type dragon et eau cette fois, ici son type eau permet de contrer les types feu qui est le 3ème type le plus présent. Il a un total de stat de 500
