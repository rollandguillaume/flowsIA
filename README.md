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
  - dossier devant contenir les fichiers “.xml” des données correspondantes aux différents paquets contenus dans des flows et dont on connaît leur dangerosité. Lien pour les données : https://www.unb.ca/cic/datasets/index.html
- resources/evaluation/test/
  - dossier devant contenir le(s) fichier(s) “.xml” au même format que le dossier précédent. Correspondant aux données et dont on souhaite prédire leur dangerosité.

### Docker
- docker/
  - permet de démarrer un serveur ElasticSearch et d’une interface Kibana accessible sur le port 5601

````
cd docker
docker-compose up

````


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
