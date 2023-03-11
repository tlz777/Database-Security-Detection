# 文本检测

---

##20230223

- [X] html/pdf报告输出
    - [ ] 报告内容/形式完善
- [X] markdown记录
- [ ] 新的敏感词检测算法讨论


## 基本环境

本地安装python，并在环境中至少下载安装numpy、PIL、time、paddleocr、pytesseract、jieba、collections、re、ahocorasick模块。

## 实现进度(含配置需求)
### 图片OCR
##### 已完成
目前已基本实现对输入图片中文字的提取。
共实现了三种OCR方式：
- 使用**百度API**实现
    - *需要联网*
- 使用**飞桨PaddleOCR**实现
    - *需要本地安装*paddleocr包*
- 使用**Pytesseract**实现
    - *需要本地安装pytesseract包*
##### todo 
根据测试效果选择最终使用的OCR方式。

### 文本处理
##### 已完成
目前已实现**去停用词分词**。
- *需要安装jieba包*



### 敏感词检测
##### 已完成
目前已基本实现根据现有敏感词表对输入文本做**敏感词检测**并**将敏感词替换成星号**。
共实现了以下敏感词检测算法：
- **AC自动机算法**
- **AC自动机算法调库**实现
  - *需要本地安装ahocorasick包*
- **DFA过滤算法**
- **DFA过滤算法 + BFS宽度优先搜索**
  - *需要本地含有collections、re包*

##### todo 
- 使用分词方式实现敏感词检测。
- 根据测试效果去选择最终使用的敏感词检测替换方式或者算法叠加使用。


### 深度学习加强检测
##### todo
- 使用深度学习扩充敏感词库，扩大敏感词检测范围。
  
## 检测流程(含接口说明)

### 图片文字提取
**输入**：图片的保存路径。
**输出**：图中的文本。
**路径接口**：
- /OCR/baidu_api.py
    >line 21 :  f = open('*路径* ', 'rb')
- /OCR/PaddleOCR.py
    >line 6 : img_path = '*路径* '
- /OCR/pytesseract.py
    >line 4 : image = Image.open('*路径* ')

    路径应位以".png 、.jpg"等结尾的图片路径形式

### 敏感词检测替换
**输入**：文本内容。
**输出**：完成敏感词替换的文本。
**路径接口**：
- /检测/AC_version2/AC自动机.py
    >line 13 :  sent = '*文本* '
- /检测/AC自动机算法/swr_use.py
    >line 2 : text=swr('*文本* ')
- /检测/DFA_version2/DFA算法.py
    >line 144 : msg = "*文本* "
- /检测/Naive_BSF_DFA算法/Naive_BSF_DFA.py
    >line 134 :  f.filter("*文本* ")
