from paddleocr import PaddleOCR, draw_ocr
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from datetime import datetime
from reportlab.platypus import Spacer
from reportlab.lib.enums import TA_CENTER

os.environ['KMP_DUPLICATE_LIB_OK']='True'
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
img_path = '1.jpg'
result = ocr.ocr(img_path, cls=True)
new_lst = []
for line in result:
    print(line)
    new_lst = [elem[1][0] for elem in line]

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

    pdf = SimpleDocTemplate("output_paddle.pdf", pagesize=letter)

    # 将字典中的内容以表格的形式输出到 PDF 文件中
    elements = []
    elements.append(Paragraph("图片识别报告", title_style))
    elements.append(Spacer(1, 20))
    export_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"导出时间：{export_time}", body_style))

    elements.append(Spacer(1, 20))

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

generate_pdf(new_lst)

# # 显示结果
# from PIL import Image
#
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
#
# im_show = draw_ocr(image, boxes, txts, scores, font_path='G:\大三下\数据库检测工具\demo\导出\simsun.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')
