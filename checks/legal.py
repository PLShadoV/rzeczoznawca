"""Check reference coverage, integrity, and audit flags for potentially inaccurate labels."""
import json,re
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit
q=json.loads(Path('dist/questions.json').read_text())['questions']
x=json.loads(Path('dist/legal-bases.json').read_text());items=x['items'];assert x['schemaVersion']==1
assert set(items)=={z['id'] for z in q}
assert Counter(e['status'] for e in items.values())==Counter(x['counts'])
flags=[]
for z in q:
 e=items[z['id']];assert e['status'] in {'cited','nonlegal','unresolved'}
 if e['status']=='cited':
  assert e['citations']
  for c in e['citations']:
   assert all(c.get(k) for k in ['act','provision','url','evidence'])
   u=urlsplit(c['url']);assert u.scheme=='https' and u.hostname.endswith('gov.pl')
   assert re.search(r'art\.?\s*\d|§\s*\d|załącznik|zał\.\s*\d',c['provision'],re.I)
 else:assert not e.get('citations') and e.get('note')
 if e['status']=='nonlegal' and re.search(r'ustaw|kodeks|rozporządzen|zgodnie z przepis|według przepis',z['question'],re.I):flags.append({'id':z['id'],'question':z['question'],'note':e['note']})
Path('data/legal/audit-flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
print('PASS: all',len(q),'question IDs represented; official links, exact provisions and supporting excerpts required for citations.')
print('Coverage:',x['counts'],'Nonlegal statements needing manual spot review:',len(flags))
