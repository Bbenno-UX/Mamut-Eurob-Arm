import time
from threading import Thread
from serial import Serial
import numpy as np
import cv2 as cv
from sympy import Point, Polygon
from numpy.linalg import norm
from picamera import PiCamera
from picamera.array import PiRGBArray
import smbus
#from I2C_LCD import lcddriver
import os
import numpy as np
#Punkte im Raum aus sicht von Arm und Kamera,muss für den Eurobot angepasst werden
punkte_rpi=[[317,127],[286,90],[184,66],[181,128],[103,108],[94,145],[168,188],[234,177]]
punkte_arm=[[1250,1400],[1250,1650],[1350,1950],[1800,1350],[1600,1950],[1900,1600],[2050,1100],[1900,1000]]

class dreieck():
    def __init__(self,pol1,pol2):
        
        self.pol1=Polygon(pol1[0],pol1[1],pol1[2])
        self.pol2=Polygon(pol2[0],pol2[1],pol2[2])
        pol1=np.array(pol1)
        #pol2=np.array(pol2)
        inds=[[1,2],[2,0],[0,1]]
        #zählt zum Interpolationsversuch hier
        self.ander=np.argmax(np.linalg.norm(np.array([pol1[1]-pol1[2],pol1[2]-pol1[0],pol1[0]-pol1[1]]),axis=1))
        self.groesste_linie=inds[self.ander]
lisde=[[0,1,3],[0,7,3],[2,3,4],[4,3,5],[6,5,3],[1,2,3]]
Dreiecke=[]
for i in lisde:
    Dreiecke.append(dreieck([punkte_rpi[i[0]],punkte_rpi[i[1]],punkte_rpi[i[2]]],[punkte_arm[i[0]],punkte_arm[i[1]],punkte_arm[i[2]]]))
def dieprozedur(ptest):
    ptest=np.array(ptest)
    for i in Dreiecke:
        #Versuch der Interpolation der Position eines ArUcO Codes, 
        #ggf. eine vorgeschriebene Bibliothek verwenden
        if i.pol1.encloses_point(Point(*ptest)):
            p1=i.pol1.vertices[i.groesste_linie[0]]

            p1=np.asarray(i.pol1.vertices[0],dtype=int)
            p2=np.asarray(i.pol1.vertices[1],dtype=int)
            p3=np.asarray(i.pol1.vertices[2],dtype=int)
            d=norm(np.array([p1-ptest,p2-ptest,p3-ptest]),axis=1)
            werte=[0,0,0]
            werte[0]=max([0,1-d[0]/min([norm(p2-p1),norm(p3-p1)])])
            werte[1]=max([0,1-d[1]/min([norm(p2-p1),norm(p2-p3)])])
            werte[2]=max([0,1-d[2]/min([norm(p3-p1),norm(p3-p2)])])
            werte=[i*1/sum(werte) for i in werte]
            #werte=np.array(max([0,1-d[0]/min()]),max([0,1-d[1]/min()]),max([0,1-d[2]/min()]))

            q1=np.array(i.pol2.vertices[i.groesste_linie[0]],dtype=int)
            q2=np.array(i.pol2.vertices[i.groesste_linie[1]],dtype=int)
            q3=np.array(i.pol2.vertices[i.ander],dtype=int)
            # finalx=q1[0]+(q2[0]-q1[0])*abs(ptest[0]/p2[0])+(q3[0]-q1[0])*abs(ptest[1]/p3[1])
            # finaly=q1[1]+(q2[1]-q1[1])*abs(ptest[0]/p2[0])+(q3[1]-q1[1])*abs(ptest[1]/p3[1])
            finale=q1*werte[0]+q2*werte[1]+q3*werte[2]
            #finale=[finalx,finaly]
            return finale
    return[0,0]
# lcd start
#lcd = lcddriver.lcd()

# this command clears the display (captain obvious)
#lcd.lcd_clear()

# now we can display some characters (text, line)
bef=0
magn=0

#s=Serial('/dev/ttyACM0',baudrate=9600)
t=time.time()
#t1=Thread(target=Seral)
#t1.start()
print("meddl")
camera = PiCamera()
camera.framerate=10
camera.resolution = (400, 300)
print("11")
rawCapture = PiRGBArray(camera,size=(400,300))
print("2")
# allow the camera to warmup
time.sleep(0.1)
t=0
t1=0



u=np.array([[110,294],[342,131],[342,382],[231,382]])
l=[3543,245]
s=Serial("/dev/ttyACM0",baudrate=9600)
def warter():
    while True:
        #Funktion für IO, Soll bei aktiviertung den Arm zum Code fahren,
        #Schrittmotor herunter, Schrittmotor hoch und zurück, bei jedem Schritt
        #auf Antwort des Arduinos warten, Momentan probleme damit, 
        #Weil pi bislang einfach weiter macht.
        k=input()
        st="0,%d,%d\n"%(l[0],l[1])
        s.write(st.encode('utf-8'))
        s.read(s.inWaiting())
        st="-100,%d,%d\n"%(l[0],l[1])
        s.write(st.encode('utf-8'))
        s.read(s.inWaiting())
        st="100,%d,%d\n"%(l[0],l[1])
        s.write(st.encode('utf-8'))
        s.read(s.inWaiting())
        st="0,1900,1600"
        s.write(st.encode('utf-8'))
        
        l[0]+=1
k=Thread(target=warter)
k.start()
# while True:
#     print("Ecken",u)
#     u+=1
#     print("Vorgeschlagen:%d,%d Drücke [ENTER] zum ausführen"%(l[0],l[1]))
#     l=[randint(1000,1500),randint(1000,1500)]
#     time.sleep(0.5)
#     os.system('clear')










dicter=cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_100) 
print("HIER")
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #for-loop für die Kamera
    image = frame.array

    key = cv.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    imag=image.copy()
    arucoParams = cv.aruco.DetectorParameters_create()
    corners,ids,rejected=cv.aruco.detectMarkers(imag, dicter,parameters=arucoParams)
    its=np.array(ids)
    #print("ja")
    if its.size==0:
        print("NEIN")
        pass
    else:
        if corners:
            corner=np.array(corners)[0][0]
            frams=int(1/(time.time()-t))
            t=time.time()
            if time.time()-t1>2:
                t1=time.time()
                #lcd.lcd_clear()
                #lcd.lcd_display_string(str(corner[0].astype(int))+str(corner[1].astype(int)), 1)
                #lcd.lcd_display_string(str(corner[2].astype(int))+str(corner[3].astype(int)), 2)
                #lcd.lcd_display_string("Frames: %i" %(frams), 3)
            #print(corner)
            x=np.mean(corner[:,0])
            y=np.mean(corner[:,1])
            
            stat=dieprozedur([x,y])
            l=stat
            os.system('clear')
            print("Ecken:",corner)
            if stat[0]==None:
                l=[0,0]
            print("Punkte:",x,y)
            print("Vorgeschlagen:%d,%d Drücke [ENTER] zum ausführen"%(stat[0],stat[1]))
            print("Vorgeschlagen:",stat)

            else:
                bef=4
        else:
            bef=4
        #corners,ids,rejected=cv.aruco.detectMarkers(img, dicter,parameters=arucoParams)
        #cv.imshow("Fram",img)
k.join()
