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
    print("Vectorisation Training:", timeStamp(start))
    Parser.initVectorisation("resources/ISCX_train/", Conf.indexVector)
    print("Vectorisation Test:", timeStamp(start))
    Parser.initVectorisation("resources/evaluation/test/", Conf.indexVectorTest)


# --------------LEARNING-----------------
if Conf.goLearning:
    print("goLearning")
    learnWithRoc(Search.getAllByAppName("HTTPWeb"))
    evaluation(Search.getAllByAppName("HTTPWeb"), Search.getAllByIndex("evaluationtest"))


print("~~~~~~~~~~~~~~~MAIN TOTAL TIME~~~~~~~~~~~~~~~\n", timeStamp(start))



