import librosa
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import os
import subprocess
from multiprocessing import Pool, cpu_count
import psutil
import resource
import sys

#load pre-trained model and tokenizer
processor = Wav2Vec2Processor.from_pretrained("Harveenchadha/vakyansh-wav2vec2-indian-english-enm-700")
model = Wav2Vec2ForCTC.from_pretrained("Harveenchadha/vakyansh-wav2vec2-indian-english-enm-700")

dir_list = os.listdir("./")
#print(dir_list)
file_name = "text.txt"
wfile = open(file_name, 'w+', encoding='utf-8')
ts=[]
count = 0
for x in dir_list:
    if x.endswith(".wav"):
        count += 1
    else:
        continue
    speech, rate = librosa.load(x,sr=16000)
    input_values = processor(speech, return_tensors = 'pt').input_values
    #Store logits (non-normalized predictions)
    logits = model(input_values).logits
    #Store predicted id's
    predicted_ids = torch.argmax(logits, dim =-1)
    #decode the audio to generate text
    transcriptions = processor.decode(predicted_ids[0])
    y = transcriptions.replace('<s>','')
    # wfile.write(x+"\t"+y+"\n")
    ts.append(x+"\t"+y+"\n")
    print(psutil.Process().memory_info().rss / (1024 * 1024))
    print(y)
print(count)

ts.sort()
for i in ts:
    wfile.write(i)