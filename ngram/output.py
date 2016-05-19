# encoding = utf-8#
import re
seqout=[]
seqin=[]
num = 0;

with open ('test.prob','rb') as f: 
    for line in f.readlines():
        score=re.match('.*(Total:.* OOV)',line)
        #print line
        if score:
	    #print score.group(1)[7:-4]
	    seqin.append( float(score.group(1)[7:-4]))
	    #print len(seqin)s
	    num+=1
	    if (num%40==0):
	        seqout.append(seqin)
	        seqin=[]
    print len(seqout)

with open('prediction.csv','w') as f:
    f.write("Id,Emoticon" +"\r")
    id_inial = 261955
    for i in seqout:
	dict_prediction={}
	for j in range(0,40):
	    dict_prediction[j]=i[j]
	output = sorted(dict_prediction.iteritems(),key=lambda d:d[1],reverse = True)
        f.write(str(id_inial)+','+str(output[0][0]+1)+' '+str(output[1][0]+1)+' '+str(output[2][0]+1)+'\r')
	print(str(id_inial)+','+str(output[0][0]+1)+' '+str(output[1][0]+1)+' '+str(output[2][0]+1))
	id_inial +=1

