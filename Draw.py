import Search
import matplotlib.pyplot as plt
from sklearn import metrics

def draw_log_nb_flow_by_log_nb_packet():
    res = Search.get_the_number_of_flows_for_each_packet_number()

    x = []
    y = []
    for item in res:
        x.append(item["key"])
        y.append(item["doc_count"])

    # plt.plot(x,y, 'bo')
    plt.loglog(x, y, 'bo')
    plt.xlabel('Packets')
    plt.ylabel('Flows')
    plt.show()


# https://stackoverflow.com/questions/25009284/how-to-plot-roc-curve-in-python
def drawRoc(X_test, y_test, clf, score_knn):
    print("Draw ROC Curve...")

    y_pred = clf.predict(X_test)

    # Accuracy
    print("Accuracy", metrics.accuracy_score(y_test, y_pred))

    # AUC Curve
    y_pred_proba = score_knn[::, 1]

    fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)
    plt.plot(fpr, tpr, label="data 1, auc=" + str(auc))
    plt.legend(loc=4)
    plt.show()
