from lxml import etree
import hashlib
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import os
import Conf
import Vector

def createId(value):
    key = value["startDateTime"] \
          + value["source"] + str(value["sourcePort"]) \
          + value["destination"] + str(value["destinationPort"]) \
          + value["stopDateTime"] \
          + str(datetime.now().timestamp())
    return hashlib.sha256(key.encode()).hexdigest()

# https://python101.pythonlibrary.org/chapter31_lxml.html
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