"""Integrity of the current-law layer (dist/law-status.json)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
law = json.loads((ROOT / 'dist/law-status.json').read_text())
questions = {q['id']: q for q in json.loads((ROOT / 'dist/questions.json').read_text())['questions']}
legal = json.loads((ROOT / 'dist/legal-bases.json').read_text())['items']
assert law['schemaVersion'] == 1 and law['checkedAt']
items = law['items']
assert set(items) <= set(questions), 'unknown question ids'
for qid, e in items.items():
    assert e['status'] in ('outdated', 'uncertain', 'changed', 'current'), qid
    if e['status'] != 'current':
        assert len(e.get('note', '')) >= 30, f'{qid}: status without explanation'
    if e['status'] == 'outdated':
        assert e.get('annulled') is True or (e.get('currentCorrect') and set(e['currentCorrect']) <= {0, 1, 2}), f'{qid}: outdated without current-law key'
    else:
        assert 'currentCorrect' not in e and 'annulled' not in e, qid
counts = {s: sum(1 for e in items.values() if e['status'] == s) for s in law['counts']}
assert counts == law['counts'], 'counts out of date – run data/law/assemble.py'
missing = [qid for qid, q in questions.items()
           if q['session'] <= '2023-12-31' and qid not in items and legal.get(qid, {}).get('status') != 'nonlegal']
assert not missing, f'2022–2023 questions without a law status: {missing[:5]}'
print(f"PASS: current-law layer for {len(items)} questions {law['counts']}; every 2022–2023 legal question reviewed (checked {law['checkedAt']}).")
