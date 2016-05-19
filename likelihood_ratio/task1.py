import nltk
import math
import csv
import string
from collections import Counter
from operator import itemgetter
import numpy as np
import bottleneck as bn
import sys
import pandas as pd
import operator
import jieba
import jieba.analyse
import re
import csv
import decimal
from decimal import Decimal, getcontext

#encoding=utf-8999

pd.options.display.encoding = sys.stdout.encoding

jieba.set_dictionary('dict.txt.big')

stopwordfile = open('stop_words.txt', 'r')
stopwords = [line.strip('\n') for line in stopwordfile.readlines()]

punct = set(u'''`۩％═﹑∼∵│ο▣☏｀ËＮßゞミゴàòΘμнт๑↖↘∕∩≦≧ⓐⓘ↓↗◆ｚ＠αγεⓡⓢ┌╭├◇✿＋＄∴・＼ｌ←＃:※!=＝－‧⊙／０)#@°ˊˋ˙１２３４５６７８９０1234567890&ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕ¯²ãçˍ¤ㄖㄗㄘㄙㄧㄨㄩㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦＡＢＥｓａｉｅｏｙｐｎｕABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,.:;~?$><＞＜=/]%}¢'"、。〉》」』】〕〗〞︰|︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！‥） ，→★☆．▃'▄▆╰▇^：；？｜｝︴＂＊*+↑︶︸︺︼︾﹀﹂﹄﹏､～￠
っあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわんをがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽや‖•·ˇˉ―--一′’”([{─ღ㊣◎●♫♡♥〃£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

adjustword = {'喜欢':'喜歡','朋有':'朋友','回忆':'回憶','买':'買'}

filterpunt = lambda s: ''.join(filter(lambda x: x not in punct, s))

def getdata(fname):

    tempsentence={}
    tempsen = []
    datas={}
    allterms=[]
    total_doc_len=0
    doc_len={}

    f = open(fname,'r+')

    for classno in range(1,41):
        tempsentence[classno] = ""
        datas[classno] = []
        doc_len[classno] = 0

    for line in f:
        total_doc_len += 1
        line = line.strip()
        num = line.split('\t')[0]
        emoticon = line.split('\t')[1]
        sentence = line.split('\t')[2].replace("EMOTICON", "").replace("\u3000", "").replace("\uf75e", "").replace("\uf787", "").replace("\uf787", "").replace("\uf6fc", "").replace("\ue5e5", "")
        doc_len[int(emoticon)] += 1
        tempsentence[int(emoticon)] += filterpunt(sentence)
        #tempsen += filterpunt(sentence)
    
    #total_term = Counter(tempsen)
    avg_doc_len = total_doc_len / 40
    b = 0.75

    for classno in range(1,41):
        seg_list = Counter(jieba.lcut(tempsentence[classno], cut_all=False))
        
        for k in seg_list:
            if k in adjustword:
                if seg_list[adjustword[k]] not in seg_list:
                    seg_list[adjustword[k]] = 0
                seg_list[adjustword[k]] += seg_list[k]
        
        for k in adjustword:
            del seg_list[k]

        datas[classno] = {i:round((seg_list[i]/(1-b+(b*doc_len[classno]/avg_doc_len)))*10) for i in seg_list if seg_list[i]/(1-b+(b*doc_len[classno]/avg_doc_len)) > 5 and i not in stopwords}

    tempmatrix = pd.DataFrame(datas).T.fillna(0)
    #class and term matrix, class for row name, term for column name
    f.close()
    likelihood(np.array(tempmatrix),list(tempmatrix.columns.values))
      
def likelihood(matrix,allterms):
    #print(matrix)
    rowlen = matrix.shape[0]
    columnlen = matrix.shape[1]
    #print(rowlen,columnlen)

    rowsum = [sum(matrix[i]) for i in range(rowlen)]
    colsum = [sum(matrix[:,i]) for i in range(columnlen)]
    N = matrix.sum()
    lrmatrix = np.zeros(shape = (rowlen, columnlen))

    record_skip = []
    for j in range(columnlen):

        for i in range(rowlen):

            n11 = matrix[i][j]
            if n11 == 0:
                record_skip.append((i,j))
                continue
            n10 = colsum[j] - n11
            n01 = rowsum[i] - n11
            n00 = N - n11 - n01 - n10
            
            if n10 == 0:
                n10 = 1
            if n00 == 0:
                n00 = 1

            pt = (n11 + n01) / float(N)
            p1 = n11 / float(n11 + n10)
            p2 = n01 / float(n01 + n00)
            
            L1 = C(n11 + n10, n11) * Decimal(math.pow(pt,n11)) * Decimal(math.pow((1-pt),n10)) * C(n01 + n00, n01) * Decimal(math.pow(pt,n01)) * Decimal(math.pow(1-pt,n00))
            L2 = C(n11 + n10, n11) * Decimal(math.pow(p1,n11)) * Decimal(math.pow((1-p1),n10)) * C(n01 + n00, n01) * Decimal(math.pow(p1,n11)) * Decimal(math.pow(1-p2,n00))

            lrmatrix[i][j] = -2* (transnum(L1) - transnum(L2))
            #if lrmatrix[i][j] > 1600:
            #    lrmatrix[i][j] = -1000000
            #print(allterms[j], lrmatrix[i][j])
            #lrmatrix[i][j] = -2 * (math.log10(L1) - math.log10(L2))
    
    for indice in record_skip:
        lrmatrix[indice[0]][indice[1]] = -1000000

    result = {}
    larges = 1
    #record = []
    
    for classno in range(40):
        result[classno+1] = []

    #templrmatrix = lrmatrix.ravel()
    #sort_index = np.argsort(templrmatrix)

    #for i, v in enumerate(sort_index):
    #    if i > 1000:
    #        break;
    #    print(v+1)
    #    indice = ( int((v+1) / columnlen), (v+1) % columnlen)
    #    if indice[1] not in record:
    #        record.append(indice[1])   
    #        result[indice[0]+1].append((allterms[indice[1]],lrmatrix[indice[0]][indice[1]])) 

    for j in range(columnlen):
        class_indexes = bn.argpartsort(-lrmatrix[:,j], n = larges)
        for c in class_indexes[0:larges]:
            print(c+1,allterms[j],lrmatrix[c][j])
            result[c+1].append((allterms[j],lrmatrix[c][j]))

    #for i in range(rowlen):
    #    result[i+1] = []
    #    class_indexes = bn.argpartsort(lrmatrix[i], n = larges)
    #    result[i+1] = sorted([(allterms[j],lrmatrix[i][j]) for j in class_indexes], key = itemgetter(1), reverse = True)[:20]

    #likelihoodmeans = lrmatrix.mean(0)
    for classno in range(40):
        result[classno+1] = sorted(result[classno+1], key = itemgetter(1), reverse = True)[:10]

    w = csv.writer(open("result.csv", "w+"))
    for key, val in result.items():
        w.writerow([key,val])
    np.savetxt('resultmatrix.csv', lrmatrix)

def C(n,r):
    c = treefactorial(n-r, 1)
    b = treefactorial(r, 1)
    a = c * treefactorial(n, n-r)
    return Decimal(a // b // c)

def range_prod(high, low):
    if low < high - 1:
        mid = (high + low) // 2
        return range_prod(low, mid) * range_prod(mid + 1, high)
    if low == high:
        return low
    return low * high

def treefactorial(n, r):
    if n < 2:
        return 1
    return range_prod(n, r)

def transnum(num):
    result = 0

    strnum = str(num)
    
    if 'E' not in strnum:
        if num == 0:
            #if '.' in strnum:
            #    temp = strnum.split('.')
            #    left = float(temp[0])
            #    right = float('-'+str(len(temp[1])))
            #    result = left - right
            #else:
            #    result = -1000000
            result = 0
            return result
        else:    
            temp = float('%E' % Decimal(num))    
            strnum = str(temp)
    
    science = strnum.split('E')
    left = float(science[0])
    right = float(science[1])

    if left > 0:
        left = math.log10(left)
        result = left + right
    else:
        result = right

    return result

getdata("train.tsv")

