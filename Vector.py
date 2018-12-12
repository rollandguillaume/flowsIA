from datetime import datetime
import Conf
import traceback

# @param value la valeur du port a normaliser
# @return normalisation par rapport entre le port @value et la valeur théorique max du port
def _portType(value):
    return value / Conf.maxPort

# @param ip adresse ip a normaliser
# @return une valeur entre 0 et 1 en suivant la classe de l'adresse ip @ip
def _ipClass(ip):
    value = int(ip.split(".")[0])
    if (value >= 1 and value <= 126):
        return 0.2
    elif (value >= 128 and value <= 191):
        return 0.4
    elif (value >= 192 and value <= 223):
        return 0.6
    elif (value >= 224 and value <= 239):
        return 0.8
    elif (value >= 240 and value <= 255):
        return 1
    else:
        return 0

# @param start date de debut
# @param stop date de fin
# @return timestamp entre le debut et la fin de l'envoi du flow
def _elapsedTime(start, stop):
    format = "%Y-%m-%dT%H:%M:%S"
    dstart = datetime.strptime(start, format).timestamp()
    dstop = datetime.strptime(stop, format).timestamp()
    return (dstop - dstart)

# @param payload
# @return un tableau (histogramme) : rapport entre une taille de payload et la somme totale de la payload
def _payloadConverter(payload):
    tabVal = [0] * 8

    if (payload != None):
        ba = bytearray(payload, "utf-8")
        for val in ba:
            _payloadAiguillage(tabVal, val)

    sum = 0
    for c in tabVal:
        sum = sum + c

    if sum != 0:
        for i in range(len(tabVal)):
            tabVal[i] = tabVal[i] / sum

    return tabVal

# @param tabVal le tableau histogramme a normaliser
# @param value le prochain byte a ranger dans @tabVal
def _payloadAiguillage(tabVal, value):
    if (value >= 0 and value <= 31):
        tabVal[0] += 1
    elif (value > 32 and value <= 63):
        tabVal[1] += 1
    elif (value > 64 and value <= 95):
        tabVal[2] += 1
    elif (value > 96 and value <= 127):
        tabVal[3] += 1
    elif (value > 128 and value <= 159):
        tabVal[4] += 1
    elif (value > 160 and value <= 191):
        tabVal[5] += 1
    elif (value > 192 and value <= 223):
        tabVal[6] += 1
    elif (value > 224 and value < 256):
        tabVal[7] += 1

# fonction de normalisation d'un String @values
# dont les données sont entre le separateur @separator
# et dont la liste des données potentielles est @comparatifTable
# exemple de la liste des flags d'un flow :
# @value : "S,R,P"
# @separator : ","
# @comparatifTable : ["S","R","P","A","F","Illegal7","Illegal8"]
# @return : [1,1,1,0,0,0,0]
def _binarisation(values, separator, comparatifTable):
    result = [0] * len(comparatifTable)

    if (values):
        tabValues = values.split(separator)

        for val in tabValues:
            if (val in comparatifTable):
                index = comparatifTable.index(val)
                result[index] = 1

    return result

# @return le rapport entre deux valeurs @val1 et @val2
def rapport(val1, val2):
    calcul = float(val1)
    if (val2 != 0):
        calcul = float(val1 / val2)
    return calcul

# conversion tag "normal" en "0" et "Alerte" en "1"
# @param flow le flows a trasformer
# @return 0 si le flow est "normal", 1 sinon
def tag(flow):
    if (flow["Tag"] == Conf.normalTag):
        return 0
    return 1

# fonction de vectorisation d'un flow
# @param flow le flow a vectoriser
# @param indexTarget l'index de destination pour elasticsearch
# @return le flows vectorisé
def vectorisationOneFlow(flow, indexTarget):
    vector = {}

    try:
        vector["_id"] = flow["_id"]
        vector["_index"] = indexTarget
        vector["_type"] = Conf.indexVectorType

        vector["appName"] = flow["appName"]
        vector["protocolName"] = flow["protocolName"]
        vector["Tag"] = tag(flow)

        theVector = []

        theVector.append(_elapsedTime(flow["startDateTime"], flow["stopDateTime"]))

        # port
        theVector.append(_portType(flow["destinationPort"]))
        theVector.append(_portType(flow["sourcePort"]))

        # @IP
        theVector.append(_ipClass(flow["destination"]))
        theVector.append(_ipClass(flow["source"]))

        # flags
        theVector = theVector + _binarisation(flow["destinationTCPFlagsDescription"], ",", Conf.flags)
        theVector = theVector + _binarisation(flow["sourceTCPFlagsDescription"], ",", Conf.flags)

        # direction
        theVector = theVector + _binarisation(flow["direction"], ",", Conf.directions)

        # rapport
        theVector.append(rapport(flow["totalSourcePackets"], flow["totalDestinationPackets"]))
        theVector.append(rapport(flow["totalSourceBytes"], flow["totalDestinationBytes"]))


        # payload
        try:
            theVector = theVector + _payloadConverter(flow["sourcePayloadAsUTF"])
        except Exception as e:
            tabVal = [0] * 8
            theVector = theVector + tabVal

        try:
            theVector = theVector + _payloadConverter(flow["destinationPayloadAsUTF"])
        except Exception as e:
            tabVal = [0] * 8
            theVector = theVector + tabVal

        vector["vector"] = theVector

    except Exception as e:
        print("---------ERROR---------")
        print(flow)
        traceback.print_exc()

    return vector
