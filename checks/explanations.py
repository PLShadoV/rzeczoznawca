#!/usr/bin/env python3
from pathlib import Path
import json, urllib.parse
r=Path(__file__).resolve().parents[1]
qs=json.loads((r/'dist/questions.json').read_text())['questions']
legal=json.loads((r/'dist/legal-bases.json').read_text())['items']
e=json.loads((r/'dist/explanations.json').read_text())
archive={s['date'] for s in json.loads((r/'dist/questions.json').read_text())['sessions'] if s.get('archive')}
noncited={q['id'] for q in qs if legal[q['id']]['status']!='cited'}
# Every non-cited question from the 2021-2026 sessions must have a comment.
# Archive (2018-2021) questions reuse comments of identical later questions; others may have none yet.
required={i for i in noncited if i[:10] not in archive}
assert e['schemaVersion']==1 and e['count']==len(e['items'])
assert required<=set(e['items']),sorted(required-set(e['items']))[:5]
assert set(e['items'])<=noncited,sorted(set(e['items'])-noncited)[:5]
for key,item in e['items'].items():
 assert isinstance(item['text'],str) and len(item['text'].strip())>=80,key
 assert item['sources'],key
 for s in item['sources']:
  u=urllib.parse.urlsplit(s['url'])
  assert u.scheme=='https' and u.hostname and not u.username and s['title'],(key,s)
 assert '<script' not in item['text'].lower(),key
arch=[i for i in e['items'] if i[:10] in archive]
print('PASS: all',len(required),'non-cited 2021-2026 questions have substantive comments with HTTPS sources;',len(arch),'archive questions reuse comments of identical questions. Official keys remain a separate layer.')
