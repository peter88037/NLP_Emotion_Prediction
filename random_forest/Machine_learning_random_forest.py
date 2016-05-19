# encoding=utf-8#
import codecs
import sys
from sklearn.datasets import load_svmlight_file
from sklearn.externals import joblib

reload(sys)
sys.setdefaultencoding('utf-8')
'''
读取文件，用随机森林做预测

'''
from sklearn.ensemble import RandomForestClassifier

# X_train = [[0, 0], [1, 1]]
# y_train = [10, 100]
# x_test = [[0, 0], [1, 1]]

# X_test,y_test = load_svmlight_file("data\corpus_test.svmlight")
X_train, y_train = load_svmlight_file("data\\corpus.svmlight")
print X_train
print y_train
# print "x_test",X_test
# print "y_test",y_test
print "训练数据读入完成,正在训练rf模型   1/3"
clf = RandomForestClassifier(n_estimators=50)
clf = clf.fit(X_train, y_train)
print "rf模型训练完成，正在保存rf模型   2/3"
joblib.dump(clf, 'model\\randomforest50.m')
# clf = joblib.load('data\\randomforest.m')
print "rf模型保存完成   3/3"

