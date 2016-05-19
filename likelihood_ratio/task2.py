import csv
import numpy as np
import jieba
import jieba.analyse
import pandas as pd

#encoding=utf-8999

pd.options.display.encoding = sys.stdout.encoding

jieba.set_dictionary('dict.txt.big')

stopwordfile = open('stop_words.txt', 'r')
stopwords = [line.strip('\n') for line in stopwordfile.readlines()]

punct = set(u'''`۩％═﹑∼∵│ο▣☏｀ËＮßゞミゴàòΘμнт๑↖↘∕∩≦≧ⓐⓘ↓↗◆ｚ＠αγεⓡⓢ┌╭├◇✿＋＄∴・＼ｌ←＃:※!=＝－‧⊙／０)#@°ˊˋ˙１２３４５６７８９０1234567890&ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕ¯²ãçˍ¤ㄖㄗㄘㄙㄧㄨㄩㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦＡＢＥｓａｉｅｏｙｐｎｕABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,.:;~?$><＞＜=/]%}¢'"、。〉》」』】〕〗〞︰|︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！‥） ，→★☆．▃'▄▆╰▇^：；？｜｝︴＂＊*+↑︶︸︺︼︾﹀﹂﹄﹏､～￠
っあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわんをがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽや‖•·ˇˉ―--一′’”([{─ღ㊣◎●♫♡♥〃£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

filterpunt = lambda s: ''.join(filter(lambda x: x not in punct, s))

datas = {}
for classno in range(40):
    datas[classno] = []


def testdata(fname):
	
	f = open(fname,'r+')
	for line in f:
		Id = line.split('\t')[0]
		sentence = filterpunt(line.split('\t')[2].replace("EMOTICON", "").replace("\u3000", "").replace("\uf75e", "").replace("\uf787", "").replace("\uf787", "").replace("\uf6fc", "").replace("\ue5e5", ""))
		print(Id, sentence)

def trainmatrix(fname):

    matrix = np.loadtxt(fname, delimiter=",")
    return matrix

    

#trainmatrix("resultmatrix.csv")
testdata("test.csv")