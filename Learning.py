from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
import Conf
from datetime import datetime
import random


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


def checkDatas(dataTrain, resultTrain, dataTest, resultTest):
    print()
    print("~~~~~~~~~~~~~~CHECK~~~~~~~~~~~~~~")
    print("dataTrain:", len(dataTrain), " ; resultTrain:", len(resultTrain), "=>", len(dataTrain) == len(resultTrain))
    print("dataTest:", len(dataTest), " ; resultTest:", len(resultTest), "=>", len(dataTest) == len(resultTest))
    print("Total data length", (len(dataTrain) + len(dataTest)))
    print()

# fonction d'evaluation du projet
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


def knnBasic(dataTrain, resultTrain, dataTest):
    print("KNN Learning...")
    start = datetime.now()
    knn_classifier = OneVsRestClassifier(KNeighborsClassifier(n_neighbors=3))
    knn_classifier.fit(dataTrain, resultTrain)
    score_knn = knn_classifier.predict_proba(dataTest)
    print("End KNN Learning in:", datetime.now()-start)

    return knn_classifier, score_knn


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


