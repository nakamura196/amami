import sys
import urllib
import json
import argparse
import urllib.request
import unicodedata
import collections
import os
import xml.etree.ElementTree as ET
import csv
import glob
import urllib.parse

def get_mdata(manifest):
    print(manifest)
    res = urllib.request.urlopen(manifest)
    # json_loads() でPythonオブジェクトに変換
    data = json.loads(res.read().decode('utf-8'))

    canvases = data["sequences"][0]["canvases"]
    
    map = {}

    for i in range(len(canvases)):
        canvas = canvases[i]
        canvas_id = canvas["@id"]
        width = canvas["width"]
        height = canvas["height"]
        url = canvas["images"][0]["resource"]["@id"]

        map[canvas_id] = {
            "width": width,
            "height": height,
            "url": url
        }


    return map


prefix = ".//{http://www.tei-c.org/ns/1.0}"
xml = ".//{http://www.w3.org/XML/1998/namespace}"

tmp_path = "data/template.xml"

tree = ET.parse(tmp_path)
ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
ET.register_namespace('xml', "http://www.w3.org/XML/1998/namespace")
root = tree.getroot()

para = root.find(prefix + "body").find(prefix + "div")

surfaceGrp = root.find(prefix+"surfaceGrp")


with open("../001_gcv/curation.json", 'r') as f:
    curation= json.load(f)

manifest = curation["selections"][0]["within"]["@id"]
title = curation["selections"][0]["within"]["label"]

surfaceGrp.set("facs", manifest)

canvas_data = get_mdata(manifest)

prev_page = -1

canvas_map = {}

members = curation["selections"][0]["members"]

for i in range(len(members)):
    member = members[i]

    canvas_id = member["@id"].split("#xywh=")[0]

    if canvas_id not in canvas_map:
        canvas_map[canvas_id] = canvas_data[canvas_id]
        canvas_map[canvas_id]["zones"] = []

    page = int(canvas_id.split("/canvas/p")[1])

    # 新しい頁
    if page != prev_page:
        prev_page = page

        pb = ET.Element(
            "{http://www.tei-c.org/ns/1.0}pb")
        pb.set("n", str(page))
        
        para.append(pb)

    xywh = member["@id"].split("#xywh=")[1].split(",")

    obj = canvas_map[canvas_id]

    width = obj["width"]
    height = obj["height"]

    ulx = int(xywh[0])

    uly = int(xywh[1])

    lrx = ulx + int(xywh[2])
    lry = uly + int(xywh[3])

    zone = ET.Element(
        "{http://www.tei-c.org/ns/1.0}zone")
    zone.set("xml:id", "zone_"+str(i+1).zfill(8))
    zone.set("lrx", str(lrx))
    zone.set("lry", str(lry))
    zone.set("ulx", str(ulx))
    zone.set("uly", str(uly))

    canvas_map[canvas_id]["zones"].append(zone)

    line = ET.Element(
            "{http://www.tei-c.org/ns/1.0}ab")
    line.set("facs", "#zone_"+str(i+1).zfill(8))
    line.text = member["metadata"][0]["value"]
    para.append(line)

for canvas_id in canvas_map:

    obj = canvas_map[canvas_id]

    surface = ET.Element(
                "{http://www.tei-c.org/ns/1.0}surface")
    surfaceGrp.append(surface)

    graphic = ET.Element(
                "{http://www.tei-c.org/ns/1.0}graphic")
    graphic.set("n", canvas_id)
    graphic.set("url", obj["url"])
    surface.append(graphic)

    for zone in obj["zones"]:
        surface.append(zone)


tree.write("test.xml", encoding="utf-8")
