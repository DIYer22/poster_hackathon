# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 17:04:22 2019

@author: yl
"""
from boxx import *

img = imread('fromx.jpg')

img = img[75:320]

png = (255-img).max(-1)


png[png>100]=255

png = 255-png


#show -img
if __name__ == "__main__":
    show-png
    show - np.append(img,png[...,None], -1)
    
    pass
    
    
