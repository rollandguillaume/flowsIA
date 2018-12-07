
from elasticsearch import Elasticsearch, helpers
import Conf

# f1
def get_the_list_of_all_the_distinct_protocols():
    return _getAllKeyToArray("protocolName")


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

def _my_search(body):
    es = Elasticsearch()
    return es.search(index=Conf.index, body=body)

def _my_scan(body):
    es = Elasticsearch()
    return helpers.scan(es, index=Conf.index, query=body)


# f2
def get_the_list_of_flows_for_a_given_protocol(protocolName):
    return _getAllFlows("protocolName", protocolName)

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

# f3
def get_the_number_of_flows_for_each_protocols():
    return _getAll("protocolName")

# f4
def get_the_source_payload_size_for_each_protocol():
    return _getPayLoad("protocolName", "sourcePayloadAsBase64")

def get_the_destination_payload_size_for_each_protocol():
    return _getPayLoad("protocolName", "destinationPayloadAsBase64")

# f5
def get_the_destination_bytes_size_for_each_protocol():
    return _getAverageOnAggregationOf("protocolName", "totalDestinationBytes")

def get_the_source_bytes_size_for_each_protocol():
    return _getAverageOnAggregationOf("protocolName", "totalSourceBytes")

# f6
def get_the_destination_packets_size_for_each_protocol():
    return _getAverageOnAggregationOf("protocolName", "totalDestinationPackets")

def get_the_source_packets_size_for_each_protocol():
    return _getAverageOnAggregationOf("protocolName", "totalSourcePackets")


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


# f7
def get_the_list_of_all_the_distinct_applications():
    return _getAllKeyToArray("appName")

# f8
def get_the_list_of_flows_for_a_given_application(application):
    return _getAllFlows("appName", application)

# f9
def get_the_number_of_flows_for_each_application():
    return _getAll("appName")


# f10
def get_the_source_payload_size_for_each_application():
    return _getPayLoad("appName", "sourcePayloadAsBase64")

def get_the_destination_payload_size_for_each_application():
    return _getPayLoad("appName", "destinationPayloadAsBase64")

# f11
def get_the_destination_bytes_size_for_each_application():
    return _getAverageOnAggregationOf("appName", "totalDestinationBytes")

def get_the_source_bytes_size_for_each_application():
    return _getAverageOnAggregationOf("appName", "totalSourceBytes")

# f12
def get_the_destination_packets_size_for_each_application():
    return _getAverageOnAggregationOf("appName", "totalDestinationPackets")

def get_the_source_packets_size_for_each_application():
    return _getAverageOnAggregationOf("appName", "totalSourcePackets")


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


# aggregation sur le nombre de flows ayant un certain nombre de packet
def get_the_number_of_flows_for_each_packet_number():
    return _getAllNumber("totalDestinationPackets")


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


def getAllByIndex(index):
    body = {
        "query": {
            "match_all": {}
        }
    }
    es = Elasticsearch()
    return helpers.scan(es, index=index, query=body)