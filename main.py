from flask import Flask ,request,send_from_directory
import os
from werkzeug.utils import secure_filename
import shutil
import subprocess

app = Flask(__name__)


@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":
        file = request.files['file']
        filename = secure_filename(file.filename)

        # check and create upload folder
        isExist = os.path.exists("./uploads")
        if(isExist==False):
            os.makedirs("./uploads")
        
        file.save(os.path.join("./uploads", filename))

        filename_without_ext=os.path.splitext(filename)[0]
        isExist = os.path.exists("./uploads/audio")
        if(isExist):
            shutil.rmtree("./uploads/audio")
        
        os.makedirs("./uploads/audio")

        generated_audiofile="./uploads/audio/"+filename_without_ext+".mp3"
        convert_to_audio=" ffmpeg -i ./uploads/" +filename+" -vn -acodec libmp3lame -ac 1 -ab 160k -ar 16000 "+generated_audiofile
        os.system(convert_to_audio)

        os.makedirs("./uploads/audio/mp3")

        audio_split="mp3splt -s -p th=-40,min=0.4,rm=50_50,trackjoin=2.5 "+generated_audiofile+" -o @f-@n -d "+"./uploads/audio/mp3"
        os.system(audio_split)
        audio_split_text="mp3splt -s -P -p th=-40,min=0.4,rm=50_50,trackjoin=2.5 -o _@m:@s.@h_@M:@S.@H "+generated_audiofile+" > "+"./uploads/audio/time_o.txt"
        os.system(audio_split_text)
        os.makedirs("./uploads/audio/mp3/waves")
        
        for files in os.listdir("./uploads/audio/mp3/"):
            if files.endswith(".mp3"):
                filenames_without_ext=os.path.splitext(files)[0]
                wav_convert="sox "+"./uploads/audio/mp3/"+files+" ./uploads/audio/mp3/waves/"+filenames_without_ext+".wav"
                os.system(wav_convert)
            else:
                continue
        for files in os.listdir("./uploads/audio/mp3/waves/"):
            if files.endswith(".wav"):
                copying="cp "+"./uploads/audio/mp3/waves/"+files+" ./"
                os.system(copying)
            else:
                continue
        model_script="python3 check.py"
        os.system(model_script)
        xml_script="python3 xml_create.py"
        os.system(xml_script)
        remover="rm ./*.wav"
        os.system(remover)
        remover="rm -rf ./uploads/"
        os.system(remover)
        return send_from_directory("./", "G_2.xml", as_attachment=True)
    else:
        return "get"
    
    
if __name__ == "__main__":
    app.run(debug=true,host='127.0.0.1', port=80)
