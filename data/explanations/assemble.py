#!/usr/bin/env python3
"""Build reviewed educational comments, independently of official question keys."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[2]
questions = json.loads((ROOT/'dist/questions.json').read_text())['questions']
legal = json.loads((ROOT/'dist/legal-bases.json').read_text())['items']
expected = {q['id'] for q in questions if legal[q['id']]['status'] != 'cited'}
items = {}
for domain in ['building','economics','law','planning','rural','valuation']:
    source = json.loads((Path(__file__).parent/(domain+'.json')).read_text())
    if set(source) & set(items): raise SystemExit('Duplicate domain mapping')
    items.update(source)
if set(items) != expected: raise SystemExit(f'Coverage mismatch: missing {len(expected-set(items))}; extra {len(set(items)-expected)}')
for key, entry in items.items():
    if len(entry.get('text','').strip()) < 80 or not entry.get('sources'): raise SystemExit('Incomplete: '+key)
    for source in entry['sources']:
        if not source.get('title') or not source.get('url','').startswith('https://'): raise SystemExit('Invalid source: '+key)
output = {'schemaVersion':1,'checkedAt':'2026-11-05','count':len(items),'items':dict(sorted(items.items()))}
(ROOT/'dist/explanations.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(items)} sourced explanations; {sum(bool(e.get("caveat")) for e in items.values())} explicit caveats.')
