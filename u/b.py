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
import soundfile as sf
# dirs=sys.argv[1]
#load pre-trained model and tokenizer
# processor = Wav2Vec2Processor.from_pretrained("Harveenchadha/vakyansh-wav2vec2-indian-english-enm-700")
# model = Wav2Vec2ForCTC.from_pretrained("Harveenchadha/vakyansh-wav2vec2-indian-english-enm-700")
processor = Wav2Vec2Processor.from_pretrained("Harveenchadha/vakyansh-wav2vec2-hindi-him-4200")
model = Wav2Vec2ForCTC.from_pretrained("Harveenchadha/vakyansh-wav2vec2-hindi-him-4200")
# model = whisper.load_model("large")
dir_list = os.listdir("./mp3/waves/")
#print(dir_list)
file_name = "./text.txt"
wfile = open(file_name, 'w', encoding='utf-8')
ts=[]
count = 0
for y in dir_list:
    x="./mp3/waves/"+y
    if x.endswith(".wav"):
        count += 1
    else:
        continue
    audio_input, sample_rate = sf.read(x)
    input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    
    y = processor.decode(predicted_ids[0], skip_special_tokens=True)
    
    # wfile.write(x+"\t"+y+"\n")
    ts.append(x+"\t"+y+"\n")
    # print(psutil.Process().memory_info().rss / (1024 * 1024))
    print(y)
print(count)

ts.sort()
for i in ts:
    wfile.write(i)

# import soundfile as sf
# import torch
# from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
# import argparse

# def parse_transcription(wav_file):
#     # load pretrained model
#     processor = Wav2Vec2Processor.from_pretrained("Harveenchadha/vakyansh-wav2vec2-hindi-him-4200")
#     model = Wav2Vec2ForCTC.from_pretrained("Harveenchadha/vakyansh-wav2vec2-hindi-him-4200")

    # load audio
    # audio_input, sample_rate = sf.read(wav_file)

    # # pad input values and return pt tensor
    # input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

    # # INFERENCE
    # # retrieve logits & take argmax
    # logits = model(input_values).logits
    # predicted_ids = torch.argmax(logits, dim=-1)

    # # transcribe
    # transcription = processor.decode(predicted_ids[0], skip_special_tokens=True)
    # print(transcription)
