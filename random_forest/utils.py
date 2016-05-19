from gensim import corpora
from gensim.corpora import dictionary

def cal_len_doc(addr):
    with open(addr, 'rb') as f1 :
        len_doc=[]
        for line in f1.readlines():
            context=line.split(" ");
            len_doc.append(len(context))
    # print len(len_doc)
    sum_doc=0
    for i in len_doc:
        sum_doc=sum_doc+i
        # print sum_doc
    aver_len_doc= sum_doc/len(len_doc)
    return aver_len_doc,len_doc
