from flask import Flask ,request,send_from_directory
import os
from werkzeug.utils import secure_filename
import shutil
import subprocess
from flask import Flask
from celery import Celery

app = Flask(__name__)
simple_app = Celery('simple_worker', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.route('/transcript',methods=["POST","GET"])
def call_method():
    app.logger.info("Invoking Method ")

    if request.method=="POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        filename_without_ext=os.path.splitext(filename)[0]
        
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
        r = simple_app.send_task('tasks.longtime_add', kwargs={'folder_for_each_video':folder_for_each_video,'filename_without_ext':filename_without_ext,'filename':filename})
        app.logger.info(r.backend)
        return r.id
    else:
        return "get"


@app.route('/transcript/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return str(status.state)


@app.route('/transcript/<task_id>/result')
def task_result(task_id):
    result = simple_app.AsyncResult(task_id).result
    return  str(result)

########################################################################################




@app.route('/translation',methods=["POST","GET"])
def call_method():
    app.logger.info("Invoking Method ")

    if request.method=="POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        filename_without_ext=os.path.splitext(filename)[0]
        
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
        r = simple_app.send_task('tasks.getTranslation', kwargs={'folder_for_each_video':folder_for_each_video,'filename':filename})
        app.logger.info(r.backend)
        return r.id
    else:
        return "get"


@app.route('/translation/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return str(status.state)


@app.route('/translation/<task_id>/result')
def task_result(task_id):
    result = simple_app.AsyncResult(task_id).result
    return  str(result)

