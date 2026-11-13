"""Merge the archive sessions (2020-2021; 2018-2019 withdrawn) into dist/ and apply editorial spelling fixes.

Inputs (all in data/older/):
  final_text.json  - question and answer text after OCR + manual proofreading (built by assemble_older.py)
  keys.json        - answer keys read from the scanned key grids (keys_detect.py)
  sources-older.json - official PDF links for each archive session
Outputs:
  dist/questions.json, dist/legal-bases.json, dist/explanations.json
  data/text-corrections.json (log of spelling fixes applied to the 2021-2026 text)

Run from the repository root:  python3 data/older/merge_into_dist.py
The script is idempotent: archive sessions already present are replaced.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'data'))
from text_fixes import fix_text  # noqa: E402

OLD = ROOT / 'data/older'
FINAL = json.loads((OLD / 'final_text.json').read_text())
KEYS = json.loads((OLD / 'keys.json').read_text())
SRC = json.loads((OLD / 'sources-older.json').read_text())

# Official corrections published by the ministry next to the 2020 sheets.
KEY_CORRECTIONS = {
    '2020-06-25-57': ([1], 'Klucz uwzględnia oficjalne sprostowanie ministerstwa: w pytaniu 57 prawidłowa odpowiedź to b).', SRC['2020-06-25']['correction']),
    '2020-07-30-61': ([0, 1, 2], 'Klucz uwzględnia oficjalne sprostowanie ministerstwa: w pytaniu 61 prawidłowe odpowiedzi to a), b) i c).', SRC['2020-07-30']['correction']),
}


def category(t, n):
    t = t.lower()
    if any(x in t for x in ['lasu', 'leśn', 'drzewostan', 'drewna', 'roln', 'żyta', 'upraw', 'plantac', 'siedlisk']): return 'Rolnictwo i leśnictwo'
    if any(x in t for x in ['ewidenc', 'geodez', 'rozgranicz', 'planowania', 'planowani', 'planu miejscow', 'planem miejscow', 'zagospodarowania przestrzen', 'warunkach zabudowy', 'lokalizacji inwestycji']): return 'Planowanie i geodezja'
    if n <= 9 or any(x in t for x in ['prawo budowlane', 'strop', 'fundament', 'kondygnac', 'budowlanych']): return 'Budownictwo'
    if n <= 18 or any(x in t for x in ['rachunkowo', 'inflac', 'rynk', 'ekonom', 'kapitał', 'statyst', 'warianc', 'odchylen', 'korelac']) and n < 19: return 'Ekonomia i finanse'
    if any(x in t for x in ['wycen', 'wartoś', 'podejści', 'operat', 'kapitaliz', 'dyskont', 'porównywan', 'ceny średniej', 'zużyci', 'kosztów odtworzenia', 'dochod']): return 'Wycena nieruchomości'
    return 'Prawo i gospodarka nieruchomościami'


def sig(q):
    norm = lambda s: re.sub(r'[^0-9a-ząćęłńóśźż]', '', s.lower())
    return json.dumps([norm(q['question'])] + [norm(o) for o in q['options']] + [q['correct']])


data = json.loads((ROOT / 'dist/questions.json').read_text())
# Only sessions listed in sources-older.json are published (2018-2019 were withdrawn
# from the bank on 2026-11-13). Previously merged archive sessions are always rebuilt.
archive_dates = set(SRC)
previous_archive = {s['date'] for s in data['sessions'] if s.get('archive')} | archive_dates
current = [q for q in data['questions'] if q['session'] not in previous_archive]
sessions = [s for s in data['sessions'] if s['date'] not in previous_archive]

# 1) Spelling fixes in the 2021-2026 text (logged).
log = []
for q in current:
    for field, idx in [('question', None), ('options', 0), ('options', 1), ('options', 2)]:
        before = q[field] if idx is None else q[field][idx]
        after = fix_text(before)
        if after != before:
            log.append({'id': q['id'], 'field': field if idx is None else f'option {"abc"[idx]}', 'before': before, 'after': after})
            if idx is None: q[field] = after
            else: q[field][idx] = after

# 2) Archive questions.
archive = []
for date in sorted(archive_dates, reverse=True):
    src = SRC[date]
    for n in range(1, 91):
        qid = f'{date}-{n}'
        r = FINAL[qid]
        q = {'id': qid, 'number': n, 'session': date, 'question': fix_text(r['q']),
             'options': [fix_text(o) for o in r['o']], 'correct': KEYS[date][str(n)],
             'category': None, 'source': src['pdf'], 'keySource': src['pdf']}
        if qid in KEY_CORRECTIONS:
            fixed, note, link = KEY_CORRECTIONS[qid]
            q['correct'] = fixed
            q['keyNote'] = note
            q['keySource'] = link
        assert q['question'] and all(q['options']) and q['correct'], qid
        q['category'] = category(q['question'], n)
        archive.append(q)
    sessions.append({'date': date, 'count': 90, 'source': src['pdf'], 'keySource': src['pdf'], 'archive': True})

questions = sorted(current + archive, key=lambda q: (q['session'], -q['number']), reverse=True)
sessions.sort(key=lambda s: s['date'], reverse=True)
assert len({q['id'] for q in questions}) == len(questions)
(ROOT / 'dist/questions.json').write_text(json.dumps({'questions': questions, 'sessions': sessions}, ensure_ascii=False))
if log:  # a re-run on already corrected text finds nothing; keep the existing log
    (ROOT / 'data/text-corrections.json').write_text(json.dumps(log, ensure_ascii=False, indent=1) + '\n')

# 3) Legal layer and educational comments: reuse entries of identical 2021-2026 questions.
legal = json.loads((ROOT / 'dist/legal-bases.json').read_text())
expl = json.loads((ROOT / 'dist/explanations.json').read_text())
items = {k: v for k, v in legal['items'].items() if k[:10] not in previous_archive}
eitems = {k: v for k, v in expl['items'].items() if k[:10] not in previous_archive}
by_sig = {}
for q in current:
    by_sig.setdefault(sig(q), q['id'])
archive_entries = {}
archive_comments = {}
copied = 0
for q in archive:
    twin = by_sig.get(sig(q))
    if twin and twin in items:
        entry = json.loads(json.dumps(items[twin]))
        if twin in eitems:
            eitems[q['id']] = eitems[twin]
            archive_comments[q['id']] = twin
        copied += 1
    else:
        entry = {'status': 'unresolved', 'citations': [],
                 'note': 'Pytanie z archiwalnej sesji (2018–2021). Przypis prawny nie został jeszcze opracowany. '
                         'Przepisy mogły zmienić się od daty egzaminu — odpowiedź jest zgodna z historycznym kluczem.'}
    items[q['id']] = entry
    archive_entries[q['id']] = entry
counts = {s: sum(1 for e in items.values() if e['status'] == s) for s in ('cited', 'nonlegal', 'unresolved')}
legal['items'] = items
legal['counts'] = counts
(ROOT / 'dist/legal-bases.json').write_text(json.dumps(legal, ensure_ascii=False, separators=(',', ':')) + '\n')
(ROOT / 'data/legal/archive-2018-2021.json').write_text(json.dumps(archive_entries, ensure_ascii=False, indent=1) + '\n')
expl['items'] = dict(sorted(eitems.items()))
(ROOT / 'data/explanations/archive-2018-2021.json').write_text(json.dumps(dict(sorted(archive_comments.items())), indent=1) + '\n')
expl['count'] = len(eitems)
(ROOT / 'dist/explanations.json').write_text(json.dumps(expl, ensure_ascii=False, indent=2) + '\n')
print(f'questions={len(questions)} sessions={len(sessions)} archive={len(archive)} '
      f'legal copied from identical questions={copied} spelling fixes={len(log)} counts={counts} comments={len(eitems)}')
