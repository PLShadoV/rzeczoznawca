#!/usr/bin/env python3
from pathlib import Path
import json, urllib.parse, hashlib, subprocess
r=Path(__file__).resolve().parents[1]
qs=json.loads((r/'dist/questions.json').read_text())['questions']
legal=json.loads((r/'dist/legal-bases.json').read_text())['items']
e=json.loads((r/'dist/explanations.json').read_text())
required={q['id'] for q in qs if legal[q['id']]['status']!='cited'}
assert e['schemaVersion']==1 and e['count']==len(required)==len(e['items'])
assert set(e['items'])==required
for key,item in e['items'].items():
 assert isinstance(item['text'],str) and len(item['text'].strip())>=80,key
 assert item['sources'],key
 for s in item['sources']:
  u=urllib.parse.urlsplit(s['url'])
  assert u.scheme=='https' and u.hostname and not u.username and s['title'],(key,s)
 assert '<script' not in item['text'].lower(),key
print('PASS: all',len(required),'questions without cited statutes have substantive comments and HTTPS sources; official keys remain a separate layer.')
