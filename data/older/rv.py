import json,sys,re,os
sys.argv+=['']
W=re.compile(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+')
dbv=set()
for q in json.load(open('../../dist/questions.json'))['questions']:
    for t in [q['question']]+q['options']: dbv.update(W.findall(t))
import subprocess
F0=json.load(open('final_text.json'))
allw={w for r in F0.values() for t in [r['q']]+r['o'] for w in W.findall(t)}
badw=set(subprocess.run(['hunspell','-d','pl_PL','-l'],input='\n'.join(allw-dbv),capture_output=True,text=True).stdout.split())
def rank(w):
    if re.search(r'[\]\[|$!@#<>{}]',w): return 0
    ws=W.findall(w)
    if not ws: return 1 if re.fullmatch(r'[\d.,;:()%/=+*-]+',w) else 0
    if all(x in dbv or x not in badw for x in ws): return 2
    return 0
F=json.load(open('final_text.json'));C=json.load(open('cleaned.json'))
s=sys.argv[1]
corr=set()
p=f'corr/{s}.txt'
if os.path.exists(p):
    for l in open(p):
        m=re.match(r'(\d+) ([qabc]) ',l)
        if m: corr.add((m[1],m[2]))
RAW=[json.load(open(f'parsed_{p}.json')) for p in ('ocr','ocr2','ocr3')]
def rawlen(qid,f):
    s_,n_=qid[:10],int(qid[11:]);best=0
    for P in RAW:
        q=P[s_][n_-1]; t=q['q'] if f=='q' else q['o'].get(f,'')
        best=max(best,len(re.findall(r'[a-ząćęłńóśźż]{3,}',t)))
    return best
def mark(t): return ' '.join(w if rank(w)>=2 or rank(w)==1 else f'⟦{w}⟧' for w in t.split())
for qid,r in F.items():
    if not qid.startswith(s+'-'): continue
    n=qid[11:];out=[]
    for f,t in zip('qabc',[r['q']]+r['o']):
        v=C[qid]['fields'][f]
        if v['src']=='db' or (n,f) in corr: continue
        agree=v.get('n',0)>=2 and not v.get('alts')
        m=mark(t)
        short=rawlen(qid,f)-len(re.findall(r'[a-ząćęłńóśźż]{3,}',t))>=2
        if short: m='✂ '+m
        if agree and '⟦' not in m and not short: continue
        out.append(f'{f}{"=" if agree else ":"} {m}')
    if out: print('#',n);print('\n'.join(out))
