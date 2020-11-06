from PIL import Image
import sys
sys.path.append('/path/to/dir')

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))

builder = pyocr.builders.TextBuilder()
builder = pyocr.tesseract.CharBoxBuilder()
builder = pyocr.builders.LineBoxBuilder() # tesseract_layout=6

im_path = 'data/amami-1-001_OCR.jpg'

char_boxes = tool.image_to_string(
    Image.open(im_path),
    lang='jpn_vert',
    builder=builder
)

# print(char_boxes)

im = Image.open(im_path)

for box in char_boxes:
    # box.position は左下を原点とした ((min-x, min-y), (max-x, max-y)) らしい。
    # ここでは左上を原点とした x, y, width, height に変換してみる
    x = box.position[0][0]
    y = im.height - box.position[1][1]
    width = box.position[1][0] - x
    height = im.height - box.position[0][1] - y
    print("\t".join([
        box.content.replace(" ", ""),                          # 文字
        str(x), str(y), str(width), str(height),
                       # 確信度 str(box.confidence),   
    ]))

'''

txt = "|".join(box.content for box in char_boxes)
print(txt)



for box in char_boxes:
    # box.position は左下を原点とした ((min-x, min-y), (max-x, max-y)) らしい。
    # ここでは左上を原点とした x, y, width, height に変換してみる
    x = box.position[0][0]
    y = im.height - box.position[1][1]
    width = box.position[1][0] - x
    height = im.height - box.position[0][1] - y
    print("\t".join([
        box.content,                          # 文字
        str(x), str(y), str(width), str(height),
        str(box.confidence),                  # 確信度
    ]))
'''