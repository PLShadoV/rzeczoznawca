import json,re,difflib,collections,subprocess
from clean_text import strip_tail,best_clean,digits
import sys
if __name__!="__main__" and False: pass
passes=[json.load(open(f'parsed_{p}.json')) for p in ('ocr2','ocr3','ocr')]
fix=json.load(open('autofix.json'))
W=re.compile(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+')
db=json.load(open('../../dist/questions.json'))['questions']
dbv=set()
for q in db:
    for t in [q['question']]+q['options']: dbv.update(W.findall(t))
def fw(t): return W.sub(lambda m:fix.get(m[0],m[0]),t)
# collect all words for hunspell validity
allw=set()
cands={}
for s in passes[0]:
    for i in range(90):
        qid=f'{s}-{i+1}'
        base=passes[0][s][i]['q']
        for f in 'qabc':
            L=[]
            for P in passes:
                q=P[s][i]
                if difflib.SequenceMatcher(None,q['q'][:80],base[:80]).ratio()<0.5: continue
                t=q['q'] if f=='q' else q['o'].get(f)
                if t: L.append(fw(strip_tail(t)))
            cands[(qid,f)]=L
            for t in L: allw.update(W.findall(t))
p=subprocess.run(['hunspell','-d','pl_PL','-l'],input='\n'.join(w for w in allw if w not in dbv),capture_output=True,text=True)
badw=set(p.stdout.split())
json.dump(sorted(badw),open('badw.json','w'))
SHORT=set('a i w z o u do na od po za ze we to są nie lub jak ma m r. zł ha m2 m3 cm dt q pkt ust art kl. ii iii iv vi'.split())
def score(t):
    pen=0
    for w in t.split():
        core=w.strip('.,;:()"„”')
        if not core: pen+=1;continue
        if re.fullmatch(r'[\d.,%/=+*<>-]+',core): continue
        if re.fullmatch(r'(?:I|II|III|IV|V|VI|VII|VIII|IX|X)[abz]?|VIz|Ł|Ps|Bp|Ba|Bi|Lz[IV]+|R|S|N|W|B|Wk|Wl|Ws|WKn|WKb',core): continue
        ws=W.findall(core)
        if not ws or re.search(r'[|\]\[$@#{}<>_—]',w): pen+=2;continue
        if any(x in badw and x not in dbv for x in ws): pen+=2;continue
        if len(core)<=2 and core.lower() not in SHORT: pen+=1.5
        if re.fullmatch(r'[A-ZĄĆĘŁŃÓŚŹŻ]{2,}',core) and core not in dbv: pen+=1
    return pen
def rank(w):
    if re.search(r'[\]\[|$!@#<>{}]',w): return 0
    ws=W.findall(w)
    if not ws: return 1 if re.fullmatch(r'[\d.,;:()%-]+',w) else 0
    if all(x in dbv for x in ws): return 3
    if all(x in dbv or x not in badw for x in ws): return 2
    return 0
def valid(w): return rank(w)>=2
def wordmerge(t,alts):
    B=t.split()
    for a in alts:
        A=a.split()
        sm=difflib.SequenceMatcher(None,B,A,autojunk=False)
        NB=[]
        for op,i1,i2,j1,j2 in sm.get_opcodes():
            if op=='equal': NB+=B[i1:i2];continue
            if op=='replace' and i2-i1==j2-j1:
                for x,y in zip(B[i1:i2],A[j1:j2]):
                    NB.append(y if rank(y)>rank(x) else x)
            elif op=='replace' and i2-i1==1 and j2-j1==2 and not valid(B[i1]) and all(valid(y) for y in A[j1:j2]):
                NB+=A[j1:j2]
            elif op=='replace' and i2-i1==2 and j2-j1==1 and not all(valid(x) for x in B[i1:i2]) and valid(A[j1]):
                NB+=A[j1:j2]
            elif op=='insert':
                ins=A[j1:j2]
                good=[w for w in ins if rank(w)>=2]
                if len(good)==len(ins) and len(ins)>=1 and not (len(ins)==1 and len(ins[0])<=2): NB+=ins
            else: NB+=B[i1:i2]
        B=NB
    return ' '.join(B)
out={};st=collections.Counter()
for (qid,f),L in cands.items():
    rec=None
    for t in L:
        b=best_clean(t) if t else None
        if b:
            tail=re.search(r'[\s.;:,]*$',t)[0].strip()
            rec={'text':b[1]+tail,'src':'db'};break
    if not rec:
        if not L: rec={'text':'','src':'missing'}
        else:
            t=min(L,key=score)
            t=wordmerge(t,[x for x in L if x!=t])
            rec={'text':t,'src':'ocr','alts':[x for x in L if x!=t],'n':len(L)}
    st[rec['src']]+=1
    out.setdefault(qid,{'fields':{}})['fields'][f]=rec
json.dump(out,open('cleaned.json','w'),ensure_ascii=False,indent=1)
print(st, 'fully-db', sum(all(v['src']=='db' for v in r['fields'].values()) for r in out.values()))
