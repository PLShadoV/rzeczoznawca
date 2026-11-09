"""Assemble editorial legal references without modifying exam questions or keys."""
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit
import json,re,unicodedata
ROOT=Path(__file__).resolve().parents[2]
_DATA=json.loads((ROOT/'dist/questions.json').read_text())
ARCHIVE_DATES={s['date'] for s in _DATA['sessions'] if s.get('archive')}
ALL_QUESTIONS=_DATA['questions']
# 2018-2021 archive sessions have their own mapping file (data/legal/archive-2018-2021.json).
QUESTIONS=[q for q in ALL_QUESTIONS if q['session'] not in ARCHIVE_DATES]
DOMAINS=['building','law','valuation','rural','economics','planning']
items={};reports={}
for domain in DOMAINS:
 assigned=json.loads((ROOT/f'data/legal/domains/{domain}-questions.json').read_text())
 expected={q['id'] for g in assigned for q in g['occurrences']}
 result=json.loads((ROOT/f'data/legal/domains/{domain}-citations.json').read_text())
 assert isinstance(result,dict),domain
 assert set(result)==expected,(domain,'coverage mismatch',len(expected-set(result)),len(set(result)-expected))
 for qid,entry in result.items():
  assert entry.get('status') in ['cited','nonlegal','unresolved'],(domain,qid)
  entry=dict(entry)
  if entry['status']!='cited' and entry.get('citations'):
   entry['researchLeads']=entry['citations'];entry['citations']=[]
  citations=entry.get('citations',[])
  assert isinstance(citations,list),(qid,'citations must be list')
  assert bool(citations)==(entry['status']=='cited'),(qid,'unexpected or missing citations')
  for c in citations:
   assert all(isinstance(c.get(k),str) and c[k].strip() for k in ['act','provision','url','evidence']),(qid,'missing fields')
   u=urlsplit(c['url']);assert u.scheme=='https' and (u.hostname=='eli.gov.pl' or u.hostname.endswith('.gov.pl')),(qid,c['url'])
   assert re.search(r'(?:art\.?\s*\d|§\s*\d|załącznik|zał\.\s*\d)',c['provision'],re.I),(qid,c['provision'])
   assert len(c['evidence'].strip())>=20,(qid,'insufficient source evidence')
  if entry['status']!='cited':assert isinstance(entry.get('note'),str) and entry['note'].strip(),(qid,'explanation missing')
  assert qid not in items,qid
  items[qid]=entry
 reports[domain]=dict(Counter(e['status'] for e in result.values()))
assert set(items)=={q['id'] for q in QUESTIONS}
for path in sorted((ROOT/'data/legal').glob('*-extra.json'))+[ROOT/'data/legal/owner-citations.json']:
 if not path.exists():continue
 extra=json.loads(path.read_text())
 for qid,entry in extra.items():
  assert qid in items,(path,qid)
  if items[qid]['status']=='unresolved' or items[qid]['status']=='nonlegal' and entry['status']=='cited':items[qid]=entry
for domain in DOMAINS:
 assigned=json.loads((ROOT/f'data/legal/domains/{domain}-questions.json').read_text())
 ids=[q['id'] for g in assigned for q in g['occurrences']]
 reports[domain]=dict(Counter(items[i]['status'] for i in ids))
archive_path=ROOT/'data/legal/archive-2018-2021.json'
if archive_path.exists():
 items.update(json.loads(archive_path.read_text()))
assert set(items)=={q['id'] for q in ALL_QUESTIONS}
# Exact repeated question/answer sets can expose inconsistent editorial classifications.
groups={}
for q in QUESTIONS:
 key=json.dumps([q['question'],q['options'],q['correct']],ensure_ascii=False)
 groups.setdefault(key,[]).append(q['id'])
conflicts=[]
for ids in groups.values():
 statuses={items[i]['status'] for i in ids}
 if 'cited' in statuses and 'nonlegal' in statuses:conflicts.append(ids)
counts=dict(Counter(e['status'] for e in items.values()))
for status in ['cited','nonlegal','unresolved']:counts.setdefault(status,0)
output={'schemaVersion':1,'checkedAt':'2026-11-05','counts':counts,'items':items}
for entry in items.values():
 entry.pop('researchLeads',None)
(ROOT/'dist/legal-bases.json').write_text(json.dumps(output,ensure_ascii=False,separators=(',',':'))+'\n')
(ROOT/'data/legal/coverage.json').write_text(json.dumps({'counts':counts,'domains':reports,'classificationConflicts':conflicts},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'counts':counts,'domains':reports,'classificationConflicts':len(conflicts)},ensure_ascii=False,indent=2))
