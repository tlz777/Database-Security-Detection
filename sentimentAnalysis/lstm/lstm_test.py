import jieba
import numpy as np
import yaml
import sys
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence
from keras import backend as K
from keras.models import model_from_yaml
import json
from keras.models import model_from_json

np.random.seed(1337)  # For Reproducibility
sys.setrecursionlimit(1000000)
# define parameters
maxlen = 100
w2indx = {}
f = open("./sentimentAnalysis/lstm/word2index.txt",'r',encoding='utf8')
lines = f.readlines()
for line in lines:
    if line.strip()=='':
        continue
    s= line.split()
    w2indx[s[0]]=int(s[1])
f.close()

# def create_dictionaries(model=None,
#                         combined=None):
#     ''' Function does are number of Jobs:
#         1- Creates a word to index mapping
#         2- Creates a word to vector mapping
#         3- Transforms the Training and Testing Dictionaries

#     '''
#     if (combined is not None) and (model is not None):
#         w2indx={}
#         gensim_dict = Dictionary()
#         gensim_dict.doc2bow(model.wv.vocab.keys(),
#                             allow_update=True)
#         #  freqxiao10->0 所以k+1
#         f = open("word2index.txt",'r',encoding='utf8')
#         lines = f.readlines()
#         for line in lines:
#             if line.strip()=='':
#                 continue
#             s= line.split()
#             w2indx[s[0]]=int(s[1])
#         f.close()
#         #w2indx = {v: k+1 for k, v in gensim_dict.items()}#所有频数超过10的词语的索引,(k->v)=>(v->k)
#         w2vec = {word: model[word] for word in w2indx.keys()}#所有频数超过10的词语的词向量, (word->model(word))
#         def parse_dataset(combined): # 闭包-->临时使用
#             ''' Words become integers
#             '''
#             data=[]
#             for sentence in combined:
#                 new_txt = []
#                 for word in sentence:
#                     try:
#                         new_txt.append(w2indx[word])
#                     except:
#                         new_txt.append(0) # freqxiao10->0
#                 data.append(new_txt)
#             return data # word=>index
#         combined=parse_dataset(combined)
#         combined= sequence.pad_sequences(combined, maxlen=maxlen)#每个句子所含词语对应的索引，所以句子中含有频数小于10的词语，索引为0
#         print(combined)
#         return w2indx, w2vec,combined
#     else:
#         print ('No data provided...')

def create_dictionaries(words):
    data =[]
    for sentence in words:
        new_txt = []
        for word in sentence:
            try:
                new_txt.append(w2indx[word])
            except:
                new_txt.append(0)
        data.append(new_txt)
    combined= sequence.pad_sequences(data, maxlen=maxlen)
    return combined



def input_transform(string):
    words=jieba.lcut(string)
    print(words)
    words=np.array(words).reshape(1,-1)
    #model=Word2Vec.load('../model/Word2vec_model.pkl')
    #_,_,combined=create_dictionaries(model,words)
    combined = create_dictionaries(words)

    return combined


def lstm_predict(string):
    f1 = open('comments_sentiment.txt','a+')
    print ('loading model......')
    with open('./sentimentAnalysis/model/lstm.json', 'r') as f:
        json_string = json.load(f)
    model = model_from_json(json_string)

    print ('loading weights......')
    model.load_weights('./sentimentAnalysis/model/lstm.h5')
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    data=input_transform(string)
    data.reshape(1,-1)
    # print(data)
    # result=model.predict_classes(data)
    result=model.predict(data)
    # print(result)
    return result[0]

if __name__=='__main__':
    string='我爱生活，生活爱我'
    # f =  open('../../step1_cut_words/raw data/comments.txt','r')
    # lines = f.readlines()
    # for line in lines:
    #    lstm_predict(line)
    lstm_predict(string)
    