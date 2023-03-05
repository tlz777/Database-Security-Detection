# 'ersleeer'
# 2022-08-03 18:35

import requests
import base64
import urllib3
# requests.packages.urllib3.disable_warnings()

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus import Image as PlatypusImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from datetime import datetime
from reportlab.platypus import Spacer
from reportlab.lib.enums import TA_CENTER

from PIL import Image
from reportlab.lib.units import inch

'''
通用文字识别
'''

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=fqq2vFRXkzGmFPArh5d2YBL0&client_secret=pgUz5rUqcstIUgdjbnNUHSI0sQRYD2Fd'
response = requests.get(host)
if response:
    print(response.json())

request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
# 二进制方式打开图片文件
f = open('1.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image": img}
access_token = response.json()['access_token']
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print(response.json())


def generate_pdf(data):
    # 创建一个新的 PDF 文件
    pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttc'))

    # 设置样式
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomHeading',
                              fontName='msyh',
                              fontSize=14,
                              spaceAfter=10,
                              alignment=TA_CENTER))
    # 定义样式
    # 定义标题样式
    title_style = ParagraphStyle(name="title",
                                 fontName="msyh",
                                 fontSize=24,
                                 leading=28,
                                 alignment=TA_CENTER)

    # 定义正文样式
    body_style = ParagraphStyle(name="body",
                                fontName="msyh",
                                fontSize=12,
                                leading=16,
                                alignment=TA_CENTER)

    pdf = SimpleDocTemplate("output_baidu.pdf", pagesize=letter)

    # 将字典中的内容以表格的形式输出到 PDF 文件中
    elements = []
    elements.append(Paragraph("图片识别报告", title_style))
    elements.append(Spacer(1, 20))
    export_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"导出时间：{export_time}", body_style))

    elements.append(Spacer(1, 20))

    # # 计算图像的缩放比例，将其调整为1英寸
    # img_width, img_height = PlatypusImage('1.jpg').wrap(0.001 * inch, 0.001 * inch)
    #
    # # 将图像添加到PDF中
    # elements.append(PlatypusImage('1.jpg', width=img_width, height=img_height))

    # 构建要输出的文本
    text = list(zip(["识别到的词："] + data))

    t = Table(text)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'msyh'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'msyh'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    pdf.build(elements)


data = [x['words'] for x in response.json()['words_result']]
generate_pdf(data)
