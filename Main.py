import Search
import Draw
import Vector
import Parser
import Learning
from datetime import datetime
import Conf

def timeStamp(start):
    return datetime.now()-start

# use datas to draw the ROC curve
def learnWithRoc(datas):
    dataTrain, resultTrain, dataTest, resultTest = Learning.initLearn(datas)
    Learning.checkDatas(dataTrain, resultTrain, dataTest, resultTest)
    knn_clasifier, score_knn = Learning.knnBasic(dataTrain, resultTrain, dataTest)
    Draw.drawRoc(dataTest, resultTest, knn_clasifier, score_knn)

# use the datas test to evaluate our own learning
def evaluation(datas, genTest):
    dataTrain, resultTrain, dataTest = Learning.testLearning(datas, genTest)
    knn_clasifier, score_knn = Learning.knnBasic(dataTrain, resultTrain, dataTest)
    nbAlert = Learning.writeResultFile(score_knn)
    print("Total Alert:", nbAlert)


start = datetime.now()

# --------------PARSER-----------------
if Conf.goParsing:
    print("goParsing")
    print("~~~~~Parsing of ISCX_train~~~~~")
    Parser.initVectorisation("resources/ISCX_train/", Conf.indexVector)
    print("Vectorisation Training:", timeStamp(start))
    print("~~~~~Parsing of evaluation~~~~~")
    Parser.initVectorisation("resources/evaluation/test/", Conf.indexVectorTest)
    print("Vectorisation Test:", timeStamp(start))

# --------------LEARNING-----------------
if Conf.goLearning:
    print("goLearning")
    print("~~~~~Learning and Draw ROC curve~~~~~")
    learnWithRoc(Search.getAllByAppName("HTTPWeb"))
    print("~~~~~Learning and Prediction~~~~~")
    evaluation(Search.getAllByAppName("HTTPWeb"), Search.getAllByIndex("evaluationtest"))


print("~~~~~~~~~~~~~~~MAIN TOTAL TIME~~~~~~~~~~~~~~~\n", timeStamp(start))
