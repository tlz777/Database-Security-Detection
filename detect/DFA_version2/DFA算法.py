#!/usr/bin/env python
# coding: utf-8

# ### 方法二：DFA过滤算法
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from datetime import datetime
from reportlab.platypus import Spacer
from reportlab.lib.enums import TA_CENTER

MinMatchType = 1  # 最小匹配规则
MaxMatchType = 2  # 最大匹配规则

class DFAUtils(object):
    """
    DFA算法
    """
 
    def __init__(self, word_warehouse):
        """
        算法初始化
        :param word_warehouse:词库
        """
        # 词库
        self.root = dict()
        # 无意义词库,在检测中需要跳过的（这种无意义的词最后有个专门的地方维护，保存到数据库或者其他存储介质中）
        self.skip_root = [' ', '&', '!', '！', '@', '#', '$', '￥', '*', '^', '%', '?', '？', '<', '>', "《", '》']
        # 初始化词库
        for word in word_warehouse:
            self.add_word(word)
 
    def add_word(self, word):
        """
        添加词库
        :param word:
        :return:
        """
        now_node = self.root
        word_count = len(word)
        for i in range(word_count):
            char_str = word[i]
            if char_str in now_node.keys():
                # 如果存在该key，直接赋值，用于下一个循环获取
                now_node = now_node.get(word[i])
                now_node['is_end'] = False
            else:
                # 不存在则构建一个dict
                new_node = dict()
 
                if i == word_count - 1:  # 最后一个
                    new_node['is_end'] = True
                else:  # 不是最后一个
                    new_node['is_end'] = False
 
                now_node[char_str] = new_node
                now_node = new_node
 
    def check_match_word(self, txt, begin_index, match_type=MinMatchType):
        """
        检查文字中是否包含匹配的字符
        :param txt:待检测的文本
        :param begin_index: 调用getSensitiveWord时输入的参数，获取词语的上边界index
        :param match_type:匹配规则 1：最小匹配规则，2：最大匹配规则
        :return:如果存在，则返回匹配字符的长度，不存在返回0
        """
        flag = False
        match_flag_length = 0  # 匹配字符的长度
        now_map = self.root
        tmp_flag = 0  # 包括特殊字符的敏感词的长度
 
        for i in range(begin_index, len(txt)):
            word = txt[i]
 
            # 检测是否是特殊字符"
            if word in self.skip_root and len(now_map) < 100:
                # len(nowMap)<100 保证已经找到这个词的开头之后出现的特殊字符
                tmp_flag += 1
                continue
            # 获取指定key
            now_map = now_map.get(word)
            if now_map:  # 存在，则判断是否为最后一个
                # 找到相应key，匹配标识+1
                match_flag_length += 1
                tmp_flag += 1
                # 如果为最后一个匹配规则，结束循环，返回匹配标识数
                if now_map.get("is_end"):
                    # 结束标志位为true
                    flag = True
                    # 最小规则，直接返回,最大规则还需继续查找
                    if match_type == MinMatchType:
                        break
            else:  # 不存在，直接返回
                break
        if tmp_flag < 2 or not flag:  # 长度必须大于等于1，为词
            tmp_flag = 0
        return tmp_flag
    def get_match_word(self, txt, match_type=MinMatchType):
        """
        获取匹配到的词语
        :param txt:待检测的文本
        :param match_type:匹配规则 1：最小匹配规则，2：最大匹配规则
        :return:文字中的相匹配词
        """
        matched_word_list = list()
        for i in range(len(txt)):  # 0---11
            length = self.check_match_word(txt, i, match_type)
            if length > 0:
                word = txt[i:i + length]
                matched_word_list.append(word)
                # i = i + length - 1
        return matched_word_list
    def is_contain(self, txt, match_type=MinMatchType):
        """
        判断文字是否包含敏感字符
        :param txt:待检测的文本
        :param match_type:匹配规则 1：最小匹配规则，2：最大匹配规则
        :return:若包含返回true，否则返回false
        """
        flag = False
        for i in range(len(txt)):
            match_flag = self.check_match_word(txt, i, match_type)
            if match_flag > 0:
                flag = True
        return flag
    def replace_match_word(self, txt, replace_char='*', match_type=MinMatchType):
        """
        替换匹配字符
        :param txt:待检测的文本
        :param replace_char:用于替换的字符，匹配的敏感词以字符逐个替换，如"你是大王八"，敏感词"王八"，替换字符*，替换结果"你是大**"
        :param match_type:匹配规则 1：最小匹配规则，2：最大匹配规则
        :return:替换敏感字字符后的文本
        """
        tuple_set = self.get_match_word(txt, match_type)
        word_set = [i for i in tuple_set]
        result_txt = ""
        if len(word_set) > 0:  # 如果检测出了敏感词，则返回替换后的文本
            for word in word_set:
                replace_string = len(word) * replace_char
                txt = txt.replace(word, replace_string)
                result_txt = txt
        else:  # 没有检测出敏感词，则返回原文本
            result_txt = txt
        return result_txt


if __name__ == '__main__':
    word_warehouse = ["王八蛋", "王八羔子", "你妈的", "你奶奶的", "你妈的啊"]
    msg = "你是王$八!蛋，你&&奶 奶的真有病"
    dfa = DFAUtils(word_warehouse=word_warehouse)
    print('词库结构：', json.dumps(dfa.root, ensure_ascii=False))
    # 待检测的文本
    msg = msg
    print('是否包含：', dfa.is_contain(msg))
    print('相匹配的词：', dfa.get_match_word(msg))
    print('替换包含的词：', dfa.replace_match_word(msg))

    # 设置字体
    pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttc'))

    # 设置样式
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomHeading', fontName='msyh', fontSize=14, spaceAfter=10, alignment=TA_CENTER))
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
    # 创建pdf文档
    pdf = SimpleDocTemplate("output.pdf", pagesize=letter)

    # 准备数据
    data = list(zip(["相匹配的词："]+dfa.get_match_word(msg)))

    # 创建段落和表格
    elements = []
    elements.append(Paragraph("敏感词检测报告", title_style))
    elements.append(Spacer(1, 20))
    export_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"导出时间：{export_time}", body_style))
    # elements.append(Paragraph(text, styles["CustomHeading"]))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("替换前：" + msg, styles["CustomHeading"]))
    elements.append(Spacer(1, 20))
    t = Table(data)
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
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("替换后：" + str(dfa.replace_match_word(msg)), styles["CustomHeading"]))

    # 生成pdf文档
    pdf.build(elements)


