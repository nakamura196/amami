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

with open('../docs/curation/block.json') as f:
    df = json.load(f)

with open('../docs/iiif/amami/manifest.json') as f:
    mdata = json.load(f)

canvases = mdata["sequences"][0]["canvases"]

canvasMap = {}

for canvas in canvases:
  

members = df["selections"][0]["members"]

for member in members:


canvases = df["sequences"][0]["canvases"]

members = []

for i in range(len(canvases)):
    canvas_id = canvases[i]["@id"]
    ys = [[1600, 2400, 3150, 3200 + 800], [4500, 5250, 6000, 6000 + 800]]
    
    if i % 2 == 0:
        xs = [770, 2700, 2700 + 1900]
       
    else:
        xs = [1000, 2800, 2800 + 1900]

    r = 2400 / 5457

    for y in ys:

        for j in range(0, len(xs) - 1):
            x1 = xs[len(xs) - j - 2]
            x2 = xs[len(xs) - j - 1]
            w = x2 - x1

            for k in range(len(y) - 1):
                y1 = y[k]
                y2 = y[k + 1]
                h = y2 - y1

                member_id = canvas_id+"#xywh="+str(int(x1 * r))+","+str(int(y1 * r))+","+str(int(w*r))+","+str(int(h*r))
                members.append({
                    "@id": member_id,
                    "@type": "sc:Canvas",
                    "label": "["+str(i+1)+"]",
                    "description": ""
                })

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

fw = open("../docs/curation/block.json", 'w')
json.dump(curation, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
