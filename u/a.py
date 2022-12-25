import os

for files in os.listdir("./mp3/"):
            if files.endswith(".mp3"):
                filenames_without_ext=os.path.splitext(files)[0]
                wav_convert="sox "+"./mp3/"+files+" "+"./mp3/waves/"+filenames_without_ext+".wav"
                os.system(wav_convert)
            else:
                continue