# FlowsIA
## But du projet

On cherche à prédire le fait qu’un flow soit une alerte ou non, Pour cela on dispose d’un ensemble de données de flows.

## Etapes de réalisation

- [x] Parser les fichiers d’entrées
- [x] Stocker les données dans une DB
- [x] Normaliser les données
- [x] Vectoriser les données
- [x] Lancer l’apprentissage
- [x] Prédire
- [x] Évaluer la précision
- [x] Tracer la courbe ROC
- [x] Rendre compte des résultats dans un fichier de sortie


## Architecture

### Dossier de données
- resources/ISCX_train/
  - dossier devant contenir les fichiers “.xml” des données correspondantes aux différents paquets contenus dans des flows et dont on connaît leur dangerosité. [Site vers les données.](https://www.unb.ca/cic/datasets/index.html)
- resources/evaluation/test/
  - dossier devant contenir le(s) fichier(s) “.xml” au même format que le dossier précédent. Correspondant aux données et dont on souhaite prédire leur dangerosité.

### Docker
- docker/
  - permet de démarrer un [serveur ElasticSearch](http://localhost:9200) et d’une [interface Kibana](http://localhost:5601)

### Conf.py

Fichier de configuration modifiable
````
goParsing = True //au moins une fois à vrai pour la première fois
goLearning = True
fileNameResult = "resources/output.txt"
# -----------DEV-ONLY----------------
neighbors = 3
````
- goParsing permet de vectoriser les données
- goLearning permet de lancer l'apprentissage et les prédictions

- Un nombre impaire de voisin est plus intéressant pour éviter d’avoir un choix random en cas d’égalité entre le nombre de voisin “Normal” et “Alerte” trouvé.

## Procedure d'utilisation

Dans un premier terminal, démarrer ElasticSearch.
````
cd docker
docker-compose up
````

[Vérifier les configurations](#confpy) et modifier au besoin.


Dans un second terminal, lancer le script Main.py.
````
python3 Main.py
````

## Cas d'utilisation

Suivre [la procédure d'utilisation](#procedure-dutilisation) au préalable.

1. Vectorisation des **547347** données d'apprentissage

  ![image de l'avancement de la vectorisation des données d'apprentissage](/resources/images/0_trainingParsing.png)

  Lecture de tous les fichiers de resources/ISCX_train/ avec indication du temps passé depuis le lancement du programme.

2. Vectorisation des **19884** données à prédire

  ![image de l'avancement de la vectorisation des données d'apprentissage](/resources/images/1_evalParsing.png)

  Lecture de tous les fichiers de resources/evaluation/test/ avec indication du temps passé depuis le lancement du programme.

3. Evaluation de la précision du classifieur **KNN**

  Parmi toutes les données d'apprentissage (celles dont on connait à l'avance le résultat "Alerte" ou non donc) ; on choisi 2/3 d'entre elles pour permettre au classifieur d'apprendre de ces données afin de prédire les résultats sur le tiers restant.

4. Tracer de la courbe **ROC**

  La courbe ROC permet d'évaluer la précision du classifieur, plus l'aire sous la courbe (**AUC**) est proche de **1** et plus le classifieur est intéressant.

  ````
  AUC = 0.995
  ````

  Les valeurs d'AUC peuvent varier (résultats déjà obtenus entre 0.952 et 0.999) dû au fait que les données sont choisies aléatoirement.

  ![image de la courbe ROC](/resources/images/3_ROCcurveWithAUC.png)

  **NB** : Avoir une bonne précision de signifie pas que notre classifieur detecte tout. En effet, parmi les données mis à disposition, il y a très peu d'alertes donc si le classifieur trouve bien les flows normals, il peut n'en être rien des alertes.

5. Lancement de la prédiction sur les données à évaluer

  Dans ce contexte, toutes les données d'apprentissage sont utilisées pour faire apprendre le classifieur afin de prédire les résultats sur les données à évaluer.

  ````
  nobre d'alerte = 12
  ````
  Le nombre d'alerte remonté varie parfois bien que les données d'apprentissage soit identiques d'une expérience à l'autre, résultats déjà obtenus entre 11 et 14 alertes.

  ![image de la courbe ROC](/resources/images/4_learningPrediction.png)

6.  Formatage des résultats de prédiction

  Pour chacune des données à évaluer, le classifieur fourni un **indice de confiance** compris entre 0 et 1 et le **résultat de prédiction**, 0 pour un flow "Normal" et 1  pour un flow "Alerte".

  On est en mesure de compter le nombre potentiel d'alerte, ici **12** alertes ; Puis d'écrire l'entierté des résultats dans un fichier présenté de la manière suivante : (indice de confiance *espace* prédiction)

  ````
  ...
  1.0 0
  1.0 0
  1.0 0
  0.666666666667 1
  1.0 0
  1.0 0
  1.0 0
  ...
  ````

7. Temps d'éxécution *juste pour information*

  ![image du temps d'éxécution](/resources/images/5_mainTotalTime.png)


## Description de notre vectorisation

On a une liste de données soit normalisée soit binaire. Les valeurs sont donc entre 0 et 1 quoi qu’il arrive. La plupart des données sont présentes pour les parties source et destination.

Les valeurs binaire :
- Tous les flags HTTP : "S", "R", "P", "A", "F", "Illegal7", "Illegal8" qui sont présent (x=1) ou non (x=0) dans les flows.
- La direction : "L2R", "L2L", "R2L", "R2R". Si la direction est “L2R” par exemple, cette valeur sera à 1 et les trois autres à 0.
- Adresse IP triées selon leur classe. Pour AAA.BBB.CCC.DDD , on a :
  - Classe A (x=0.2) si 0 < AAA <= 126
  - Classe B (x=0.4) si 126 < AAA <= 191
  - Classe C (x=0.6) si 191 < AAA <= 223
  - Classe D (x=0.8) si 223 < AAA <= 239
  - Classe E (x=1) si 239 < AAA <= 250
- La payload à partir de laquelle on forme un histogramme qui présente le nombre de bytes ayant une taille comprise entre des intervals de valeurs définis (0..31 / 32..63 / … / 224..255).

Les valeurs normalisées :
- Le port : On normalise la valeur du port en le divisant par la valeur de port maximale, x = port / 65535


Autres valeurs :
- Timestamps : Différence entre date de fin et date de début d'émission.
- Rapport entre le nombre de paquets de la source et celui de la destination
- Rapport entre le nombre de flows de la source et celui de la destination
- 0 ou 1 si le flow est une attaque (valeur séparée du vecteur)



## Dev only
### datafield configuration
````
PUT flows/packet/_doc
{
  "properties": {
    "protocolName.keyword": {
      "type":     "text",
      "fielddata": true
    }
  }
}
````

### delete all data of an index
````
curl -X DELETE "localhost:9200/my_index"
````
