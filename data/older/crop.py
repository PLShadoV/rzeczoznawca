# usage: crop.py session qnum [qnum...] -> writes png/crop-<s>-<n>.png
import sys,glob,subprocess,re,cv2,os
s=sys.argv[1];nums=[int(x) for x in sys.argv[2:]]
# locate by page text order: count Pyt occurrences in ocr2 pages
from parse import PYT,clean_lines
pages=sorted(glob.glob(f'ocr2/{s}-p*.txt'))
idx=[]
for p in pages:
    for l in clean_lines(open(p).read()):
        if PYT.match(l): idx.append((p,l[:40]))
for n in nums:
    p,first=idx[n-1]; nxt=idx[n] if n<len(idx) else (None,None)
    png='clean/'+os.path.basename(p)[:-4]+'.png'
    tsv=subprocess.run(['tesseract',png,'-','-l','pol','--psm','6','tsv'],capture_output=True,text=True).stdout
    lines={}
    for row in tsv.splitlines()[1:]:
        c=row.split('\t')
        if len(c)<12 or not c[11].strip(): continue
        k=(c[2],c[3],c[4]);x,y,w,h=map(int,c[6:10])
        L=lines.setdefault(k,{'t':[],'y':y,'y2':y+h});L['t'].append(c[11]);L['y']=min(L['y'],y);L['y2']=max(L['y2'],y+h)
    L=sorted(lines.values(),key=lambda v:v['y'])
    texts=[' '.join(v['t']) for v in L]
    starts=[i for i,t in enumerate(texts) if PYT.match(t)]
    # find order of this question within page
    within=[q for q in idx if q[0]==p].index((p,first))
    a=L[starts[within]]['y']-15
    b=L[starts[within+1]]['y']-5 if within+1<len(starts) else L[-1]['y2']+10
    g=cv2.imread(png,0);g=g[max(0,a):b,:]
    g=cv2.resize(g,(g.shape[1]*2//3,g.shape[0]*2//3),interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'png/crop-{s}-{n}.png',g)
    print(f'png/crop-{s}-{n}.png',g.shape)
