import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

class Metrics(object):

    def __init__(self, arrTrue, arrPred):
        self.arrTrue = arrTrue
        self.arrPred = arrPred

    def accuracy(self):
        y_pred = self.arrPred
        y_true = self.arrTrue
        return accuracy_score(y_true, y_pred) #, normalize=False

    def f1_score(self):
        y_pred = self.arrPred
        y_true = self.arrTrue
        f1_score(y_true, y_pred, average='macro')
        f1_score(y_true, y_pred, average='micro')
        f1_score(y_true, y_pred, average='weighted')
        return f1_score(y_true, y_pred, average=None)
