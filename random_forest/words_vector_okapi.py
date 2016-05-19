# encoding=utf-8#
import sys
from utils import cal_len_doc
from gensim import corpora, models

reload(sys)
sys.setdefaultencoding('utf-8')
'''
根据分词后的语料生成向量空间文件svnlight格式

'''

###处理训练集###
labels = []  # 读取标签
with open('data\\label', 'rb') as f1:
    for i in f1.readlines():
        labels = i.split(',')
        # print labels
print("读取标签完成   1/5")

path_corpus_split = 'data\\corpus'  # 读取分词后语料
path_corpus_split_test = 'data\\corpus_test'  # 读取分词后语料


class MyCorpus(object):
    def __iter__(self):
        for line in open(path_corpus_split):
            yield line.split()


class MyCorpus_test():
    def __iter__(self):
        for line in open(path_corpus_split_test):
            # print line.split()
            yield line.split()


Corp = MyCorpus()
Corp_test = MyCorpus_test()
dictionary = corpora.Dictionary(Corp)  # 词典
print("字典完成     2/5")
corpus = [dictionary.doc2bow(text) for text in Corp]
corpus_test = [dictionary.doc2bow(text) for text in Corp_test]
print corpus[0][0]
aver_len_doc, list_len_doc = cal_len_doc('data\\corpus')
aver_len_test, list_len_test = cal_len_doc('data\\corpus_test')


def okapi(corpus, aver_len_doc, list_len_doc):
    k = 1.2
    b = 0.75
    for i in range(0, len(list_len_doc)):
        for j in range(0, len(corpus[i])):  # 词典里的词的数量
            tempid = corpus[i][j][0]
            tempdf = corpus[i][j][1]
            newdf = (tempdf * (k + 1) / tempdf + k * (1 - b + b * list_len_doc[i] / aver_len_doc));
            corpus[i][j] = (tempid, newdf)
    return corpus

corpus = okapi(corpus,aver_len_doc,list_len_doc)
corpus_test =okapi(corpus_test,aver_len_test,list_len_test)
print corpus[0][0]
print("训练集，测试集tf完成     3/5")
tfidf = models.TfidfModel(corpus)
tfidf_test = models.TfidfModel(corpus_test)
corpus_tfidf = tfidf[corpus]  # 得到tfidf
corpus_tfidf_test = tfidf_test[corpus_test]  # 得到tfidf
print("训练集，测试集tfidf完成   4/5")
# 输出文件为svmlight格式
corpora.SvmLightCorpus.serialize('data\corpus.svmlight', corpus_tfidf, labels=labels)
corpora.SvmLightCorpus.serialize('data\corpus_test.svmlight', corpus_tfidf_test)
print("训练集，测试集svmlight输出完成   5/5")






