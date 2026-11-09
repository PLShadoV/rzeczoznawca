import json,collections
F=json.load(open('final_text.json'))
by=collections.defaultdict(list)
for qid,r in F.items():
    flds=[f for f in 'qabc' if r['src'][f]!='db']
    if flds: by[qid[:10]].append((qid,r,flds))
for s in sorted(by):
    with open(f'review-{s}.txt','w') as fh:
        for qid,r,flds in by[s]:
            fh.write(f"## {qid[11:]}\n")
            for f,t in zip('qabc',[r['q']]+r['o']):
                fh.write(f"{'*' if f in flds else ' '}{f}: {t}\n")
print(sum(len(v) for v in by.values()))
