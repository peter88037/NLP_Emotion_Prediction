# encoding=utf-8#
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''
读取文件，获得lables和分词结果存到corpus中
包括去停用词以及标签存到label中
'''

import codecs
import re
import jieba

# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式

stopword= [line.strip().decode('utf-8') for line in open('data\stoplist.zh_TW.u8').readlines()]
labels=[]
doc=[]
###处理训练集###
with open('data\\train.tsv', 'rb') as f1 :
    for line in f1.readlines():
        matchlabel = re.match('.*?\\s(.*?)\\s', line)
        if matchlabel:
            labels.append(matchlabel.group(1))
        matchdoc = re.match('[0-9]*\s[0-9]*\s(.*)', line)
        if matchdoc:
            # doc_split=jieba.cut(matchdoc.group(1), cut_all=True)
            doc_split = jieba.cut(matchdoc.group(1))
            doc.append(" ".join(doc_split))
            # print (" ".join(doc_split))
        else:
           print "No match!!"
# print doc
print ("训练语料分词完成    1/6")
print ("标签提取完成  2/6")

with codecs.open('data\\corpus', 'w', 'utf8') as f2:
    for i in doc:
        f2.write(i+"\r\n")
print ("训练语料分词结果写入完成    3/6")
with codecs.open('data\\label', 'w', 'utf8') as f2:
    for i in labels:
        f2.write(i+",")
print ("标签写入完成  4/6")



###处理测试集###
doc_test=[]
with open('data\\test.tsv', 'rb') as f3:
    for line in f3.readlines():
        matchdoc = re.match('[0-9]*\s[0-9]*\s(.*)', line)
        if matchdoc:
            doc_split=jieba.cut(matchdoc.group(1))
            doc_test.append(" ".join(doc_split))

        else:
           print "No match!!22"
print ("测试语料分词完成    5/6")

with codecs.open('data\\corpus_test', 'w', 'utf8') as f4:
    for i in doc_test:
        f4.write(i+"\r\n")
print ("测试语料分词结果写入完成    6/6")