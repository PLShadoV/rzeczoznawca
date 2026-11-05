"""Independent excerpt provenance check against retained official source corpora.
Run after sources have been downloaded; visual-scan references remain explicitly flagged.
"""
import json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def norm(s):return re.sub(r'[^\w]+','',unicodedata.normalize('NFKC',s).casefold()).replace('_','')
sources=ROOT/'data/legal/sources'
files=list(sources.glob('*.txt'))+list(sources.glob('*-corpus.json'))+list(sources.glob('*-provisions.json'))
haystacks=[]
for p in files:
 if p.suffix=='.json':
  def strings(o):
   if isinstance(o,str):return [o]
   if isinstance(o,dict):return [s for v in o.values() for s in strings(v)]
   if isinstance(o,list):return [s for v in o for s in strings(v)]
   return []
  text='\n'.join(strings(json.loads(p.read_text())))
 else:text=p.read_text(errors='replace')
 haystacks.append((p.name,norm(text)))
x=json.loads((ROOT/'dist/legal-bases.json').read_text());unique={}
for id,e in x['items'].items():
 if e['status']=='cited':
  for c in e['citations']:unique.setdefault((c['url'],c['provision'],c['evidence']),{'citation':c,'ids':[]})['ids'].append(id)
fail=[];visual=[]
for v in unique.values():
 c=v['citation'];evidence=c['evidence']
 if c.get('sourceVerification')=='visual-scan':visual.append(v);continue
 # Bracketed omissions, ellipses and line hyphenation are permitted, but actual words must exist.
 segments=[s for s in re.split(r'\[?[…]+\]?|\.{3}',evidence) if len(norm(s))>=20]
 if not segments and '=' in evidence and len(norm(evidence))>=6:segments=[evidence]
 if not segments:fail.append(v);continue
 if not any(all(norm(s) in text for s in segments) for name,text in haystacks):fail.append(v)
report={'uniqueCitations':len(unique),'textMatched':len(unique)-len(fail)-len(visual),'visual':visual,'unmatched':fail}
(ROOT/'data/legal/evidence-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('Unique citation passages:',len(unique),'Text matched:',report['textMatched'],'Manually checked scans:',len(visual),'Unmatched:',len(fail))
for v in fail[:12]:print(v['ids'][0],v['citation']['provision'],v['citation']['evidence'][:130])

assert not fail, "Some source excerpts did not match the retained official corpus; inspect evidence-audit.json"
