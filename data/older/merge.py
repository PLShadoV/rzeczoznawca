import json
p1=json.load(open('parsed_ocr.json'));p2=json.load(open('parsed_ocr2.json'))
out={};left=[]
for s,qs in p2.items():
    assert len(qs)==90,(s,len(qs))
    q1={q['n']:q for q in p1.get(s,[])} if len(p1.get(s,[]))==90 else {}
    res=[]
    for q in qs:
        if set(q['o'])!=set('abc'):
            alt=q1.get(q['n'])
            if alt and set(alt['o'])==set('abc'):
                o=dict(alt['o']);o.update(q['o']);q=dict(q);q['o']=o
            else: left.append((s,q['n']))
        res.append(q)
    out[s]=res
json.dump(out,open('parsed.json','w'),ensure_ascii=False,indent=1)
print('left',len(left),left)
