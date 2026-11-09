import cv2,numpy as np,sys,os
f=sys.argv[1];g=cv2.imread(f,0)
b=cv2.adaptiveThreshold(g,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,41,18)
hz=cv2.morphologyEx(b,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_RECT,(120,1)))
hz=cv2.dilate(hz,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
out=g.copy();out[hz>0]=255
H,W=out.shape
# whiten left/right margins (scanner noise)
if W<H: out[:, :int(W*0.045)]=255; out[:, int(W*0.975):]=255
cv2.imwrite('clean/'+os.path.basename(f),out)
