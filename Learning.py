from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
import Conf
from datetime import datetime
import random

# fonction d'initialisation d'evaluation d'un classifieur :
# - prise des données d'entrées @generator
# - melange des données
# - 2/3 des données definies comme données d'entrainement
# - 1/3 des données definies comme données de test
# @param generator les données totales d'entrée
# @return 4 listes :
# - liste des données selectionné d'entrainement
# - liste des resultats de la liste d'entrainement
# - liste des données selectionné pour les tests
# - liste des resultats attendu lors de la prediction sur la liste des tests
def initLearn(generator):
    print("Starting...")
    datas = list(generator)
    print("Datas Training:", len(datas))

    nbData = len(datas)
    start = datetime.now()
    random.shuffle(datas)
    print("Shuffle Datas", len(datas), "in", datetime.now() - start)

    print("Load Datas:")
    start = datetime.now()
    dataTrain = []
    resultTrain = []
    dataTest = []
    resultTest = []
    i = 0
    for flow in datas:
        source = flow["_source"]
        response = source["Tag"]
        vector = source["vector"]

        if i < int(nbData*.67):
            dataTrain.append(vector)
            resultTrain.append(response)
        else:
            dataTest.append(vector)
            resultTest.append(response)

        i = i + 1

    return dataTrain, resultTrain, dataTest, resultTest

# fonction de verification entre les quantites de données d'entrainement ou de test
# et leur liste associe de resultat attendu
def checkDatas(dataTrain, resultTrain, dataTest, resultTest):
    print()
    print("~~~~~~~~~~~~~~CHECK~~~~~~~~~~~~~~")
    print("dataTrain:", len(dataTrain), " ; resultTrain:", len(resultTrain), "=>", len(dataTrain) == len(resultTrain))
    print("dataTest:", len(dataTest), " ; resultTest:", len(resultTest), "=>", len(dataTest) == len(resultTest))
    print("Total data length", (len(dataTrain) + len(dataTest)))
    print()

# point d'entree de la fonction d'evaluation du projet
# @param generatorTrain la liste des données d'entrainement du predicteur
# @param generatorTest la liste des données a evaluer par le predicteur
def testLearning(generatorTrain, generatorTest):
    print("Starting...")
    start = datetime.now()
    datas = list(generatorTrain)
    datasTest = list(generatorTest)
    print("Datas Training:", len(datas))
    print("Datas Test:", len(datasTest))

    print("Load Datas:")
    dataTrain = []
    resultTrain = []
    dataTest = []
    i = 0
    for flow in datas:
        source = flow["_source"]
        dataTrain.append(source["vector"])
        resultTrain.append(source["Tag"])
        i = i + 1
    print("Feed Training duration:", datetime.now() - start)

    i = 0
    for flow in datasTest:
        source = flow["_source"]
        dataTest.append(source["vector"])
        i = i + 1
    print("Feed Test duration:", datetime.now()-start)

    return dataTrain, resultTrain, dataTest

# fonction de lancement du classifieur
# @param dataTrain les données d'entrainement
# @param resultTrain les resultats attendus
# @param les données sur lesquelles la prediction est demandé
def knnBasic(dataTrain, resultTrain, dataTest):
    print("KNN Learning...")
    start = datetime.now()
    knn_classifier = OneVsRestClassifier(KNeighborsClassifier(n_neighbors=Conf.neighbors))
    knn_classifier.fit(dataTrain, resultTrain)
    score_knn = knn_classifier.predict_proba(dataTest)
    print("End KNN Learning in:", datetime.now()-start)

    return knn_classifier, score_knn

# fonction d'ecriture des resultats d'un classifieur
# dans un fichier de sortie (Conf.py)
# @param score_knn les resultats de prediction du classifieur et leur probabilité associé
def writeResultFile(score_knn):
    start = datetime.now()
    file = open(Conf.fileNameResult, "w")

    nbAlert = 0
    for i in range(len(score_knn)):
        if score_knn[i][0] > score_knn[i][1]:
            file.write(str(score_knn[i][0]) + " 0")
        else:
            nbAlert += 1
            file.write(str(score_knn[i][1]) + " 1")

        file.write("\n")

    file.close()
    print("Write of", Conf.fileNameResult, "in", datetime.now()-start)
    return nbAlert
