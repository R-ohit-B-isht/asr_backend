import librosa
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import os
import subprocess
from multiprocessing import Pool, cpu_count
import psutil
import resource
import sys
import whisper
dirs=sys.argv[1]
#load pre-trained model and tokenizer
# processor = Wav2Vec2Processor.from_pretrained("Harveenchadha/vakyansh-wav2vec2-indian-english-enm-700")
# model = Wav2Vec2ForCTC.from_pretrained("Harveenchadha/vakyansh-wav2vec2-indian-english-enm-700")
model = whisper.load_model("base.en")
dir_list = os.listdir(dirs+"/audio/mp3/waves/")
#print(dir_list)
file_name = dirs+"/text.txt"
wfile = open(file_name, 'w', encoding='utf-8')
ts=[]
count = 0
for y in dir_list:
    x=dirs+"/audio/mp3/waves/"+y
    if x.endswith(".wav"):
        count += 1
    else:
        continue
    
    y = model.transcribe(x, language='en', fp16=False)
    # wfile.write(x+"\t"+y+"\n")
    ts.append(x+"\t"+y["text"]+"\n")
    print(psutil.Process().memory_info().rss / (1024 * 1024))
    print(y["text"])
print(count)

ts.sort()
for i in ts:
    wfile.write(i)
