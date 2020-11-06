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


import requests
import shutil

manifest = "https://raw.githubusercontent.com/nakamura196/amami/master/docs/iiif/amami/manifest.json"

manifest_data = requests.get(manifest).json()

canvases = manifest_data["sequences"][0]["canvases"]

members = []

for i in range(len(canvases)):
    canvas = canvases[i]

    print(i+1, len(canvases))

    url = canvas["images"][0]["resource"]["@id"]

    id = url.split("/")[-1].replace(".jpg", "")

    opath = "data/"+id+".json"



    if os.path.exists(opath):

        try:

            with open(opath) as f:
                members_ = json.load(f)

            for member in members_:
                members.append(member)
        except Exception as e:
            print(e)


id = "amami"
    
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
                "@id": manifest,
                "@type": "sc:Manifest",
                "label": manifest_data["label"]
            }
        }
    ]
}

fw = open("curation.json", 'w')
json.dump(curation, fw, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))

