"""Keep only exam sessions from MIN_SESSION onwards in every published dataset.

Sessions before 2022 were withdrawn from the bank on 2026-11-22 (version 1.5.0).
Run from the repository root after any of the data builds
(data/prepare.py, data/older/merge_into_dist.py, data/legal/assemble.py,
data/explanations/assemble.py), then rebuild the law layer:

  python3 data/prune_sessions.py && python3 data/law/assemble.py

The script is idempotent. Raw sources (PDFs, OCR, review notes) stay in data/.
"""
import json
from pathlib import Path

MIN_SESSION = '2022-01-01'
ROOT = Path(__file__).resolve().parents[1]


def keep(qid):
    return qid[:10] >= MIN_SESSION


def load(rel):
    return json.loads((ROOT / rel).read_text())


q = load('dist/questions.json')
before = len(q['questions'])
q['questions'] = [x for x in q['questions'] if x['session'] >= MIN_SESSION]
q['sessions'] = [s for s in q['sessions'] if s['date'] >= MIN_SESSION]
(ROOT / 'dist/questions.json').write_text(json.dumps(q, ensure_ascii=False))

legal = load('dist/legal-bases.json')
legal['items'] = {k: v for k, v in legal['items'].items() if keep(k)}
legal['counts'] = {s: sum(1 for e in legal['items'].values() if e['status'] == s) for s in ('cited', 'nonlegal', 'unresolved')}
(ROOT / 'dist/legal-bases.json').write_text(json.dumps(legal, ensure_ascii=False, separators=(',', ':')) + '\n')

expl = load('dist/explanations.json')
expl['items'] = {k: v for k, v in expl['items'].items() if keep(k)}
expl['count'] = len(expl['items'])
(ROOT / 'dist/explanations.json').write_text(json.dumps(expl, ensure_ascii=False, indent=2) + '\n')

# Archive (scan-based) mappings only covered withdrawn sessions.
for rel in ('data/legal/archive-2018-2021.json', 'data/explanations/archive-2018-2021.json'):
    path = ROOT / rel
    if path.exists():
        data = json.loads(path.read_text())
        path.write_text(json.dumps({k: v for k, v in data.items() if keep(k)}, ensure_ascii=False, indent=1) + '\n')

print(f"questions {before} -> {len(q['questions'])}, sessions {len(q['sessions'])}, "
      f"legal {legal['counts']}, comments {expl['count']}")
