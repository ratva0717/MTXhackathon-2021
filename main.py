from flask import Flask, render_template , request 
from werkzeug.utils import secure_filename
import tensorflow as tf
import os 
import cv2
import math
import numpy as np 
import shutil
import matplotlib.pyplot as plot 

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
img_upload = os.path.join(app.instance_path, 'images')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect',methods=[ "GET",'POST'])
def detect():
    if not request.method == "POST":
        return
    video = request.files['video']
    try:
        os.mkdir("instance")
        os.chdir("instance")
        os.mkdir("uploads")
        os.mkdir("images")
        os.chdir("../")
    except:
        print("Folder already exists")
    print(os.path.join(uploads_dir, secure_filename(video.filename)))
    vid_path = os.path.join(uploads_dir, secure_filename(video.filename))
    video.save(vid_path)
    frame(vid_path)
    return "success"
    
def frame(video):
    videoFile = video
    imagesFolder = img_upload
    cap = cv2.VideoCapture(videoFile)
    frameRate = cap.get(5) #frame rate
    while(cap.isOpened()):
        frameId = cap.get(1) #current frame number
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            print(frameId % math.floor(frameRate))
            filename = imagesFolder + "/image_" +  str(int(frameId)) + ".jpg"
            cv2.imwrite(filename, frame)
            print("written")
    cap.release()
    predict(imagesFolder)
    try:
        os.chdir("instance")
        shutil.rmtree('images', ignore_errors=True)
        os.mkdir("images")
        os.chdir("../")
    except:
        print("Error")
    print ("Done!")

def predict(img_path):
    class_names = ['Non-scoring', 'Scoring']
    conf = []
    classes = []
    frames = []
    img_height = 180 
    img_width = 180
    model = tf.keras.models.load_model("model.h5")
    frame = 1
    for imgs in os.listdir(img_path):
        img = os.path.join(img_path, imgs)
        img = tf.keras.utils.load_img(img, target_size=(img_height, img_width))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        conf.append(100 * np.max(score))
        frames.append(frame)
        classes.append(class_names[np.argmax(score)])
        print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score)))
        frame +=1
    createPlot(conf, frames, classes)

def createPlot(conf, frames, classes):
    color = [] 
    for val in classes:
        if val == "Non-scoring":
            color.append("yellow")
        else:
            color.append("green")
    plot.bar(frames, conf, color = color, width=0.7)
    plot.xlabel("Frames")
    plot.ylabel("Confidence")
    plot.savefig('static/image/plot.png')
if __name__ == "__main__":
    app.run(debug=True)
    
    