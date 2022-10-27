
fil='/workspace/asr_backend/uploads/CS337L4WasL6in2020-tvhzNIK7fG8/CS337_L4_Was_L6_in_2020-tvhzNIK7fG8.mp4'
urler='https://udaaniitb.aicte-india.org:8000/asr/'
import requests

r = requests.post(urler, files = {'file': open(fil, 'rb')},verify=False)
with open('./transcript.xml','w',encoding='utf-8')as t:
  t.write(r.text)