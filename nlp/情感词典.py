# %%
import os
import csv
import pandas as pd
import jieba
import time

def sensitive_corpus():
  '''
  生成positive和negative的词库
  '''
  df = pd.read_excel('emo.xlsx')
  print(df.head(2))
  Happy = []
  Good = []
  Surprise = []
  Anger = []
  Sad = []
  Fear = []
  Disgust = []
  for idx, row in df.iterrows():
      if row['情感分类'] in ['PA', 'PE']:
          Happy.append(row['词语'])
      if row['情感分类'] in ['PD', 'PH', 'PG', 'PB', 'PK']:
          Good.append(row['词语']) 
      if row['情感分类'] in ['PC']:
          Surprise.append(row['词语'])     
      if row['情感分类'] in ['NA']:
          Anger.append(row['词语'])    
      if row['情感分类'] in ['NB', 'NJ', 'NH', 'PF']:
          Sad.append(row['词语'])
      if row['情感分类'] in ['NI', 'NC', 'NG']:
          Fear.append(row['词语'])
      if row['情感分类'] in ['NE', 'ND', 'NN', 'NK', 'NL']:
          Disgust.append(row['词语'])
  print('情绪词语列表整理完成')   
  return Happy,Good ,Surprise,Anger, Sad,Fear,Disgust


def emotion_caculate(text):
  import jieba
  '''
  计算每一段文本的情感分数
  '''
  happy = 0
  good = 0
  surprise = 0
  anger = 0
  sad = 0
  fear = 0
  disgust = 0
  wordlist = jieba.lcut(text)
  wordset = set(wordlist)
  wordfreq = []
  for word in wordset:
      freq = wordlist.count(word)
      if word in Happy:
          happy+=freq
      if word in Good:
          good+=freq
      if word in Disgust:
          disgust+=freq
      if word in Surprise:
          surprise+=freq
      if word in Anger:
          anger+=freq
      if word in Sad:
          sad+=freq
      if word in Fear:
          fear+=freq

  emotion_info = {
        'Happy':happy,
        'Good' :good,
        'Surprise':surprise,
        'Anger':anger,
        'Sad':sad,
        'Fear':fear,
        'Disgust':disgust
  }
  indexs = ['Happy','Good' ,'Surprise', 'Anger', 'Sad','Fear','Disgust']
  return pd.Series(emotion_info, index=indexs)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandarallel import pandarallel

# 在此写入文件路径
text_path="" # 文件路径
plain_text_col_name="" # 文本列名

Happy,Good ,Surprise,Anger, Sad,Fear,Disgust = sensitive_corpus()

# 为每条文本赋予对应的情绪分数
text = pd.read_excel(text_path)
# print(weibo.head())
#并行初始化
pandarallel.initialize()
start = time.time()
def func():
    import jieba
    return text[plain_text_col_name].apply(emotion_caculate)
emotion_df = func()
# emotion_df = weibo_df['review'].parallel_apply(emotion_caculate)
end = time.time()
print(end-start)
# print(emotion_df.head())


#将情绪分数转化为二值
temp1= np.argmax(np.array(emotion_df), axis=1)
temp2= np.max(np.array(emotion_df), axis=1)
emotion_df['emotion_type'] =temp1
emotion_df['emotion_value'] =temp2
emotion_df.head()

emotion_df['emotion_type'].value_counts()
emo=emotion_df[emotion_df['emotion_value']!=0]
emo['emotion_type'].value_counts()

emotion_list= ['Happy','Good' ,'Surprise', 'Anger', 'Sad','Fear','Disgust']
for i in range(emotion_df.shape[0]):
    emotion_df['emotion_type'][i]=emotion_list[emotion_df['emotion_type'][i]]

#将文本与对应的情感合并
output_df = pd.concat([text, emotion_df['emotion_type']], axis=1)
output_df = pd.concat([output_df, emotion_df['emotion_value']], axis=1)