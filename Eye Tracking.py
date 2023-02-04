import cv2
import threading
import numpy
import pyautogui
import keyboard
import math
import speech_recognition
def move(x,y):
    pyautogui.moveTo(x = x , y = y)
def speech():
    r=speech_recognition.Recognizer()
    while 1:
        with speech_recognition.Microphone() as source:
            print("Speak")
            audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
            print(text)
            if text=="click":
                pyautogui.click()
        except:
            print("error")
def screen_edges():
    global x1,y1,x2,y2,x3,y3
    screen=cv2.VideoCapture(2)
    screen.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    screen.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while 1:
        ret,frame=screen.read()
        frame=cv2.flip(frame,1)
        frame=cv2.flip(frame,0)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        _, threshold = cv2.threshold(gray,120, 255, cv2.THRESH_BINARY)
        contours ,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        if len(contours)>0:
            cv2.drawContours(frame, [contours[0]], -1, (0, 0, 255), 2)
            x1,y1=10000,10000
            x2,y2=10000,10000
            x3,y3=10000,10000
            for point in contours[0]:
                if point[0][0]+point[0][1]<x1+y1:
                    x1,y1=point[0][0],point[0][1]
                if 1280-point[0][0]+point[0][1]<1280-x2+y2:
                    x2,y2=point[0][0],point[0][1]
                if point[0][0]+720-point[0][1]<x3+720-y3:
                    x3,y3=point[0][0],point[0][1]
            cv2.circle(frame,(x1,y1),8,(0,255,0),3)
            cv2.circle(frame,(x2,y2),8,(0,255,0),3)
            cv2.circle(frame,(x3,y3),8,(0,255,0),3)
        cv2.imshow('screen',frame)
        key=cv2.waitKey(1)
        if key==27:
            break
    cv2.destroyAllWindows()
eye=cv2.VideoCapture(1)
eye.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
eye.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
x1,y1,x2,y2,x3,y3=1,1,1,1,1,1
xx1,yy1,xx2,yy2,xx3,yy3=1,1,1,1,1,1
xz,yz,zx,zy=0,0,0,0
xa,ya,xb,yb=10,10,10,10
screen_edge=threading.Thread(target=screen_edges)
screen_edge.start()
voice=threading.Thread(target=speech)
voice.start()
while 1:
    ret,frame=eye.read()
    frame=frame[300:500,950:1200]
    frame=cv2.flip(frame,1)
    rot=cv2.getRotationMatrix2D((125,100),50,1)
    frame=cv2.warpAffine(frame,rot,(250,250),borderValue=(255,255,255))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (1, 1), 0)
    _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    contours ,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    if len(contours)>0:
        cv2.drawContours(frame, [contours[0]], -1, (0, 0, 255), 2)
        (x,y,w,h)=cv2.boundingRect(contours[0])
        x=x+w//2
        y=y+h//2
        if keyboard.is_pressed('w'):
            xz=x
            yz=y
            zx=x1
            zy=y1
        cv2.circle(frame,(x,y),8,(255,255,255),3)
        xx1=xz+(zx//10)-(x1//10)
        yy1=yz+(zy//10)-(y1//10)
        xx2=xx1+(x2//10)-(x1//10)
        yy2=yy1+(y2//10)-(y1//10)
        xx3=xx1+(x3//10)-(x1//10)
        yy3=yy1+(y3//12)-(y1//12)
        cv2.circle(frame,(xx1,yy1),8,(255,0,0),3)
        cv2.circle(frame,(xx2,yy2),8,(0,255,0),3)
        cv2.circle(frame,(xx3,yy3),8,(0,0,255),3)
        if(xx2-xx1>0):
            x=(x-xx1)*1920//(xx2-xx1)
        if(yy3-yy1>0):
            y=(y-yy1)*1080//(yy3-yy1)
        if(x<10):
            x=10
        if(x>1910):
            x=1910
        if(y<10):
            y=10
        if(y>1070):
            y=1070
        if(xb>x-10 and xb<x+10)and(yb>y-10 and yb<y+10):
            xa=xb
            ya=yb
            x=xb
            y=yb
        t=threading.Thread(target=move,args=(xb,yb))
        t.start()
        xb=xa
        yb=ya
        xa=x
        ya=y
    cv2.imshow('frame',frame)
    key=cv2.waitKey(1)
    if key==27:
        break
cv2.destroyAllWindows()
