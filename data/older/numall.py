import json,re,glob,collections
F=json.load(open('final_text.json'));C=json.load(open('cleaned.json'))
corr=set()
for p in glob.glob('corr/*.txt'):
    s=p[5:15]
    for l in open(p):
        m=re.match(r'(\d+) ([qabc]) ',l)
        if m: corr.add(f'{s}-{m[1]}/{m[2]}')
by=collections.defaultdict(set)
for qid,r in F.items():
    opts=r['o'];ocr=[f for f in 'abc' if C[qid]['fields'][f]['src']!='db' and f'{qid}/{f}' not in corr]
    if not ocr: continue
    if any(re.search(r'\d',t) and len(t)<45 for t in opts) or any(r['o']['abc'.index(f)].strip()=='' for f in ocr):
        by[qid[:10]].add(int(qid[11:]))
tot=0
for s in sorted(by): print(s,sorted(by[s]));tot+=len(by[s])
print(tot)
