import sys
import requests
import xml.etree.ElementTree as ET

def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    print(tree)
    root = tree.getroot()
    print(root)
    lines = []
    for item in root.findall('line'):
        words=[]
        news = {}
        line=""
        for child in item.findall('word'):
              if child.text is not None:
                line +=child.text+" "
        lines.append(line)
    return lines

def compareXMLforTimeStamps(xmlfile,tXML):
    count=[]
    cn1=0
    cn2=0
    fu=""
    with open (xmlfile,"r",encoding='utf-8') as re:
            re1 = re.readline()
            wr1 = tXML.readline()
            while re1 !="":
                if "line timestamp" in re1:
                    cn1+=1
                    count.append(re1)
                re1 = re.readline()

            while  wr1 != "":
                if "line timestamp" in wr1:
                    cn2+=1
                    wr1=count[cn2-1]
                fu+=wr1
                wr1 = tXML.readline()
    return fu

def getTranslation():
    final_translation=[]
    for line in parseXML('./transcript.xml'):
        payload = {"sentence": line}
        req = requests.post('https://udaaniitb2.aicte-india.org:8000/udaan_project_layout/translate/en/hi'.format("math,phy", "1"), data = payload, verify=False)
        final_translation.append(req.json()['translation'])
        
    tXML='<?xml version="1.0" encoding="UTF-8"?>\n'+'<transcript lang="hindi">\n'

    for line in final_translation:
        tXML+='<line timestamp="" speaker="Speaker_1">\n'
        for word in line.split():
            tXML+=('<word timestamp="">')
            tXML+=(word)
            tXML+=('</word>\n')
        tXML+=('</line>\n')
    tXML+=('</transcript>\n')
    tXML=compareXMLforTimeStamps('./transcript.xml',tXML)
    return tXML