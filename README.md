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
  - permet de démarrer un [serveur ElasticSearch]((http://localhost:9200) et d’une [interface Kibana](http://localhost:5601)

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

[Vérifier les configurations](#conf.py) et modifier au besoin.


Dans un second terminal, lancer le script Main.py.
````
python3 Main.py
````

## Cas d'utilisation

//TODO


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
