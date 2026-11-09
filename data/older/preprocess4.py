import cv2,numpy as np,sys,os
f=sys.argv[1];g=cv2.imread(f,0)
g=cv2.GaussianBlur(g,(3,3),0)
_,b=cv2.threshold(g,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
hz=cv2.morphologyEx(b,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_RECT,(160,1)))
hz=cv2.dilate(hz,cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)))
out=255-b;out[hz>0]=255
H,W=out.shape
if W<H: out[:, :int(W*0.045)]=255; out[:, int(W*0.975):]=255
cv2.imwrite('clean4/'+os.path.basename(f),out)
