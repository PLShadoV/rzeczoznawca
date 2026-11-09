import json,re,difflib,collections
db=json.load(open('../../dist/questions.json'))['questions']
P=json.load(open('parsed.json'))
def digits(s):
    s=re.sub(r'(?<=\d)[\s\u00a0](?=\d{3}\b)','',s)
    return '|'.join(re.findall(r'\d+(?:[.,]\d+)*',s))
def strip_tail(s):
    s=s.strip(' _|—-~')
    # remove trailing junk tokens after final ; or .
    m=re.match(r'^(.*[\.;:,!?])((?:\s+\S{1,6}){1,6})\s*$',s)
    if m and re.search(r'\b[IV]{1,3}[abz]?\b',m[2]) and re.search(r'\b(?:I|II|III|IV|V|VI)[abz]?[;.,]',m[2]): m=None
    if m and not re.search(r'[A-Za-ząćęłńóśźż]{4,}',m[2]) and not (re.search(r'[:;.,]$',m[2].strip()) and re.search(r'\b[a-ząćęłńóśźż]{2,}\b',m[2])): s=m[1]
    m=re.match(r'^(.*[\.;:!?])\s+(.{1,80})$',s)
    if m:
        tail=m[2];low=sum(c.islower() for c in tail);alpha=sum(c.isalpha() for c in tail)
        if re.search(r'[:;.]$',tail.strip()) and low/max(alpha,1)>=0.6: pass
        elif alpha==0 or low/alpha<0.6 or re.search(r'[_—|]{1,}|\b[A-ZĄĆĘŁŃÓŚŹŻ]{3,}\b',tail) and len(tail)<60: s=m[1]
    s=re.sub(r'[\s_—|\-]{2,}[^\s]{0,12}$','',s) if re.search(r'[_—|]{2,}',s) else s
    s=re.sub(r'^[\W_]+(?=[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9])','',s)
    return s.strip()
def key(s): return re.sub(r'\W','',s.lower())
SEG=collections.defaultdict(set)  # index by 6-gram of key
STR=[];seen=set()
for q in db:
    for t in [q['question']]+q['options']:
        if t in seen: continue
        seen.add(t);STR.append(t)
for i,t in enumerate(STR):
    k=key(t)
    for j in range(0,max(1,len(k)-6),3): SEG[k[j:j+6]].add(i)
GROUPS=['lIi1|!ł','eęc','aąo','oóO0','sś','cć','zżź','nń','uv','rn','m','8B','5S','0O','tf','hb','yv']
def conf(x,y):
    x=x.replace(' ','');y=y.replace(' ','')
    if x==y: return True
    strip=lambda t:''.join(ch for ch in t if ch.isalnum())
    if strip(x)==strip(y): return True
    if {x,y}=={'rn','m'}: return True
    if len(x)==len(y)<=2:
        return all(p==q or any(p in g and q in g for g in GROUPS) for p,q in zip(x,y))
    return False
def acceptable(a,b):
    if digits(a)!=digits(b): return False
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    tot=0
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': continue
        x,y=a[i1:i2],b[j1:j2]
        if not conf(x,y): return False
        tot+=max(len(x),len(y))
    return tot<=max(4,0.08*len(b))
def best_clean(a):
    k=key(a);c=collections.Counter()
    for j in range(0,max(1,len(k)-6),2):
        for i in SEG.get(k[j:j+6],()): c[i]+=1
    best=None
    for i,_ in c.most_common(25):
        b=STR[i]
        # ignore trailing punctuation difference
        a2=a.rstrip(' .;:,');b2=b.rstrip(' .;:,')
        if acceptable(a2,b2):
            r=difflib.SequenceMatcher(None,a2,b2,autojunk=False).ratio()
            if best is None or r>best[0]: best=(r,b2,b)
    return best
out={};stats=collections.Counter()
for s,qs in P.items():
    for q in qs:
        qid=f"{s}-{q['n']}"
        rec={'id':qid,'n':q['n'],'session':s,'fields':{}}
        for f,txt in [('q',q['q'])]+[(l,q['o'].get(l,'')) for l in 'abc']:
            t=strip_tail(txt)
            b=best_clean(t) if t else None
            if b:
                # keep OCR trailing punctuation
                tail=re.search(r'[\s.;:,]*$',t)[0].strip()
                clean=b[1]+(tail if tail else '')
                rec['fields'][f]={'text':clean,'src':'db','ocr':t,'exact':b[1]==t.rstrip(' .;:,')}
                stats['db']+=1
            else:
                rec['fields'][f]={'text':t,'src':'ocr'};stats['ocr']+=1
        out[qid]=rec
json.dump(out,open('cleaned.json','w'),ensure_ascii=False,indent=1)
print(stats)
q=sum(1 for r in out.values() if all(v['src']=='db' for v in r['fields'].values()))
print('fully db-clean questions',q,'of',len(out))
