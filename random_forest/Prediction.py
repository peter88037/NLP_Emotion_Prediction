# encoding=utf-8#
from sklearn.datasets import load_svmlight_file
from sklearn.externals import joblib

clf = joblib.load( 'model\\randomforest50.m')
print "模型加载完成，正在加载数据   1/4"

X_test,y_test = load_svmlight_file("data\\corpus_test.svmlight")
print "数据加载完成，正在预测   2/4"

# doc_class_predicted = clf.predict(X_test)
pro_class_predicted=clf.predict_proba(X_test)
print "模型预测完成，正在输出结果   3/4"

with open('data/prediction.csv', 'w') as f:
    f.write("Id,Emoticon" + "\r")
    id_inial = 261955;
    for i in pro_class_predicted:
        dict_Prediction={}
        for j in range(0,40):
            dict_Prediction[j]=i[j]
        output=sorted(dict_Prediction.iteritems(), key=lambda d:d[1], reverse=True)
        # print output[0][0]
        f.write( str(id_inial) + ',' + str(output[0][0]+1)+' '+ str(output[1][0]+1)+ ' '+ str(output[2][0]+1) +'\r')
        id_inial = id_inial + 1

print "结果输出完成   4/4"