from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
import json
from tensorflow import Graph, Session

img_height,img_width=224,224
with open('./models/imagenet_classes.json','r') as f:
    labelInfo=f.read()

labelInfo=json.loads(labelInfo) 

model_graph= Graph()
with model_graph.as_default():
    tf_session= Session()
    with tf_session.as_default():
        model=load_model('./models/mobilenet.h5')



# Create your views here.
def index(request):
    context={'a':1}
    return render(request,'index1.html',context)


def classifier(request):
    fileObj=request.FILES['fileP']
    fs=FileSystemStorage()
    path=fs.save(fileObj.name,fileObj)
    path=fs.url(path)
    testimage='.'+path

    img=image.load_img(testimage,target_size=(img_height,img_width))
    x=image.img_to_array(img)
    x=x/255 
    x=x.reshape(1,img_height,img_width,3)

    with model_graph.as_default():
        with tf_session.as_default():
            pred=model.predict(x)


    import numpy as np
    prediction=labelInfo[str(np.argmax(pred[0]))]



    

    context={'path':path,
    'prediction':prediction[1],
    }
    return render(request,'index.html',context)

def viewhistory(request):
    import os
    History=os.listdir('./media/')
    historypath=['./media/'+i for i in History]
    context={
        'historypath':historypath
    }

    return render(request,'history.html',context)
    
