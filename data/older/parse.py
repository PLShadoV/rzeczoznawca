import re,json,glob,os,sys
OCRDIR=os.environ.get('OCRDIR','ocr2')
def load(sess):
    out=[]
    for f in sorted(glob.glob(f'{OCRDIR}/{sess}-p*.txt')):
        t=open(f).read()
        if 'Pyt' not in t and 'Odp' not in t: continue
        out.append(t)
    return '\n'.join(out)
HDR=re.compile(r'(zaznacz|egzempl|egzampł|Str?ona\s*\S{1,2}\s*z|ŃSTWOWA|STWOWA|KWALIF|IFIKACYJ|ACYJNA|przeprowadzana|Kod:|EGZAMIN|PAŃSTWOWA|KOMISJA|KWALIFIKACYJNA|UPRAWNIENIA ZAWOD|ZAWODOWE|MAJĄTKOWEGO|RZECZOZNAWCY MAJ|Część p.semna|Proszę nie zaznaczać|Strona\s*\d+\s*z\s*\d+|^\W*$)')
def clean_lines(t):
    L=[]
    for l in t.splitlines():
        if HDR.search(l) and not re.match(r'^.{0,5}?\b[PBF][yv][tlł1i](?![a-ząćęłńóśźż])|^[\W_]{0,4}Od[pę]',l): continue
        L.append(l)
    return L
OPT=re.compile(r'^[\W_]{0,4}Od[pę][\.,:]?\s*([abc©eo])[\s_\.,:)]+(.*)$')
PYT=re.compile(r'^.{0,5}?\b[PBF][yv][tlł1i](?![a-ząćęłńóśźż])[\.,]?\s*([\dOo$?BSl]{0,2})\s*(.*)$')
def parse(sess):
    L=clean_lines(load(sess))
    qs=[];cur=None;target=None
    for l in L:
        m=PYT.match(l)
        if m:
            cur={'n':m[1],'q':[m[2]],'o':{}};qs.append(cur);target=cur['q'];continue
        m=OPT.match(l)
        if m and cur is not None:
            lab={'©':'c','e':'c','o':'c'}.get(m[1],m[1])
            if lab in cur['o']:
                # duplicate label: probably misread; assign next missing
                miss=[x for x in 'abc' if x not in cur['o']]
                lab=miss[0] if miss else lab
            cur['o'][lab]=[m[2]];target=cur['o'][lab];continue
        if target is not None: target.append(l)
    return qs
def tidy(parts):
    s=' '.join(p.strip() for p in parts)
    s=re.sub(r'\s+',' ',s).strip()
    # remove trailing scan noise like " s sa a sa m m a" or "5 = — = a ="
    s=re.sub(r'(\s+[\W\dsamy_]{1,2}){3,}$','',s)
    return s.strip(' _')
if __name__=='__main__':
    res={}
    for sess in sorted({os.path.basename(p)[:10] for p in glob.glob(OCRDIR+'/*.txt')}):
        qs=parse(sess)
        for i,q in enumerate(qs): q['ocrn']=q['n'];q['n']=i+1
        nums=[q['n'] for q in qs]
        mism=[(q['n'],q['ocrn']) for q in qs if q['ocrn']!=str(q['n'])]
        bad=[q['n'] for q in qs if set(q['o'])!=set('abc')]
        print(sess,len(qs),'missing',sorted(set(range(1,91))-set(nums)),'dupe',sorted({n for n in nums if nums.count(n)>1}),'badopts',bad,'mism',mism[:8])
        res[sess]=[{'n':q['n'],'q':tidy(q['q']),'o':{k:tidy(v) for k,v in q['o'].items()}} for q in qs]
    json.dump(res,open('parsed.json','w'),ensure_ascii=False,indent=1)
