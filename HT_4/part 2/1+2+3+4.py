import cv2
import numpy as np
import wave
import struct

def equalize_image(path,out):
    img=cv2.imread(path,0)
    eq=cv2.equalizeHist(img)
    cv2.imwrite(out,eq)

def gamma_correction(path,out,gamma):
    img=cv2.imread(path)
    inv=1.0/gamma
    table=np.array([((i/255.0)**inv)*255 for i in range(256)]).astype("uint8")
    res=cv2.LUT(img,table)
    cv2.imwrite(out,res)

def save_histogram_wav(imgpath,outwav):
    img=cv2.imread(imgpath,0)
    hist=cv2.calcHist([img],[0],None,[256],[0,256]).flatten()
    hist=hist/hist.max()
    hist=(hist*32767).astype(np.int16)
    wf=wave.open(outwav,'w')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    for h in hist:
        wf.writeframes(struct.pack('<h',h))
    wf.close()