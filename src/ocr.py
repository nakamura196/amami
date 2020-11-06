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

builder = pyocr.tesseract.CharBoxBuilder()


txt = tool.image_to_string(
    Image.open('data/amami-1-001_OCR.jpg'),
    lang='jpn_vert',
    builder=pyocr.builders.TextBuilder()
)
print(txt)