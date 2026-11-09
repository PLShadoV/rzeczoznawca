import json,re,glob
from clean_text import digits
F=json.load(open('final_text.json'));C=json.load(open('cleaned.json'))
RAW=[json.load(open(f'parsed_{p}.json')) for p in ('ocr','ocr2','ocr3')]
corr=set()
for p in glob.glob('corr/*.txt'):
    s=p[5:15]
    for l in open(p):
        m=re.match(r'(\d+) ([qabc]) ',l)
        if m: corr.add(f'{s}-{m[1]}/{m[2]}')
out=[]
for qid,r in F.items():
    s,n=qid[:10],int(qid[11:])
    for f,t in zip('qabc',[r['q']]+r['o']):
        if C[qid]['fields'][f]['src']=='db' or f'{qid}/{f}' in corr: continue
        if not re.search(r'\d',t): 
            # raw has digits but final not?
            if any(re.search(r'\d{2,}',(P[s][n-1]['q'] if f=='q' else P[s][n-1]['o'].get(f,''))) for P in RAW): out.append((qid,f,t))
            continue
        ds={digits(P[s][n-1]['q'] if f=='q' else P[s][n-1]['o'].get(f,'')) for P in RAW}
        if len(ds)>1 or digits(t) not in ds: out.append((qid,f,t))
for x in out: print(*x)
print(len(out))
