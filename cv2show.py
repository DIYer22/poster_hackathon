# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 14:22:46 2019

@author: yl
"""
import cv2
from boxx import *
import skimage.data as sda

from boxx import sin, cos
from boxx import Vector, np, timegap, intround
import time

img = sda.astronaut()
imgs = [img]


hw = Vector([800,800])
imgHw = hw
bg = np.zeros(list(imgHw) + [3]).astype(np.uint8)


bgc = 250,85,70
bg[:] = bgc
#bg[:] = 0


from skimage import draw

line = draw.line(0,0,10,10)


def drawXyCycle(img, yx=(200,300),r=8, color=255):
    cir = draw.circle(*yx,r)
    cir = list(cir)
    cir[0] = cir[0].clip(0, img.shape[0]-1)
    cir[1] = cir[1].clip(0, img.shape[1]-1)
#    cir = npa(cir)
    img[cir] = color
    

class FarAwayPoint():
    def __init__(self, du=30, speed=100, r=8,color=255, offset=None):
        self.offset = offset or imgHw/2
        self.b = time.time()
        self.du = du
        self.speed = speed
        self.r = r
        self.color = color
    def __call__(self, img):
        b = self.b
        diff = time.time() - b
        distan = diff * self.speed
        if distan < max(img.shape):
            dy = intround(sin(self.du)*distan)
            dx = intround(cos(self.du)*distan)
            
            drawXyCycle(img, self.offset+(dy,dx), color=self.color, r=self.r)
        
        
        
        pass
        

p1 = FarAwayPoint()

from colors import colors

#colors = (colors*1.5)
colors = np.uint8(colors.clip(0, 255))

duSpeed = -360/20
lineNumber = 10
genGap = .4
lastDu = 0
begin = lastTime = time.time()

points = []

eyeScalecycle = 3
eyeScaleRate = .2

cycR = 5
showeye = True

saveGif = True
saveGif = False
gifs = []

try:
    while True:
        
        key = cv2.waitKey(1)
        
        if key == ord('a'):
            duSpeed -= 2
        if key == ord('d'):
            duSpeed += 2
            
        if key == ord('w'):
            cycR += 1
        if key == ord('s'):
            cycR -= 1
            
        if key == ord('e'):
            showeye = not showeye
        
        tDiff = time.time() - lastTime
        lastTime = time.time()
        timeLong = lastTime - begin
        lastDu += tDiff * duSpeed
        lastDu %= 360
        
        if timegap(genGap, 'gen_points'):
            for ind in range(lineNumber):
                point = FarAwayPoint(lastDu+ind*(360/lineNumber), color=colors[ind], r=cycR)
                points.append(point)
        
        img = bg.copy()
        points = points[-300:]
        for point in points:
            point(img)
        
        
        if showeye:
            from process_img import png 
            
            pngHw = Vector(png.shape[:2])
            
            scale = 1.2 + sin(timeLong*180/eyeScalecycle)*eyeScaleRate
            png = resize(png, map2(intround, pngHw*scale))
            png = uint8(png)
            
            pngHw = Vector(png.shape[:2])
            p0 = imgHw//2 - pngHw//2
            
            mask = (png/255.)[...,None]
            img[p0.h:p0.h+pngHw.h, p0.w:p0.w+pngHw.w] = np.uint8(img[p0.h:p0.h+pngHw.h, p0.w:p0.w+pngHw.w]* (1-mask)+ mask*np.ones(pngHw)[...,None]*255)
        
#        show-img
#        break
        if saveGif:
            sleep(.05)
            img = img[::2,::2]
            gifs.append(img)
            gifs = gifs[-500:]
            
        frame = img[...,[2,1,0]]
        cv2.imshow('now',frame)
        if key==ord('q'):
            break
finally:
    cv2.destroyAllWindows()

if saveGif:
    ylimgVideoAndGif.gifSave(gifs, 'demo.gif')

if 0 :
    cap = cv2.VideoCapture(0)
    while True:
#        frame = randchoice(imgs)[...,[2,1,0]]
        geted, frame = cap.read()
        cv2.imshow('now',frame)
        if cv2.waitKey(1) in [ord('q'), ord(' ')]:
            break
 
    cap.release()
    cv2.destroyAllWindows()




