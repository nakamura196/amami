import sys
import urllib
import json
import argparse
import urllib.request
import csv
import os
import yaml
import glob
from PIL import Image

prefix = "https://github.com/nakamura196/amami/raw/master/docs"
prefix2 = "../docs"

files = sorted(glob.glob("../docs/files/large/*.jpg"))

canvases = []

canvas_prefix = prefix + "/iiif/amami"

for i in range(len(files)):
    file = files[i]

    print(file)
    im = Image.open(file)
    w,h = im.size

    print(w,h)

    index = str(i+1)

    canvas_uri = canvas_prefix+"/canvas/p" + index

    url = file.replace(prefix2, prefix)

    canvas = {
        "@id": canvas_uri,
        "@type": "sc:Canvas",
        "label": "["+index+"]",
        "thumbnail": {
            "@id": url.replace("/large/", "/medium/")
        },
        "width": w,
        "height": h,
        "images": [
            {
            "@id": canvas_prefix + "/annotation/p"+index.zfill(4)+"-image",
            "@type": "oa:Annotation",
            "motivation": "sc:painting",
            "on": canvas_uri,
            "resource": {
                "@id": url,
                "@type": "dctypes:Image",
                "format": "image/jpeg",
                "height": h,
                "width": w
            }
            }
        ]
    }

    canvases.append(canvas)
    
# print(canvases)

manifest = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": "https://utda.github.io/shelly/manifest.json",
    "@type": "sc:Manifest",
    "label": "奄美大島",
    "sequences": [
      {
        "@id": "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/e3e3be43-358d-47bf-a245-d52ffe4ed866/sequence/normal",
        "@type": "sc:Sequence",
        "label": "Current Page Order",
        "viewingHint": "non-paged",
        "canvases": canvases
      }
    ]
}

# print(manifest)
    

fw = open("../docs/iiif/amami/manifest.json", 'w')
json.dump(manifest, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
