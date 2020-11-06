import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import yaml
import requests
import glob
import io

from google.cloud import vision

import requests
import shutil

def getMember(canvas, vertices, chars, metadata, type):

    canvas_uri = canvas["@id"]

    x = vertices[0].x
    y = vertices[0].y
    w = vertices[2].x -x
    h = vertices[3].y -y

    width = canvas["width"]
    height = canvas["height"]

    if type == "object":
        x = int(width * x)
        y = int(height * y)
        w = int(width * w)
        h = int(height * h)

    member_uri = canvas_uri + "#xywh="+str(x)+","+str(y)+","+str(w)+","+str(h)

    label = "Google Cloud Vision API"


    member = {
        "@id": member_uri,
        "@type": "sc:Canvas",
        "label": label,
        "metadata": [
            {
                "label": "Text",
                "value": chars
            }
        ]
    }

    return member

def getObjects(image, canvas):
    
    members = []
    try:

        objects = client.object_localization(
            image=image).localized_object_annotations

        for object_ in objects:
            vertices = object_.bounding_poly.normalized_vertices
            label = object_.name
            metadata = [
                {
                    "label" : "score",
                    "value" : object_.score
                },
                {
                    "label" : "type",
                    "value" : "object_localization"
                }
            ]
            members.append(getMember(canvas, vertices, label, metadata, "object"))

    
    except Exception as e:
        print(e)

    return members

def getText(image, canvas):
    
    members = []
    try:
        response = client.document_text_detection(image=image)
        document = response.full_text_annotation

        for page in document.pages:
            for block in page.blocks:

                vertices = block.bounding_box.vertices

                all_text = ""

                for paragraph in block.paragraphs:

                    

                    for word in paragraph.words:
                        for symbol in word.symbols:
                            text = symbol.text
                            all_text += text

                chars = all_text

                metadata = [
                    {
                        "label" : "type",
                        "value" : "document_text_detection"
                    }
                ]

                members.append(getMember(canvas, vertices, chars, metadata, "annotation"))

    except Exception as e:
        print(e)

    return members

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

# Instantiates a client
client = vision.ImageAnnotatorClient()

manifest = "https://raw.githubusercontent.com/nakamura196/amami/master/docs/iiif/amami/manifest.json"

manifest_data = requests.get(manifest).json()

canvases = manifest_data["sequences"][0]["canvases"]

for i in range(len(canvases)):
    canvas = canvases[i]

    print(i+1, len(canvases))

    url = canvas["images"][0]["resource"]["@id"]

    path = url.replace("https://github.com/nakamura196/amami/raw/master/", "../../")

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    id = path.split("/")[-1].replace(".jpg", "")

    # OCR
    if True:

        opath = "data/"+id+".json"

        if not os.path.exists(opath):

            print("Text Detection")
            members_ = getText(image, canvas)

            fw = open(opath, 'w')
            json.dump(members_, fw, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))


'''

dir = "../../docs/iiif/item"

files = glob.glob(dir+"/*/manifest.json")

for file in files:
    

    with open(file) as f:
        df = json.load(f)

    id = file.split("/item/")[1].replace("/manifest.json", "")

    if "003_014" not in id:
        continue

    manifest_uri = df["@id"]
    print(manifest_uri)

    sequences = df["sequences"]

    members = []

    odir = "../../docs/iiif/curation/" + id
    os.makedirs(odir, exist_ok=True)

    opath =  odir + "/curation.json"

    if False:
        if os.path.exists(opath):
            continue

    for i in range(len(sequences)):

        canvases = sequences[i]["canvases"]

        for j in range(len(canvases)):

            if False:
                if j != 1:
                    continue

            print(str(j)+"/"+str(len(canvases)))
            canvas = canvases[j]
            

            path = canvas["images"][0]["resource"]["@id"]

            tmp_path = "tmp.jpg"

            if path.startswith('http') or path.startswith('gs:'):
                tmp = path.split("https://")
                path = "https://cj:!cj@"+tmp[1]
                download_img(path, tmp_path)

            with io.open(tmp_path, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            # OCR
            if True:
                print("Text Detection")
                members_ = getText(image, canvas)
                print(len(members_))
                for member in members_:
                    members.append(member)
            

            # Object Detection
            print("Object Detection")
            members_ = getObjects(image, canvas)
            print(len(members_))
            for member in members_:
                members.append(member)

            # break
    
    curation = {
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://codh.rois.ac.jp/iiif/curation/1/context.json"
        ],
        "@id": "https://umesao.cultural.jp/iiif/curation/"+id+"/curation.json",
        "@type": "cr:Curation",
        "label": "Character List",
        "selections": [
            {
                "@id": "https://umesao.cultural.jp/iiif/curation/"+id+"/range1",
                "@type": "sc:Range",
                "label": "Characters",
                "members": members,
                "within": {
                    "@id": manifest_uri,
                    "@type": "sc:Manifest",
                    "label": df["label"]
                }
            }
        ]
    }

    fw = open(opath, 'w')
    json.dump(curation, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))

'''