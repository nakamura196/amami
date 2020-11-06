from PIL import Image
import sys
sys.path.append('/path/to/dir')
import json
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

with open('../docs/iiif/amami/manifest.json') as f:
    df = json.load(f)

canvases = df["sequences"][0]["canvases"]

members = []

for i in range(len(canvases)):
    print(i+1, len(canvases))

    if i > 10:
      break

    page = str(i+1).zfill(4)
    canvas = canvases[i]
    canvas_id = canvas["@id"]

    image_url = canvas["images"][0]["resource"]["@id"]

    filename = image_url.split("/")[-1]

    im_path = "../docs/files/large/"+filename

    char_boxes = tool.image_to_string(
        Image.open(im_path),
        lang='jpn_vert',
        builder=builder
    )

    # print(char_boxes)

    im = Image.open(im_path)

    for j in range(len(char_boxes)):
        box = char_boxes[j]
        x = box.position[0][0]
        y = box.position[0][1]
        width = box.position[1][0] - x
        height = box.position[1][1] - y
        text =  box.content.replace(" ", "")

        '''
        print("\t".join([
            text,                          # 文字
            str(x), str(y), str(width), str(height),
                        # 確信度 str(box.confidence),   
        ]))
        '''

        if j > 10 and False:
          break

        if text == "":
          continue

        member_id = canvas_id+"#xywh="+str(x)+","+str(y)+","+str(width)+","+str(height)

        
        member = {
          # "label": text,
          "metadata": [
            {
              "label": "Text",
              "value": text
            }
          ],
          "@id": member_id,
          "@type": "sc:Canvas"
        }

        members.append(member)

    # break



curation = {
  "@context": [
    "http://iiif.io/api/presentation/2/context.json",
    "http://codh.rois.ac.jp/iiif/curation/1/context.json"
  ],
  "@type": "cr:Curation",
  "@id": "https://mp.ex.nii.ac.jp/api/curation/json/aaa5d585-3cd2-4651-ba98-71769b028e19",
  "label": "Curating list",
  "selections": [
    {
      "@id": "https://mp.ex.nii.ac.jp/api/curation/json/aaa5d585-3cd2-4651-ba98-71769b028e19/range1",
      "@type": "sc:Range",
      "label": "Manual curation by IIIF Curation Viewer",
      "members": members,
      "within": {
        "@id": "https://raw.githubusercontent.com/nakamura196/amami/master/docs/iiif/amami/manifest.json",
        "@type": "sc:Manifest",
        "label": "奄美大島"
      }
    }
  ]
}

fw = open("../docs/curation/test_line.json", 'w')
json.dump(curation, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
