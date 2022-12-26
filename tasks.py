import time
from celery import Celery
from celery.utils.log import get_task_logger
from flask import Flask ,request,send_from_directory
import os
from werkzeug.utils import secure_filename
import shutil
import subprocess
import re
import requests
import sys          
import xml.etree.ElementTree as ET

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.task()
def longtime_add(folder_for_each_video,filename_without_ext,filename):
    isExist = os.path.exists(folder_for_each_video+"/audio")


    os.makedirs(folder_for_each_video+"/audio")

    generated_audiofile=folder_for_each_video+"/audio/"+filename_without_ext+".mp3"
    convert_to_audio=" ffmpeg -i "+ folder_for_each_video+"/"+filename+" -vn -acodec libmp3lame -ac 1 -ab 160k -ar 16000 "+generated_audiofile
    os.system(convert_to_audio)

    os.makedirs(folder_for_each_video+"/audio/"+"mp3")

    audio_split_text="mp3splt -s -P -p th=-10,min=0.4,rm=50_50,trackjoin=2.5 -o _@m:@s.@h_@M:@S.@H "+generated_audiofile+" > "+folder_for_each_video+"/audio/time_o.txt"
    os.system(audio_split_text)
    
    with open(folder_for_each_video+"/audio/time_o.txt",'r')as slice:
        lines=slice.readlines()
        ts=lines[-1]

    lvl=re.findall("\d+\.\d+", ts)
    print("\n\n\n\n\n\n\nsilence lvl is : "+lvl[0])
    print("\n\n\n\n\n\n\n")
    
    if lvl[0]!=10:
        audio_split="mp3splt -s -p th=-"+lvl[0]+",min=0.4,rm=50_50,trackjoin=2.5 "+generated_audiofile+" -o @f-@n -d "+folder_for_each_video+"/audio/"+"mp3"
        os.system(audio_split)
        audio_split_text="mp3splt -s -P -p th=-"+lvl[0]+",min=0.4,rm=50_50,trackjoin=2.5 -o _@m:@s.@h_@M:@S.@H "+generated_audiofile+" > "+folder_for_each_video+"/audio/time_o.txt"
        os.system(audio_split_text)
    else:
        audio_split="mp3splt -s -p th=-10"+",min=0.4,rm=50_50,trackjoin=2.5 "+generated_audiofile+" -o @f-@n -d "+folder_for_each_video+"/audio/"+"mp3"
        os.system(audio_split)
        audio_split_text="mp3splt -s -P -p th=-10"+",min=0.4,rm=50_50,trackjoin=2.5 -o _@m:@s.@h_@M:@S.@H "+generated_audiofile+" > "+folder_for_each_video+"/audio/time_o.txt"
        os.system(audio_split_text)
    
    os.makedirs(folder_for_each_video+"/audio/mp3/waves")

    for files in os.listdir(folder_for_each_video+"/audio/mp3/"):
        if files.endswith(".mp3"):
            filenames_without_ext=os.path.splitext(files)[0]
            wav_convert="sox "+folder_for_each_video+"/audio/mp3/"+files+" "+folder_for_each_video+"/audio/mp3/waves/"+filenames_without_ext+".wav"
            os.system(wav_convert)
        else:
            continue


    model_script="python3 check.py "+folder_for_each_video
    os.system(model_script)
    xml_script="python3 xml_create.py "+folder_for_each_video
    os.system(xml_script)


    
    st=""
    with open(folder_for_each_video+"/transcript.xml",'r')as sendt:
        st=sendt.read()
    remover="rm -rf "+folder_for_each_video
    # os.system(remover)
    
    return st



##########################################################################

def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
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
        with open (tXML,"r",encoding='utf-8') as wr:
            re1 = re.readline()
            wr1 = wr.readline()
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
                wr1 = wr.readline()
    return fu

@app.task()
def getTranslation(folder_for_each_video,filename,source_lang,destination_lang):
    print(source_lang)
    print(destination_lang)
    sr='en'
    dt='hi'
    
    ##source lang
    if source_lang=="hindi":
        sr='hi'
    elif source_lang=='english':
        sr='en'
     
    ##destination lang   
    if destination_lang=="hindi":
        dt='hi'
    elif destination_lang=='english':
        dt='en'
        
        
    final_translation=[]
    for line in parseXML(folder_for_each_video+"/"+filename):
        payload = {"sentence": line}
        req = requests.post('https://udaaniitb2.aicte-india.org:8000/udaan_project_layout/translate/'+sr+'/'+dt.format("math,phy", "1"), data = payload, verify=False)
        final_translation.append(req.json()['translation'])
        
    tXML='<?xml version="1.0" encoding="UTF-8"?>\n'+'<transcript lang="'+destination_lang+'">\n'

    for line in final_translation:
        tXML+='<line timestamp="" speaker="Speaker_1">\n'
        for word in line.split():
            tXML+=('<word timestamp="">')
            tXML+=(word)
            tXML+=('</word>\n')
        tXML+=('</line>\n')
    tXML+=('</transcript>\n')
    with open(folder_for_each_video+"/"+destination_lang+'.xml','w',encoding='utf-8')as tr:
        tr.write(tXML)
    tXML=compareXMLforTimeStamps(folder_for_each_video+"/"+filename,folder_for_each_video+"/"+destination_lang+'.xml')
    remover="rm -rf "+folder_for_each_video
    os.system(remover)
    return tXML