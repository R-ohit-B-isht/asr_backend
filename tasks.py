import time
from celery import Celery
from celery.utils.log import get_task_logger
from flask import Flask ,request,send_from_directory
import os
from werkzeug.utils import secure_filename
import shutil
import subprocess

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

    audio_split="mp3splt -s -p th=-25,min=0.4,rm=50_50,trackjoin=2.5 "+generated_audiofile+" -o @f-@n -d "+folder_for_each_video+"/audio/"+"mp3"
    os.system(audio_split)
    audio_split_text="mp3splt -s -P -p th=-25,min=0.4,rm=50_50,trackjoin=2.5 -o _@m:@s.@h_@M:@S.@H "+generated_audiofile+" > "+folder_for_each_video+"/audio/time_o.txt"
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
    os.system(remover)
    
    return st