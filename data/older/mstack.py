import sys,subprocess,cv2,numpy as np
# args: session:n,n session:n,...
ims=[]
for a in sys.argv[1:]:
    s,ns=a.split(':');ns=ns.split(',')
    subprocess.run(['python3','crop.py',s]+ns,capture_output=True)
    for n in ns:
        i=cv2.imread(f'png/crop-{s}-{n}.png',0)
        if i is None: continue
        c=np.where((i<128).sum(0)>0)[0]; i=i[:, :c.max()+20] if len(c) else i
        cv2.putText(i,s[2:],(i.shape[1]-200,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,0,2)
        ims.append(i)
W=max(i.shape[1] for i in ims)
ims=[cv2.copyMakeBorder(i,0,4,0,W-i.shape[1],cv2.BORDER_CONSTANT,value=128) for i in ims]
st=np.vstack(ims);cols=np.where((st<128).sum(0)>0)[0];st=st[:,:min(st.shape[1],cols.max()+20)]
cv2.imwrite('png/stack.png',st);print(st.shape)
