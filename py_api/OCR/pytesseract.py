from PIL import Image
import pytesseract

image = Image.open('D:\\tesseract_ocr\\test1.png')	# 打开图片
result = pytesseract.image_to_string(image, 'chi_sim')
# 转化str，注意'chi_sim'是语言包库
print(result)
