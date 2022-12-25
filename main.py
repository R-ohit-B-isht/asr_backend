from flask import Flask ,request,send_from_directory
import os
from werkzeug.utils import secure_filename
import shutil
import subprocess
from celery import Celery

app = Flask(__name__)
# simple_app = Celery('simple_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        filename_without_ext=os.path.splitext(filename)[0]
        # remover="rm ./*.wav"
        # os.system(remover)
        # remover="rm -rf ./uploads/"
        # os.system(remover)
        # check and create upload folder
        isExist = os.path.exists("./uploads")
        if(isExist==False):
            os.makedirs("./uploads")
            
        folder_for_each_video="./uploads/"+filename_without_ext
        folder_for_each_video = folder_for_each_video.replace(' ','')
        folder_for_each_video = folder_for_each_video.replace('_','')
        isExist = os.path.exists(folder_for_each_video)
        if(isExist==False):
            os.makedirs(folder_for_each_video)
        
        file.save(os.path.join(folder_for_each_video+"/", filename))

        
        isExist = os.path.exists(folder_for_each_video+"/audio")
        # if(isExist):
        #     shutil.rmtree(folder_for_each_video+"/audio")
        
        os.makedirs(folder_for_each_video+"/audio")

        generated_audiofile=folder_for_each_video+"/audio/"+filename_without_ext+".mp3"
        convert_to_audio=" ffmpeg -i "+ folder_for_each_video+"/"+filename+" -vn -acodec libmp3lame -ac 1 -ab 160k -ar 16000 "+generated_audiofile
        os.system(convert_to_audio)

        os.makedirs(folder_for_each_video+"/audio/"+"mp3")

        audio_split="mp3splt -s -p th=-35,min=0.4,rm=50_50,trackjoin=2.5 "+generated_audiofile+" -o @f-@n -d "+folder_for_each_video+"/audio/"+"mp3"
        os.system(audio_split)
        audio_split_text="mp3splt -s -P -p th=-35,min=0.4,rm=50_50,trackjoin=2.5 -o _@m:@s.@h_@M:@S.@H "+generated_audiofile+" > "+folder_for_each_video+"/audio/time_o.txt"
        os.system(audio_split_text)
        os.makedirs(folder_for_each_video+"/audio/mp3/waves")
        
        for files in os.listdir(folder_for_each_video+"/audio/mp3/"):
            if files.endswith(".mp3"):
                filenames_without_ext=os.path.splitext(files)[0]
                wav_convert="sox "+folder_for_each_video+"/audio/mp3/"+files+" "+folder_for_each_video+"/audio/mp3/waves/"+filenames_without_ext+".wav"
                os.system(wav_convert)
            else:
                continue
            
        # for files in os.listdir(folder_for_each_video+"/audio/mp3/waves/"):
        #     if files.endswith(".wav"):
        #         copying="cp "+"./uploads/audio/mp3/waves/"+files+" ./"
        #         os.system(copying)
        #     else:
        #         continue
        
        model_script="python3 check.py "+folder_for_each_video
        os.system(model_script)
        xml_script="python3 xml_create.py "+folder_for_each_video
        os.system(xml_script)
       
        
        # with open("./trs.xml", 'r') as fr:
        # # reading line by line
        #     lines = fr.readlines()
        remover="rm -rf "+folder_for_each_video
        os.system(remover)
        return send_from_directory("./", "trs.xml", as_attachment=True)
        
    else:
        return "get"
    
    
if __name__ == '__main__':
    app.run(debug=True,threaded=True)