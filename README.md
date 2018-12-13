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

//TODO

### Description de notre vectorisation :

On as une liste de donnée soit normalisée ou soit binaire. Les valeurs sont donc entre 0 et 1 quoi qu’il arrive. La plupart des données sont présente pour les parties source et destination. 

Les valeurs binaire:
- Tous les flags HTTP : "S","R","P","A","F","Illegal7","Illegal8" qui sont présent (x=1) ou non (x=0) dans les flows.
- La direction : "L2R", "L2L", "R2L", "R2R". Si la direction est “L2R” par exemple, cette valeur sera à un et les 3 autres à 0.
- Adresse IP triées selon leur classe. Pour AAA.BBB.CCC.DDD , on a :
  - Classe A (x=0.2) si 0 < AAA <= 126
  - Classe B (x=0.4) si 126 < AAA <= 191
  - Classe C (x=0.6) si 191 < AAA <= 223
  - Classe D (x=0.8) si 223 < AAA <= 239
  - Classe E (x=1) si 239 < AAA <= 250
- La payload à partir de laquelle on forme un histogramme qui présente le nombre de bytes ayant une taille compris entre des intervals de valeurs définis (0..31 / 32..63 / … / 224..255). 

Les valeurs normalisée :
- Le port : On normalise la valeur du port en le divisant par la valeur de port maximale, x = port / 65535 


Autres valeurs :
- Timestamps : Différence entre date de fin et date de début.
- Rapport entre le nombre de paquet de la source et celui de la destination
- Rapport entre le nombre de flow de la source et celui de la destination
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
