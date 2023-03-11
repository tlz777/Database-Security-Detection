#!/usr/bin/env python
# coding: utf-8

# # 自然语言处理

# 自然语言实现一般都通过以下几个阶段：文本读取、分词、清洗、标准化、特征提取、建模。
# 
# 首先通过文本、新闻信息、网络爬虫等渠道获取大量的文字信息。
# 
# 然后利用分词工具对文本进行处理，把语句分成若干个常用的单词、短语，由于各国的语言特征有所区别，所以NLP也会有不同的库支撑。
# 
# 对分好的词库进行筛选，排除掉无用的符号、停用词等。
# 
# 再对词库进行标准化处理，比如英文单词的大小写、过去式、进行式等都需要进行标准化转换。
# 
# 然后进行特征提取，利用 tf-idf、word2vec 等工具包把数据转换成词向量。
# 
# 最后建模，利用机器学习、深度学习等成熟框架进行计算。

# ![jupyter](./1.jpg)

# ## 分词器

# ### NLTK库

# In[12]:


import nltk
nltk.download('punkt')


# In[13]:


sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
paragraph = "The first time I heard that song was in Hawaii on radio. I was just a kid, and loved it very much! What a fantastic song!"
sentences = sent_tokenizer.tokenize(paragraph)
print(sentences)


# In[16]:


from nltk.tokenize import WordPunctTokenizer
sentence = "Are you old enough to remember Michael Jackson attending the Grammys with Brooke Shields and Webster sat on his lap during the show?"
words = WordPunctTokenizer().tokenize(sentence)
print(words)


# 最简单的方法去掉一些从文档中存在的 \n \t 等符号

# In[17]:


from nltk.tokenize import RegexpTokenizer
sentence='Thomas Jefferson began \n building \t Monticello at the age of 26.'
tokenizer=RegexpTokenizer(r'\w+|$[0-9.]+|\S+')
print(tokenizer.tokenize(sentence))


# TreebankWordTokenizer 拥有比 WordPunctTokenizer  更强大的分词功能，它可以把 don't 等缩写词分为[ "do" , " n't " ] 

# In[18]:


from nltk.tokenize import TreebankWordTokenizer
sentence="Sorry! I don't know."
tokenizer=TreebankWordTokenizer()
print(tokenizer.tokenize(sentence))


# In[19]:


from nltk.stem import porter as pt
words = [ 'wolves', 'playing','boys','this', 'dog', 'the',
            'beaches', 'grounded','envision','table', 'probably']
stemmer=pt.PorterStemmer()
for word in words:
    pt_stem = stemmer.stem(word)
    print(pt_stem)


# 可以 playing boys grounded 都被完美地还原，但对 this table 等单词也会产生歧义，这是因为被原后的单词不一定合法的单词。

# In[24]:


import nltk
nltk.download('wordnet')


# In[26]:


nltk.download('omw-1.4')


# In[27]:


from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
stemmer=PorterStemmer()
wordnet=WordNetLemmatizer()
word1=wordnet.lemmatize('boys',pos='n')
print(word1)

word2=wordnet.lemmatize('goodness',pos='a')
word2=stemmer.stem(word2)
print(word2)


# In[29]:


nltk.download('stopwords')


# In[31]:


from nltk.corpus import stopwords 
stopword=stopwords.raw('english').replace('\n',' ')
print(stopword)


# In[32]:


words = [ 'the', 'playing','boys','this', 'dog', 'a',]
stopword=stopwords.raw('english').replace('\n',' ')
words=[word for word in words if word not in stopword]
print(words)


# ###  jieba

# def cut(self, sentence, cut_all=False, HMM=True, use_paddle=False):  
# 
# - sentence 可为 unicode 、 UTF-8 字符串、GBK 字符串。注意：不建议直接输入 GBK 字符串，可能无法预料地错误解码成 UTF-8。
# 
# - 当 cut_all 返回 bool，默认为 False。当 True 则返回全分割模式，为 False 时返回精准分割模式。
# 
# - HMM 返回 bool，默认为 True，用于控制是否使用 HMM 隐马尔可夫模型。
# 
# - use_paddle 返回 bool,  默认为 False, 用来控制是否使用paddle模式下的分词模式，paddle模式采用延迟加载方式，利用PaddlePaddle深度学习框架，训练序列标注（双向GRU）网络模型实现分词，同时支持词性标注。

# In[38]:


import jieba
sentence='嫦娥四号着陆器地形地貌相机对玉兔二号巡视器成像'
word1=jieba.cut(sentence,False)
print(list(word1))
word2=jieba.cut(sentence,True)
print(list(word2))


# jieba.cut_for_search 与 jieba.cut 精确模式类似，只是在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词，返回值为 generator。
# 
# def cut_for_search(self,sentence: Any,HMM: bool = True) -> Generator[str, Any, None]

# In[39]:


word1=jieba.cut_for_search('尼康Z7II是去年底全新升级的一款全画幅微单相机',False)
print(list(word1))
word2=jieba.cut_for_search('尼康Z7II是去年底全新升级的一款全画幅微单相机',True)
print(list(word2))


# 载入新词  jieba.load_userdict 
# 
# 通过此方法可以预先载入自定义的用词，令分词更精准。文本中一个词占一行，每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒。
# 
# 例如：设定 word.txt 文本
# 
# 阿里云   1    n
# 
# 云计算   1    n

# In[40]:


word1=jieba.cut('阿里云是全球领先的云计算及人工智能科技公司')
print(list(word1))
jieba.add_word('阿里云')
jieba.add_word('云计算')
word2=jieba.cut('阿里云是全球领先的云计算及人工智能科技公司')
print(list(word2))
jieba.del_word('阿里云')
word3=jieba.cut('阿里云是全球领先的云计算及人工智能科技公司')
print(list(word3))


# In[42]:


from jieba import posseg
words=jieba.posseg.cut('阿里云是全球领先的云计算及人工智能科技公司')
for word,flag in words:
     print(word,flag)


# ## 词向量

# ### one-hot 独热向量

# In[46]:


import numpy as np

def getWords():
    # 对句子进行分词
    sentence='珠穆朗玛峰上的星空是如此的迷人'
    words=jieba.lcut(sentence)
    print('【原始语句】：{0}'.format(sentence))
    print('【分词数据】：{0}'.format(words))
    return words
 
def getTestWords():
    # 把词集进行重新排序后作为测试数据
    words=getWords().copy()
    words.sort()
    print('【测试数据】：{0}'.format(words))
    return words

def one_hot_test():
    # 获取分词后数据集
    words=getWords()
    # 获取测试数据集
    testWords=getTestWords()
    size=len(words)
    onehot_vectors=np.zeros((size,size),int)
    # 获取测试数据 one_hot 向量
    for i,word in enumerate(testWords):
        onehot_vectors[i,words.index(word)]=1
    return onehot_vectors

if __name__=='__main__':
    print(one_hot_test())


# 很直观，但是也浪费了很多的数据空间,所以这方法的实用性比较低。

# ### TF-IDF 向量

# TF 词频是代表词在单篇文章中出现的频率
# 
# 而 IDF 逆文本频率指数是代表词语在文档中的稀缺程度，它等总文件数目除以包含该词语之文件的数目，再将得到的商取以10为底的对数得到 。
# 
# TF-IDF 顾名思义就是代表 TF 与 IDF 的乘积

# In[52]:


from sklearn.feature_extraction.text import TfidfVectorizer
corpus = [
    'In addition to having a row context',
    'Usually a smaller text field',
    'The TFIDF idea here might be calculating some rareness of words',
    'The larger context might be the entire text column',
]

def stopWord():
    # 读取停用词
    stopword=[line.strip() for line in open('E:/jupyter_project/stopwords/四川大学机器智能实验室停用词库.txt','r',1024,'utf8')
        .readlines()]
    return stopword

def tfidfVectorizerTest():
    words=corpus
    #建立tfidf模型
    vertorizer=TfidfVectorizer(stop_words=stopWord(),ngram_range=(1,2))
    #训练与运算
    model=vertorizer.fit_transform(words)
    #显示分词
    print(vertorizer.vocabulary_)
    #显示向量
    print(model)

if __name__=='__main__':
    tfidfVectorizerTest()


# In[55]:


corpus = [
    '北京冬奥会完美落下帷幕',
    '冬奥生态内容方面的表现给用户留下深刻印象',
    '全平台创作者参与冬奥内容创作',
    '此次冬奥会对于中国是一次重要的里程碑时刻',
]

def stopWord():
    # 读取停用词
    stopword=[line.strip() for line in open('E:/jupyter_project/stopwords/四川大学机器智能实验室停用词库.txt','r',1024,'utf8')
        .readlines()]
    return stopword

def getWord():
    # 转换集合格式后再进行分词
    list=[jieba.lcut(sentence) for sentence in corpus]
    # 在每个词中添加空格符
    word=[' '.join(word) for word in list]
    return word

def tfidfVectorizerTest():
    words=getWord()
    # 打印转换格式后的分词
    print(str.replace('格式转换:{0}\n'.format(words),',','\n\t\t'))
    # 建立模型
    vertorizer=TfidfVectorizer(stop_words=stopWord())
    # 模型训练
    model=vertorizer.fit_transform(words)
    print('分词:{0}\n'.format(vertorizer.vocabulary_))
    print(model)

if __name__=='__main__':
    tfidfVectorizerTest()


# ## 文本相似度分析

# 根据余弦相似度，可以对 TF-IDF 向量进行比较，计算出文本之间的关联度。此原理常被广泛应用于聊天机器人，车机对话，文本自动回复等领域。先预设多个命令与回复，计算出 TF-IDF 向量，然后把输入的命令 TF-IDF 向量与预设命令的 TF-IDF 向量进行对比，找出相似度最高的命令，最后输出相关的回复。
# 
# 下面以车机系统为例子，说明一下文本相似度计算的应用。command 代表多个车机的预设命令与回复数组，先通过 jieba 把中文命令转化为相关格式，对 TfidfVectorizer 模型进行训练。然后分别计算 command 预计命令的 TF-IDF 向量和 inputCommand 输入命令的 TF-IDF 向量。通过余弦相似度对比，找到相似度最高的命令，最后输出回复。

# In[69]:


from sklearn.metrics.pairwise import cosine_similarity
# 车机的命令与回复数组
command=[['请打开车窗','好的，车窗已打开'],
         ['我要听陈奕迅的歌','为你播放富士山下'],
         ['我好热','已为你把温度调到25度'],
         ['帮我打电话给小猪猪','已帮你拨小猪猪的电话'],
         ['现在几点钟','现在是早上10点'],
         ['我要导航到中华广场','高德地图已打开'],
         ['明天天气怎么样','明天天晴']
        ]

# 利用 jieba 转换命令格式
def getWords():
    comm=np.array(command)
    list=[jieba.lcut(sentence) for sentence in comm[:,0]]
    words=[' '.join(word) for word in list]
    return words

# 训练 TfidfVectorizer 模型
def getModel():
    words=getWords()
    vectorizer=TfidfVectorizer()
    model=vectorizer.fit(words)
    print(model.vocabulary_)
    return model

# 计算 consine 余弦相似度
def consine(inputCommand):
    # 把输入命令转化为数组格式
    sentence=jieba.lcut(inputCommand)
    words=str.join(' ',sentence)
    list=[]
    list.insert(0,words)
    # 获取训练好的 TfidfVectorizer 模型
    model=getModel()
    # 获取车机命令的 TF-IDF 向量
    data0=model.transform(getWords()).toarray().reshape(len(command),-1)
    # 获取输入命令的 TF-IDF 向量
    data1=model.transform(list).toarray().reshape(1,-1)
    # 余弦相似度对比
    result=cosine_similarity(data0,data1)
    print('相似度对比：\n{0}'.format(result))
    return result

if __name__=='__main__':
    comm='我要听陈奕迅的歌'
    # 获取余弦相似度
    result=np.array(consine(comm))
    # 获取相似度最高的命令 index
    argmax=result.argmax()
    # 读取命令回复
    data=command[argmax][1]
    print('命令：{0}\n回复：{1}'.format(comm,data))


# ## 通过主题转换进行语义分析

# ### LSA (Latent Semantic Analysis 隐性语义分析)

# LSA 可用于文本的主题提取，挖掘文本背后的含义、数据降维等方面。例如一篇文章的分词中 “ 服务、协议、数据交换、传输对象” 占比较大的，可能与 “ 云计算 ” 主题较为接近; “ 分词、词向量、词频、相似度” 占比较大的可能与 " 自然语言开发 " 主题较为接近。在现实的搜索引擎中，普通用户所输入的关键词未必能与分词相同，通过核心主题分析，往往更容易找出相关的主题文章，这正是 LSA 语义分析的意义。

# LSA 是一种分析 TF-IDF 向量的算法，它是基于 SVD ( Singular Value Decomposition 奇异值分解 ) 技术实现的。SVD 是将矩阵分解成三个因子矩阵的算法，属于无监督学习模型，这种算法也被常用在图像分析领域。
# 在图像分析领域 SVD 也被称作 PCA 主成分分析

# - 转换主题时可先利用 TfidfVectorizer 将数据进行 TF-IDF 向量化，然后使用 TruncatedSVD 模型设置转换输出的主题类型数量，对主题的相关数据进行情感分析。

# #### TruncatedSVD 模型

# ### 线性判别分析（Linear Discriminant Analysis，简称 LDA）

#  LDA  属于监督学习模型.LDA 的主要思想是将一个高维空间中的数据投影到一个较低维的空间中，且投影后要保证各个类别的类内方差小而类间均值差别大，这意味着同一类的高维数据投影到低维空间后相同类别会尽量聚在一起，而不同类别之间相距较远。

# #### LinearDiscriminantAnalysis 模型

# ### LDiA 隐性狄利克雷分布

# 隐性狄利克雷分布 ( Latent Dirichlet Allocation，简称 LDiA）与 LSA 类似也是一种无监督学习模型，但与相对于 LSA 的线性模型不同的是 LDiA 可以将文档集中每篇文档的主题按照概率分布的形式给出，从而更精确地统计出词与主题的关系。

# #### LatentDirichletAllocation 模型

# In[ ]:




