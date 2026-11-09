import cv2,numpy as np,glob,json,os
def comps(f):
    g=cv2.imread(f,0)
    b=cv2.adaptiveThreshold(g,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,35,15)
    hz=cv2.morphologyEx(b,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_RECT,(22,1)))
    vt=cv2.morphologyEx(b,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_RECT,(1,22)))
    m=cv2.dilate(hz|vt,np.ones((3,3),np.uint8))
    n,lab,st,cen=cv2.connectedComponentsWithStats(m,8)
    bx=[tuple(map(int,st[i][:4])) for i in range(1,n) if 32<=st[i][2]<=62 and 32<=st[i][3]<=62]
    return g,b,bx
def cluster(vals,tol):
    vals=sorted(vals);cl=[]
    for v in vals:
        if cl and v-cl[-1][-1]<=tol: cl[-1].append(v)
        else: cl.append([v])
    return cl
res={}
for sess in sorted({os.path.basename(p)[:10] for p in glob.glob('pages/*.png')}):
    best=None
    for f in sorted(glob.glob(f'pages/{sess}-p*.png')):
        g,b,bx=comps(f)
        if best is None or len(bx)>len(best[3]): best=(f,g,b,bx)
    f,g,b,bx=best
    C=[(x+w/2,y+h/2) for x,y,w,h in bx]
    def score(a):
        h,_=np.histogram([cx-a*cy for cx,cy in C],bins=np.arange(0,3000,6))
        h2=h[:-1]+h[1:]
        return float((h2**2).sum())
    a=max(np.arange(-0.035,0.0351,0.0005),key=score)
    P=[(cx-a*cy,cy+a*cx,cx,cy) for cx,cy in C]  # sheared coords
    cl=sorted(cluster([p[0] for p in P],8),key=len,reverse=True)[:6]
    cols=sorted(float(np.median(c)) for c in cl)
    size=int(np.median([w for x,y,w,h in bx]))
    ans={};num=1;info=[]
    for hi,hc in enumerate([cols[:3],cols[3:]]):
        sel=[p for p in P if min(abs(p[0]-c) for c in hc)<12]
        rows=[float(np.median(c)) for c in cluster([p[1] for p in sel],18)]
        info.append(len(rows))
        rows=rows[-(50 if hi==0 else 40):]
        for ry in rows:
            near=[p for p in sel if abs(p[1]-ry)<18]
            dens=[]
            for c in hc:
                m=[p for p in near if abs(p[0]-c)<12]
                if m: cx,cy=m[0][2],m[0][3]
                else:
                    # invert shear: x' = x - a*y, y'=y+a*x
                    cy=(ry-a*c)/(1+a*a); cx=c+a*cy
                h2=size//2-9
                inner=b[int(cy-h2):int(cy+h2),int(cx-h2):int(cx+h2)]
                dens.append(round(float((inner>0).mean()),3))
            ans[num]=dens;num+=1
    print(sess,f,'slope',round(a,4),'cols',[round(c) for c in cols],'rows',info)
    res[sess]={'file':f,'dens':ans}
json.dump(res,open('keys_raw.json','w'),indent=0)
