# 'ersleeer'
# 2023-02-21 20:04

import os
from OCR.baidu_api import image_ocr
from detect.Naive_BSF_DFA.Naive_BSF_DFA import DFAFilter
from flask import Flask, render_template, request
from detect.AC_version2.AC2 import build_actree
from sentimentAnalysis.lstm.lstm_test import lstm_predict
import pdfkit
app = Flask(__name__)

image_type = ["png","jpg","jpeg"]
text_type = ["txt","md","csv"]

test_path='./test/'
filter_words_path = "./detect/Naive_BSF_DFA/dirtywords.txt"
# dfa = DFAFilter()
# dfa.parse(filter_words_path)
detect_result =[]
wordlist = []
from xpinyin import Pinyin
p = Pinyin()

with open(filter_words_path, encoding="UTF-8") as f:
    for keyword in f:
        ks = keyword.strip()
        result = p.get_pinyin(ks)
        wordlist.append(ks)
        s = result.split('-')
        if s != ['']:
            for i in range(len(s)):
                ks_copy = ks.replace(ks[i],s[i])
                wordlist.append(ks_copy)

actree = build_actree(wordlist=wordlist)

def sensitive_detection(test_path):
    global detect_result
    for file in os.listdir(test_path):
        print("== file:",file," ==")
        path = test_path+file
        type = file.split(".")[-1]
        if type in image_type:
            words_dic = image_ocr(path)
            words_list = [word['words'] for word in words_dic]
            text = "\n".join(words_list)
        elif type in text_type:
            f = open(path,encoding="utf-8")
            data = f.readlines()
            text = "\n".join(data)
            f.close()
        # text_result,detect_check = dfa.filter(text)
        detect_check = False
        text_result = text

        lstm_res = lstm_predict(text)
        if lstm_res[2]>0.8:
            detect_check = True
        for i in actree.iter(text):
            text_result = text_result.replace(i[1][1], "**")
            detect_check = True
        res={
            'name':path,
            'detect_check':detect_check,
            'text_result':text_result
        }
        detect_result.append(res)

@app.route('/')
def main():
    GEN_HTML = "./output/res.html"
    f = open(GEN_HTML, 'w',encoding='utf-8')
    html_content = render_template('search.html',files=detect_result)
    f.write(html_content)
    # 将wkhtmltopdf.exe程序绝对路径传入config对象
    # 注意，这里要改成自己的exe路径！
    path_wkthmltopdf = r'G:/giigle/wkhtmltox/bin/wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    # 生成pdf文件，to_file为文件路径
    f.close()
    pdfkit.from_file("./output/res.html", "./output/res.pdf", configuration=config)

    return html_content

if __name__ == '__main__':
    sensitive_detection(test_path)
    print(detect_result)
    app.run()
