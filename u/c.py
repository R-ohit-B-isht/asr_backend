#file_name = "malhar_time.txt"
import sys
# dirs=sys.argv[1]
with open('./t.txt', 'r') as fr:
    # reading line by line
    lines = fr.readlines()
    lines = lines[:-1] 
    # pointer for position
    ptr = 1
  
    # opening in writing mode
    with open('./time.txt', 'w') as fw:
        for line in lines:
            # y = line.replace('created','')
            y = line.replace('.mp3','_')
            # we want to remove 5th line
            if ptr not in [1,2,3,4,5,6,7,8,9]:
                fw.write(y)
            ptr += 1

file_name = './time.txt'
# count=0
time_list = []
with open(file_name, 'r', encoding='utf-8',  errors='ignore') as f:
    for line in f:
        # if count==0:
            # count=1
            # continue
        time = line.split("\n")[0].split("_")[2]
        # time = time.replace('created" ','')
        time_list.append(time)
print(len(time_list))

file_name = "./text.txt"
sentence_list = []
with open(file_name, 'r', encoding='utf-8',  errors='ignore') as f:
    for line in f:
        word = line.split("\t")[1].split("\n")[0]
        sentence_list.append(word)
print(len(sentence_list))

file_name = "./transcript.xml"
wfile = open(file_name, 'w+', encoding='utf-8')
i = 0

wfile.write('<?xml version="1.0" encoding="UTF-8"?>'+"\n")
wfile.write('<transcript lang="english">'+"\n")
for j in range(len(sentence_list)):
	sentence = sentence_list[j]
	time = time_list[j]
	wfile.write("<line timestamp=\""+str(time)+"\" speaker=\"Speaker_1\">"+"\n")
	word = sentence.split(" ")
	for k in range(len(word)):
		wfile.write("<word timestamp=\"\" is_valid=\"1\">"+str(word[k])+"</word>"+"\n")
	wfile.write("</line>"+"\n")
wfile.write('</transcript>')
