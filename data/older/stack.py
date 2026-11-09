import sys,subprocess,cv2,numpy as np
s=sys.argv[1];ns=sys.argv[2:]
subprocess.run(['python3','crop.py',s]+ns,capture_output=True)
ims=[cv2.imread(f'png/crop-{s}-{n}.png',0) for n in ns]
ims=[i for i in ims if i is not None]
W=max(i.shape[1] for i in ims)
ims=[cv2.copyMakeBorder(i,0,4,0,W-i.shape[1],cv2.BORDER_CONSTANT,value=128) for i in ims]
st=np.vstack(ims)
# 2018-04-12 landscape: trim right blank
cols=np.where((st<128).sum(0)>0)[0]
st=st[:, :min(st.shape[1],cols.max()+20)] if len(cols) else st
cv2.imwrite('png/stack.png',st);print(st.shape)
