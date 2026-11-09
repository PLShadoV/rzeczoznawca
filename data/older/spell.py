import json,re,subprocess,collections,itertools
C=json.load(open('cleaned.json'))
db=json.load(open('../../dist/questions.json'))['questions']
W=re.compile(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+')
dbv=collections.Counter()
for q in db:
    for t in [q['question']]+q['options']: dbv.update(W.findall(t))
words=collections.Counter()
for r in C.values():
    for f in r['fields'].values():
        if f['src']=='ocr': words.update(W.findall(f['text']))
TIERS=[{'l':['i'],'I':['i','l'],'ł':['l'],'J':['j'],'i':['l']},
       {'l':['i','ł'],'I':['i','l','ł'],'ł':['l'],'J':['j'],'i':['l'],'ą':['ę'],'ę':['ą'],'rn':['m'],'m':['rn'],'ź':['ż'],'ż':['ź'],'z':['ż'],'s':['ś'],'c':['ć','e'],'n':['ń'],'o':['ó'],'a':['ą','e'],'e':['ę','a','o']}]
def variants(w,CONF,maxsub=4):
    pos=[]
    for i in range(len(w)):
        for k in ('rn',w[i]):
            if w.startswith(k,i) and k in CONF: pos.append((i,k))
    for n in range(1,maxsub+1):
        out=set()
        for combo in itertools.combinations(pos,n):
            idx=[p[0] for p in combo]
            if len(set(idx))<n: continue
            for subs in itertools.product(*[CONF[k] for _,k in combo]):
                t=w;off=0
                for (i,k),r in sorted(zip(combo,subs)):
                    t=t[:i+off]+r+t[i+off+len(k):];off+=len(r)-len(k)
                out.add(t)
        yield n,out
def hun(ws):
    p=subprocess.run(['hunspell','-d','pl_PL','-l'],input='\n'.join(ws),capture_output=True,text=True)
    return set(p.stdout.split())
allw=list(words)
bad=hun([w for w in allw if w not in dbv])
fix={}
plan={}
for w in bad:
    if len(w)<3: continue
    plan[w]=[]
    for ti,CONF in enumerate(TIERS):
        for n,v in variants(w,CONF,4 if ti==0 else 2):
            plan[w].append((ti,n,[x for x in v if x!=w]))
allv=sorted({x for L in plan.values() for _,_,v in L for x in v})
print('variants',len(allv),flush=True)
badv=hun(allv)
for w,L in plan.items():
    for ti,n,v in L:
        good=[x for x in v if x not in badv]
        if good:
            if len(good)==1: fix[w]=good[0]
            break
unres=[w for w in bad if w not in fix]
print('bad',len(bad),'fixed',len(fix),'unresolved',len(unres))
json.dump({'fix':fix,'unres':sorted(unres,key=lambda w:-words[w])},open('spell.json','w'),ensure_ascii=False,indent=0)
