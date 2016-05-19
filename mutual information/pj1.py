import jieba
import math
import winsound
import time, itertools
from operator import itemgetter


uniList=[]
index=dict()
emotion=dict()
indexAndEmotion=dict()
PMI=dict()
numStack=[]
finalList=[{} for m in range(40)]
#fileLength=261954
fileLength=261954
testLength=68733
tStart = time.time()

def PointwiseMutualInformation(tempIndexAndEmotionSorted):
	for i in range(len(tempIndexAndEmotionSorted)):
		andValue=tempIndexAndEmotionSorted[i][1]

		indexValue=index.get(tempIndexAndEmotionSorted[i][0].split(',')[0],0)
		emotionValue=emotion.get(tempIndexAndEmotionSorted[i][0].split(',')[1],0)

		if(indexValue<=100):  #出現詞數小於一定次數的給他去除,ex:專有名詞出現次數較少,但會導致pmi較高
			continue
		mi=math.log2((andValue*fileLength)/(indexValue*emotionValue))

		PMI[tempIndexAndEmotionSorted[i][0].split(',')[0]+','+tempIndexAndEmotionSorted[i][0].split(',')[1]]=mi
		finalList[int(tempIndexAndEmotionSorted[i][0].split(',')[1])-1][tempIndexAndEmotionSorted[i][0].split(',')[0]]=mi



file = open('train.tsv', 'r',encoding = 'utf8')
for i in range(fileLength):
	flag=0
	numflag=0
	sentence=file.readline()
	words = jieba.cut(sentence, cut_all=False)
	for word in words:
		if(word=='\n'):
			break
		if(word=='EMOTICON'):
			continue
		if((word >='a' and word <='z') or (word >='A' and word <='Z') or word==',' or word=='我'or word=='的'or word=='是'or word=='了'or word=='，'or word=='~'or word=='!'or word=='?'or word=='？'or word=='～'or word=='！'or word=='．'or word=='＂' or word=='︰' or word=='*' or word=='〔' or word=='〕'):
			continue
		if(flag==2):
			indexAndEmotion[word+','+tmp]=indexAndEmotion.get(word+','+tmp,0)+1			
			index[word]=index.get(word,0)+1
			
			if (numflag==0):
				emotion[tmp]=emotion.get(tmp,0)+1
				numflag=1
		if(flag==1):
			if(word!='\t'):
				tmp=word
		if(word=='\t'):
			flag=flag+1	

indexSorted=sorted(index.items(), key=itemgetter(1), reverse=True)	
emotionSorted=sorted(emotion.items(), key=itemgetter(1), reverse=True)	
indexAndEmotionSorted=sorted(indexAndEmotion.items(), key=itemgetter(1), reverse=True)


PointwiseMutualInformation(indexAndEmotionSorted)

wordData=[[] for m in range(40)]

countFlag=0

for x in range(40):
	countFlag=0

	tempe=sorted(finalList[x].items(), key=itemgetter(1), reverse=True)	
	for i in range(10000):
		try:
			print (tempe[i][0])
			wordData[x].append(tempe[i][0])
			countFlag=countFlag+1
		except:
			continue

		if(countFlag==100):  #控制database中,每個表情有幾個詞
			break;


file = open('output.txt', 'w', encoding = 'UTF-8')
for a in range(40):
	file.write(str(a+1))
	file.write(':')
	for b in range(10):		#作業要求,挑出10個詞output到txt中
		file.write(wordData[a][b])
		file.write(' ')
	file.write('\n')
file.close()	


an=[[] for m in range(40)]

an[0].append(1)



def test():
	scoreList=dict()

	file2 = open('test.tsv', 'r',encoding = 'utf8')
	
	file3 = open('ans.csv', 'w',encoding = 'utf8')
	file3.write('Id,Emoticon')
	for i in range(testLength):
		onoff=0
		sentence2=file2.readline()
		
		for k in range(40):     #第幾個表情之詞彙庫
			score=0
			flag=0
			words = jieba.cut(sentence2, cut_all=False)
			for word in words:
				if(onoff==0):
					num=word
					onoff=1
				if(word=='\t'):
					flag=flag+1
				if(word=='\n'):
					break
				if(word=='EMOTICON'):
					continue
				if(flag==2):
					for j in range(100):   #每個表情取前N個詞,來做測試
						if(word==wordData[k][j]):
							score=score+1

					scoreList[str(k+1)]=score
		scoreListFinal=sorted(scoreList.items(), key=itemgetter(1), reverse=True)	
		file3.write('\n'+str(num)+','+str(scoreListFinal[0][0])+' '+str(scoreListFinal[1][0])+' '+str(scoreListFinal[2][0]))
	file2.close()	
	file3.close()
	winsound.Beep(600,1000)
	tStop = time.time()
	print(tStop - tStart)
	
test()

 




