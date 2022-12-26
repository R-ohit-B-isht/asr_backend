import statistics 
from statistics import mode
import sys
import os
dirs=sys.argv[1]
from resemblyzer import preprocess_wav, VoiceEncoder
from pathlib import Path

#give the file path to your audio file

audio_file_path = ''
for filename in os.listdir(dirs+'/audio'):
    if filename.endswith(".wav"):
        audio_file_path=dirs+'/audio/'+filename

wav_fpath = Path(audio_file_path)

wav = preprocess_wav(wav_fpath)
encoder = VoiceEncoder("cpu")
_, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)
print(cont_embeds.shape)

from spectralcluster import SpectralClusterer

clusterer = SpectralClusterer(
    min_clusters=1,
    max_clusters=100,
    # p_percentile=0.90,
    # gaussian_blur_sigma=1
    )

labels = clusterer.predict(cont_embeds)


def create_labelling(labels,wav_splits):
    from resemblyzer import sampling_rate
    times = [((s.start + s.stop) / 2) / sampling_rate for s in wav_splits]
    labelling = []
    start_time = 0

    for i,time in enumerate(times):
        if i>0 and labels[i]!=labels[i-1]:
            temp = [str(labels[i-1]),start_time,time]
            labelling.append(tuple(temp))
            start_time = time
        if i==len(times)-1:
            temp = [str(labels[i]),start_time,time]
            labelling.append(tuple(temp))

    return labelling
  
labelling = create_labelling(labels,wav_splits)

def get_sec(time_str):
    """Get seconds from time."""
    m, s = time_str.split(':')
    return float(m) * 60 + float(s)

with open(dirs+'/audio/time_o.txt', 'r') as fr:
    # reading line by line
    lines = fr.readlines()
    lines = lines[:-1] 
    # pointer for position
    ptr = 1
  
    # opening in writing mode
    with open(dirs+'/time.txt', 'w') as fw:
        for line in lines:
            # y = line.replace('created','')
            y = line.replace('.mp3','_')
            # we want to remove 5th line
            if ptr not in [1,2,3,4,5,6,7,8,9]:
                fw.write(y)
            ptr += 1

file_name = dirs+'/time.txt'
# count=0
time_list = []
full_time_list=[]
with open(file_name, 'r', encoding='utf-8',  errors='ignore') as f:
    for line in f:
        # if count==0:
            # count=1
            # continue
        time = line.split("\n")[0].split("_")[2]
        st=get_sec(line.split("\n")[0].split("_")[1])
        ed=get_sec(line.split("\n")[0].split("_")[2])
        speakers=[]
        for sp in labelling:
            if sp[2]<st :
                continue
                
            if sp[1]>ed:
                continue
            else:
                speakers.append(sp[0])
        if len(speakers)>0:
            full_time_list.append(mode(speakers))
        else:
            full_time_list.append(0)
        # time = time.replace('created" ','')
        time_list.append(time)
print(len(full_time_list))

file_name = dirs+"/text.txt"
sentence_list = []
with open(file_name, 'r', encoding='utf-8',  errors='ignore') as f:
    for line in f:
        word = line.split("\t")[1].split("\n")[0]
        sentence_list.append(word)
# print(len(sentence_list))

file_name = dirs+"/transcript.xml"
wfile = open(file_name, 'w+', encoding='utf-8')
i = 0

wfile.write('<?xml version="1.0" encoding="UTF-8"?>'+"\n")
wfile.write('<transcript lang="english">'+"\n")
for j in range(len(sentence_list)):
    sentence = sentence_list[j].lstrip()
    time = time_list[j]
    whoS="Speaker_"+str(full_time_list[j])
    wfile.write("<line timestamp=\""+str(time)+"\" speaker=\""+whoS+"\">"+"\n")
    word = sentence.split(" ")
    for k in range(len(word)):
        wfile.write("<word timestamp=\"\" is_valid=\"1\">"+str(word[k])+"</word>"+"\n")
    wfile.write("</line>"+"\n")
wfile.write('</transcript>')
