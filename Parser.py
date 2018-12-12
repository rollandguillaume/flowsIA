from lxml import etree
import hashlib
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import os
import Conf
import Vector

# fonction de creation d'id unique pour une donnée
# en utilisant des informations sur la donnée
# et surtout le timestamp de l'instant t
# pour s'assurer de l'unicité de l'id retourné
# @param value flows
# @return id sous forme de hash
def createId(value):
    key = value["startDateTime"] \
          + value["source"] + str(value["sourcePort"]) \
          + value["destination"] + str(value["destinationPort"]) \
          + value["stopDateTime"] \
          + str(datetime.now().timestamp())
    return hashlib.sha256(key.encode()).hexdigest()

# @source : https://python101.pythonlibrary.org/chapter31_lxml.html
# fonction de conversion d'un fichier xml
# contenant des informations sur des flows
# en dictionnaire
# en leur attribuant un index et un type
# pour un serveur elasticsearch
# @param xmlFile input file
# @return dictionnaire des flows du fichier
def parseXML(xmlFile):
    fobj = open(xmlFile, "rb")
    root = etree.fromstring(fobj.read())

    flow_dict = {}
    flows = []
    for flow in root.getchildren():
        for elem in flow.getchildren():
            if not elem.text:
                text = None
            else:
                try:
                    if(elem.tag in Conf.tagIntType):
                        text = int(elem.text)
                    else:
                        text = elem.text
                except:
                    text = elem.text

            flow_dict[elem.tag] = text

        flow_dict["_id"] = createId(flow_dict)
        flow_dict["_index"] = Conf.index
        flow_dict["_type"] = Conf.type
        flow_dict["fileName"] = xmlFile

        flows.append(flow_dict)

        flow_dict = {}
    return flows

# fonction de conversion d'un fichier xml
# contenant des informations sur des flows
# en dictionnaire
# en leur attribuant un index et un type
# pour un serveur elasticsearch
#
# les données du fichier d'entree sont normaliser sous forme d'un vecteur
# @param xmlFile input file
# @param indexTarget l'index souhaité pour le serveur elasticsearch
# @return dictionnaire des flows vectorisé du fichier d'entré
def parseXMLToVector(xmlFile, indexTarget):
    fobj = open(xmlFile, "rb")
    root = etree.fromstring(fobj.read())

    flow_dict = {}
    flows = []
    for flow in root.getchildren():
        for elem in flow.getchildren():
            if not elem.text:
                text = None
            else:
                try:
                    if(elem.tag in Conf.tagIntType):
                        text = int(elem.text)
                    else:
                        text = elem.text
                except:
                    text = elem.text


            flow_dict[elem.tag] = text

        flow_dict["_id"] = createId(flow_dict)
        flows.append(Vector.vectorisationOneFlow(flow_dict, indexTarget))

        flow_dict = {}
    return flows

# point d'entrée du parsing
# pour l'insertion des données bruts
# d'une liste de fichier xml
# dans un serveur elasticsearch
def initParser():
    es = Elasticsearch()
    sourceFolder = "resources/ISCX_train/"

    start = datetime.now()
    for file in os.listdir(sourceFolder):
        if file.endswith(".xml"):
            print("\nFILE " + file)
            for success, info in helpers.parallel_bulk(es, parseXML(sourceFolder+file), thread_count=4, request_timeout=100):
                if (not success):
                    print(info)

            print((datetime.now() - start))

    print("\n~~~~~~~~~~~~~~~~~~~~\nTOTAL TIME : ")
    end = datetime.now()
    print(end-start)

# point d'entrée du parsing
# pour l'insertion des données à vectoriser
# d'une liste de fichier xml contenue dans @sourceFolder
# dans un serveur elasticsearch à l'index @indexTarget
# @param sourceFolder le dossier source contenant les données a vectoriser
# @param indexTarget index de stockage des données sur elasticsearch
def initVectorisation(sourceFolder, indexTarget):
    es = Elasticsearch()

    start = datetime.now()
    for file in os.listdir(sourceFolder):
        if file.endswith(".xml"):
            print("\nFILE " + file)
            for success, info in helpers.parallel_bulk(es, parseXMLToVector(sourceFolder+file, indexTarget), thread_count=4, request_timeout=100):
                if (not success):
                    print(info)

            print((datetime.now() - start))

    print("\n~~~~~~~~~~~~~~~~~~~~\nTOTAL TIME : ")
    end = datetime.now()
    print(end - start)
