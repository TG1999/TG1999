import fitz
import os
from matplotlib import pyplot as plt
import cv2
import math
import numpy as np
def extract_image(file):
    doc = fitz.open(file)
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:  # this is GRAY or RGB
                try:
                    pix.writePNG("./pdf/p%s-%s.png" % (i, xref))
                except:
                    try :
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        pix1.writePNG("./pdf/p%s-%s.png" % (i, xref))
                        pix1 = None
                    except:
                        print('sorry again')
            else:  # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("./pdf/p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None

file = 'Baeg et al. - 2013 - Organic light detectors photodiodes and phototransistors.pdf'
# extract_image(file)
i=0
for (rootpdf,dirspdf,filespdf) in os.walk('./master1'):
    for filepdf in filespdf:
        orb = cv2.ORB_create()
        print(rootpdf+'/'+filepdf)
        img =cv2.imread(rootpdf+'/'+filepdf)
        max_val = 0
        (kp1, des1) = orb.detectAndCompute(img, None)
        for (root,dirs,files) in os.walk('./pdf'):
            for file in files:
                file = root+'/'+file
                print(file)
                train_img = cv2.imread(file)
                (kp2, des2) = orb.detectAndCompute(train_img, None)
                bf = cv2.BFMatcher()
                all_matches = bf.knnMatch(des1, des2, k=2)
                good = []
                for (m, n) in all_matches:
                    if m.distance < 0.789 * n.distance:
                        good.append([m])
                print(len(good))
                if len(good) > max_val:
                    max_val = len(good)
                    image = train_img
                    file_found = file
        print(image,file_found)
        cv2.imwrite('./found/'+str(i)+'.png',image)
        i = i+1
