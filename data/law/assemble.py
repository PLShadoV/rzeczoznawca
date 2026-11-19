"""Build dist/law-status.json – the current-law layer for the question bank.

Input:  data/law/review-2020-2023.json  (review of every unique question from the 2020–2023 sessions)
        dist/questions.json, dist/legal-bases.json
Output: dist/law-status.json

Statuses (per question id):
  outdated  – the historical key no longer matches the law in force on the review date
  uncertain – the legal state of the underlying act is unclear (e.g. lapsed regulation without a successor)
  changed   – the legal basis changed (new act / renumbered provision) but the keyed answer still holds
  current   – reviewed, no change affecting the answer was found
Questions classified as non-legal (calculations, technology, economics) get no status.

The historical keys and grading are never modified. Run from the repository root:
  python3 data/law/assemble.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW = json.loads((ROOT / 'data/law/review-2020-2023.json').read_text())
QUESTIONS = {q['id']: q for q in json.loads((ROOT / 'dist/questions.json').read_text())['questions']}
LEGAL = json.loads((ROOT / 'dist/legal-bases.json').read_text())['items']

STATUS = {'OUT': 'outdated', 'UNC': 'uncertain', 'CHG': 'changed', 'OK': 'current'}
WT_ACT = 'Rozporządzenie Ministra Infrastruktury z dnia 12 kwietnia 2002 r. w sprawie warunków technicznych'
WT_NOTE = ('Rozporządzenie Ministra Infrastruktury z 12.04.2002 r. w sprawie warunków technicznych, jakim powinny '
           'odpowiadać budynki – według ISAP „uznane za uchylone” z dniem 21.09.2026 r. (art. 66 ustawy z 19.07.2019 r. '
           'o zapewnianiu dostępności osobom ze szczególnymi potrzebami). W Dzienniku Ustaw nie odnaleziono nowego '
           'rozporządzenia dla budynków. Odpowiedź odpowiada ostatniemu brzmieniu tych przepisów; stan prawny do potwierdzenia.')

items = {}


def put(qid, status, note=None):
    if qid not in QUESTIONS:
        return
    entry = {'status': status}
    if note:
        entry['note'] = note
    items[qid] = entry


for group in REVIEW['groups']:
    verdict = group.get('verdict')
    for qid in group['ids']:
        if verdict:
            put(qid, STATUS[verdict], group.get('note'))
        elif LEGAL.get(qid, {}).get('status') != 'nonlegal':
            put(qid, 'current')

# The technical-conditions regulation lapsed for every session, not only 2020–2023.
for qid, entry in LEGAL.items():
    if any(c['act'].startswith(WT_ACT) for c in entry.get('citations', [])):
        if items.get(qid, {}).get('status') in (None, 'current', 'changed'):
            put(qid, 'uncertain', WT_NOTE)
for qid, entry in items.items():
    if entry['status'] == 'uncertain' and not entry.get('note'):
        entry['note'] = WT_NOTE

counts = {s: sum(1 for e in items.values() if e['status'] == s) for s in ('outdated', 'uncertain', 'changed', 'current')}
out = {
    'schemaVersion': 1,
    'checkedAt': REVIEW['reviewedAt'],
    'scope': REVIEW['scope'],
    'counts': counts,
    'items': dict(sorted(items.items())),
}
(ROOT / 'dist/law-status.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '\n')
print(f'law-status: {len(items)} questions, {counts}')

# Human-readable report of everything that is not simply "current".
def date_pl(d):
    months = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia',
              'września', 'października', 'listopada', 'grudnia']
    y, m, day = d.split('-')
    return f'{int(day)} {months[int(m) - 1]} {y}'


lines = [f'# Raport stanu prawnego pytań 2020–2023 (stan na {date_pl(REVIEW["reviewedAt"])})', '',
         'Plik generowany przez `data/law/assemble.py`. Klucze i punktacja się nie zmieniają — to warstwa informacyjna.', '']
labels = {'outdated': 'Nieaktualne po zmianie przepisów', 'uncertain': 'Stan prawny do potwierdzenia (lista 2020–2023; liczba wystąpień obejmuje też pytania 2024–2026 oparte na warunkach technicznych)'}
for status in ('outdated', 'uncertain'):
    seen = set()
    rows = []
    for group in REVIEW['groups']:
        ids = [i for i in group['ids'] if items.get(i, {}).get('status') == status]
        if not ids or group['group'] in seen:
            continue
        seen.add(group['group'])
        q = QUESTIONS[ids[0]]
        keyed = ', '.join('ABC'[i] for i in q['correct'])
        rows.append(f"- **{q['question']}** — klucz: {keyed}; sesje: {', '.join(sorted(ids))}.  \n  {items[ids[0]]['note']}")
    lines += [f'## {labels[status]} ({len(rows)} pytań, {counts[status]} wystąpień w arkuszach)', ''] + rows + ['']
(ROOT / 'data/law/REPORT.md').write_text('\n'.join(lines))
