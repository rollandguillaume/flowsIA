
# launch the vectorisation of training and evaluation datas
goParsing = True
# laucnh the learning of :
# - interApplication with 2/3 training and 1/3 test to evaluate the accuracy of learning
# - intraApplication with 100% training to predict the evaluation datas
goLearning = True
# output name of the prediction result
fileNameResult = "resources/FRERET_ROLLAND.txt"


# -----------DEV-ONLY----------------
# nombre de voisin devant etre considerer lors des predictions
neighbors = 3

# PARSER
# index et type utilisé pour l'insertion des données bruts
index = "flows"
type = "flows"

# les types de données devant être considérer comme des entiers pour elasticsearch
tagIntType = ["destinationPort", "sourcePort", "totalDestinationBytes", "totalDestinationPackets", "totalSourceBytes", "totalSourcePackets"]

# taille du bulk d'elastic search pour l'insertion des données
bulkSize = 50000

# VECTOR
# index pour la vectorisation des données d'entrainement
indexVector = "vector"
# index pour la vectorisation des données d'evaluation
indexVectorTest = "evaluationtest"
# type pour la vectorisation des données d'entrainement et d'evaluation
indexVectorType = "vector1"

# liste des flags existants dans les données brutes : sert lors de la normalisation des flags des packets
flags = ["S","R","P","A","F","Illegal7","Illegal8"]
# liste des directions existantes dans les données brutes : sert lors de la normalisation des directions des packets
directions = ["L2R", "L2L", "R2L", "R2R"]
# identifiant d'une donnée normal (= sans alerte)
normalTag = "Normal"
# constante du nombre maximum atteignable d'un port
maxPort = 65535
