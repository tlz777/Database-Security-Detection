# 'ersleeer'
# 2023-02-21 20:04

import os
from OCR.baidu_api import image_ocr
from detect.Naive_BSF_DFA.Naive_BSF_DFA import DFAFilter
from flask import Flask, render_template, request

app = Flask(__name__)

image_type = ["png","jpg","jpeg"]
text_type = ["txt","md"]

test_path='./test/'
filter_words_path = "./detect/Naive_BSF_DFA/dirtywords.txt"
dfa = DFAFilter()
dfa.parse(filter_words_path)
detect_result =[]

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
        text_result,detect_check = dfa.filter(text)
        res={
            'name':path,
            'detect_check':detect_check,
            'text_result':text_result
            }
        detect_result.append(res)

@app.route('/')
def main():
    return render_template('search.html',files=detect_result)

if __name__ == '__main__':
    sensitive_detection(test_path)
    print(detect_result)
    app.run()
