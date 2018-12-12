
from elasticsearch import Elasticsearch, helpers
import Conf

# @return la liste distinct des protocols existants
def get_the_list_of_all_the_distinct_protocols():
    return _getAllKeyToArray("protocolName")

# @param oneResName nom d'un type de donnée à trouvé en commun de données
# @return une liste des 1000 premiers resultat de l'aggregation de @oneResName
def _getAll(oneResName):
    body = {
        "_source": {
            "includes": [oneResName]
        },
        "aggs": {
            oneResName:{
                "terms":{
                    "field": oneResName+".keyword",
                    "size": 1000
                }
            }
        }
    }
    return _my_search(body)["aggregations"][oneResName]["buckets"]



# @param oneResName nom d'un type de donnée à trouvé en commun de données
# @return un generator contenant les resultats de l'aggregation de @oneResName
def _getAllNumber(oneResName):
    body = {
        "_source": {
            "includes": [oneResName]
        },
        "aggs": {
            oneResName:{
                "terms":{
                    "field": oneResName,
                    "size": 1000
                }
            }
        }
    }
    return _my_search(body)["aggregations"][oneResName]["buckets"]

def _getAllKeyToArray(oneResName):
    res = _getAll(oneResName)
    ret = []
    for item in res:
        ret.append(item['key'])
    return ret

# recherche (limité) elasticsearch
# @param body le corps de la recherche a effectuer
# @return liste limité de résultat de l'index elasticsearch @Conf.index
def _my_search(body):
    es = Elasticsearch()
    return es.search(index=Conf.index, body=body)


# scan elasticsearch
# @param body le corps de la recherche a effectuer
# @return un generator de résultat de l'index elasticsearch @Conf.index
def _my_scan(body):
    es = Elasticsearch()
    return helpers.scan(es, index=Conf.index, query=body)


# @param protocolName le nom du protocol a rechercher
# @return tous les flows dont le protocol est @protocolName
def get_the_list_of_flows_for_a_given_protocol(protocolName):
    return _getAllFlows("protocolName", protocolName)

# @param oneResName nom d'un type de donnée à trouvé
# @param value valeur du champs @oneResName a trouver
# @return un generator des données ayant le champs @oneResName egale a @value
def _getAllFlows(oneResName, value):
    body = {
        "_source": {
            "includes": [oneResName]
        },
        "query": {
            "bool": {
                "must": {
                    "match": {oneResName : value}
                }
            }
        }
    }
    return _my_scan(body)

# @return le nombre de flow pour chaque protocol
def get_the_number_of_flows_for_each_protocols():
    return _getAll("protocolName")

# @return la taille de payload source pour chaque protocol
def get_the_source_payload_size_for_each_protocol():
    return _getPayLoad("protocolName", "sourcePayloadAsBase64")

# @return la taille de payload destination pour chaque protocol
def get_the_destination_payload_size_for_each_protocol():
    return _getPayLoad("protocolName", "destinationPayloadAsBase64")

# @return des statistiques sur la taille du paquet de destination (en byte) pour chaque protocol
def get_the_destination_bytes_size_for_each_protocol():
    return _getAverageOnAggregationOf("protocolName", "totalDestinationBytes")

# @return des statistiques sur la taille du paquet de source (en byte) pour chaque protocol
def get_the_source_bytes_size_for_each_protocol():
    return _getAverageOnAggregationOf("protocolName", "totalSourceBytes")

# @return des statistiques sur la taille du paquet de destination pour chaque protocol
def get_the_destination_packets_size_for_each_protocol():
    return _getAverageOnAggregationOf("protocolName", "totalDestinationPackets")

# @return des statistiques sur la taille du paquet de source pour chaque protocol
def get_the_source_packets_size_for_each_protocol():
    return _getAverageOnAggregationOf("protocolName", "totalSourcePackets")

# @param oneResName valeur du premier type de donnée a trouver
# @param avg valeur du second type de données sur lequel effectuer les statistiques
# @return des statistiques sur @oneResName moyenné sur @avg
def _getAverageOnAggregationOf(oneResName, avg):
    body = {
        "size": 0,
        "aggs": {
            oneResName: {
                "terms": {
                    "field": oneResName + ".keyword",
                    "size": 1000
                },
                "aggs" : {
                    "avg_"+avg: {
                        "extended_stats": {
                            "field": avg
                        }
                    }
                }
            }
        }
    }
    return _my_search(body)["aggregations"][oneResName]["buckets"]


# @return la liste distincts des nom d'application des flows
def get_the_list_of_all_the_distinct_applications():
    return _getAllKeyToArray("appName")

# @param application le nom de l'application voulue
# @return la liste des flows dont le nom d'application est @application
def get_the_list_of_flows_for_a_given_application(application):
    return _getAllFlows("appName", application)

# @return le nombre de flows par nom d'application
def get_the_number_of_flows_for_each_application():
    return _getAll("appName")

# @return la taille de payload source pour chaque nom d'application
def get_the_source_payload_size_for_each_application():
    return _getPayLoad("appName", "sourcePayloadAsBase64")

# @return la taille de payload destination pour chaque nom d'application
def get_the_destination_payload_size_for_each_application():
    return _getPayLoad("appName", "destinationPayloadAsBase64")

# @return des statistiques sur la taille du paquet de destination (en byte) pour chaque nom d'application
def get_the_destination_bytes_size_for_each_application():
    return _getAverageOnAggregationOf("appName", "totalDestinationBytes")

# @return des statistiques sur la taille du paquet de source (en byte) pour chaque nom d'application
def get_the_source_bytes_size_for_each_application():
    return _getAverageOnAggregationOf("appName", "totalSourceBytes")

# @return des statistiques sur la taille du paquet de destination pour chaque nom d'application
def get_the_destination_packets_size_for_each_application():
    return _getAverageOnAggregationOf("appName", "totalDestinationPackets")

# @return des statistiques sur la taille du paquet de source pour chaque nom d'application
def get_the_source_packets_size_for_each_application():
    return _getAverageOnAggregationOf("appName", "totalSourcePackets")

# @param oneResName valeur du premier type de donnée a trouver
# @param avg valeur du second type de données sur lequel effectuer les statistiques (payload ici)
# @return des statistiques sur @oneResName moyenné sur @avg
def _getPayLoad(oneResName, avg):
    body = {
        "_source": {
            "includes": [oneResName]
        },
        "aggs": {
            oneResName: {
                "terms": {
                    "field": oneResName + ".keyword",
                    "size": 1000
                },
                "aggs": {
                    "avg_"+avg: {
                        "avg": {
                            "script": {
                                "source": "4 * doc['"+avg+"'].length / 3"
                            }
                        }
                    }
                }
            }
        }
    }
    return _my_search(body)["aggregations"][oneResName]["buckets"]


# @return une aggregation sur le nombre de flows ayant un certain nombre de packet
def get_the_number_of_flows_for_each_packet_number():
    return _getAllNumber("totalDestinationPackets")

# @param appName le nom de l'application a rechercher
# @return un generator de tous les flows ayant pour nom d'application @appName
def getAllByAppName(appName):
    body = {
        "query": {
            "match" : {
                "appName" : appName
            }
        }
    }
    es = Elasticsearch()
    return helpers.scan(es, index=Conf.indexVector, query=body)

# @param index l'index elasticsearch souhaité
# @return un generator de toutes les données contenues dans l'index @index d'elasticsearch
def getAllByIndex(index):
    body = {
        "query": {
            "match_all": {}
        }
    }
    es = Elasticsearch()
    return helpers.scan(es, index=index, query=body)
