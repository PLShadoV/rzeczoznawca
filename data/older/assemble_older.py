import json,re,collections,subprocess
C=json.load(open('cleaned.json'));fix=json.load(open('autofix.json'))
manual=json.load(open('manual_words.json')) if __import__('os').path.exists('manual_words.json') else {}
fields_override={}
import glob as _g
for _p in sorted(_g.glob('corr/*.txt')):
    _s=_p.split('/')[-1][:10]
    for _l in open(_p,encoding='utf-8'):
        _m=re.match(r'(\d+) ([qabc]) (.*)$',_l.rstrip('\n'))
        if _m: fields_override[f'{_s}-{_m[1]}/{_m[2]}']=_m[3]
W=re.compile(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+')
LOW='a-ząćęłńóśźż'
DBV=set()
for _q in json.load(open('../../dist/questions.json'))['questions']:
    for _t in [_q['question']]+_q['options']: DBV.update(re.findall(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+',_t))
def generic(t):
    t=t.replace('|','l').replace('„','').replace('«','').replace('»','').replace('©','c')
    t=re.sub(r'\s+([,;:.])',r'\1',t)
    t=re.sub(r'([,;:])(?=[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż])',r'\1 ',t)
    # roman numerals I/l confusion
    def rom(m):
        s=m[0]
        if re.fullmatch(r'[\d]+[abz]?',s): return s
        core=re.sub(r'[Il1]','I',s[:-1] if s[-1] in 'abz' else s)
        return core+(s[-1] if s[-1] in 'abz' else '')
    t=re.sub(r'(?<![A-Za-ząćęłńóśźż])(?:[Il1]{2,3}[abz]?|I[l1][abz]?)(?![A-Za-ząćęłńóśźż0-9])',rom,t)
    t=re.sub(rf'(?<=[{LOW},;]) [l|I] (?=[{LOW}])',' i ',t)
    def lowcap(m):
        w=m[2]; lw=w[0].lower()+w[1:]
        return m[1]+(lw if lw in DBV else w)
    t=re.sub(rf'([{LOW},] )([IJ][{LOW}]+)',lowcap,t)
    # lowercase I between words -> i
    t=re.sub(rf'(?<=[{LOW},]) I (?=[{LOW}])',' i ',t)
    # capital J mid-sentence
    t=re.sub(rf'(?<=[{LOW},] )J(?=[{LOW}])','j',t)
    return t.strip()
def fixwords(t):
    def rep(m):
        w=m[0]
        if w in manual: return manual[w]
        return fix.get(w,w)
    return W.sub(rep,t)
out={}
for qid,r in C.items():
    o={}
    for f,v in r['fields'].items():
        t=v['text']
        if v['src']=='ocr': t=generic(fixwords(t)); t=fixwords(t)
        t=re.sub(r'(\d)(zł|m2|m3|ha|cm)\b',r'\1 \2',t)
        o[f]=fields_override.get(f'{qid}/{f}',t)
    for f in 'qabc':
        o[f]=o[f].replace('„','"').replace('”','"').replace('“','"')
        if f'{qid}/{f}' not in fields_override:
            o[f]=re.sub(r'\s+([,;:?!])',r'\1',o[f]); o[f]=re.sub(r'\s+\.$','.',o[f]); o[f]=re.sub(r',(?=[A-Za-ząćęłńóśźż])',', ',o[f]); o[f]=re.sub(r'\s{2,}',' ',o[f]).strip()
    for f in 'ab':
        if f'{qid}/{f}' not in fields_override: o[f]=re.sub(r'[;:]?,$',';',o[f])
    if f'{qid}/c' not in fields_override: o['c']=re.sub(r'[;:]?,$','.',o['c'])
    out[qid]={'q':o['q'],'o':[o['a'],o['b'],o['c']],'src':{f:v['src'] for f,v in r['fields'].items()}}
json.dump(out,open('final_text.json','w'),ensure_ascii=False,indent=1)
# report unknown words
db=json.load(open('../../dist/questions.json'))['questions']
dbv=set()
for q in db:
    for t in [q['question']]+q['options']: dbv.update(W.findall(t))
words=collections.Counter();ctx={}
for qid,r in out.items():
    for f,t in zip('qabc',[r['q']]+r['o']):
        if r['src'][f]=='db' or f'{qid}/{f}' in fields_override: continue
        for m in W.finditer(t):
            if m[0] not in dbv: words[m[0]]+=1;ctx.setdefault(m[0],f"{qid}/{f}: …{t[max(0,m.start()-35):m.end()+25]}…")
p=subprocess.run(['hunspell','-d','pl_PL','-l'],input='\n'.join(words),capture_output=True,text=True)
bad=sorted(set(p.stdout.split()),key=lambda w:-words[w])
json.dump({w:ctx[w] for w in bad},open('unknown.json','w'),ensure_ascii=False,indent=0)
print('unknown words',len(bad))
