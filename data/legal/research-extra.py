from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from lxml import html
import subprocess,json,re
meta={'przetarg':('2021/2213','Rozporządzenie Rady Ministrów z dnia 14 września 2004 r. w sprawie sposobu i trybu przeprowadzania przetargów oraz rokowań na zbycie nieruchomości'),'oc':('2019/805','Rozporządzenie Ministra Finansów z dnia 26 kwietnia 2019 r. w sprawie obowiązkowego ubezpieczenia odpowiedzialności cywilnej przedsiębiorcy prowadzącego działalność w zakresie czynności rzeczoznawstwa majątkowego'),'zabytki':('2024/1292','Ustawa z dnia 23 lipca 2003 r. o ochronie zabytków i opiece nad zabytkami'),'geologia':('2024/1290','Ustawa z dnia 9 czerwca 2011 r. – Prawo geologiczne i górnicze')}
def download(item):
 key,(ref,title)=item;p=Path('data/legal/sources/owner-'+key+'.html')
 subprocess.run(['curl','-fLsS','--retry','2','--max-time','30','https://eli.gov.pl/api/acts/DU/'+ref+'/text.html','-o',str(p)],check=True)
 tree=html.fromstring(p.read_text());text=re.sub(r'\s+',' ',tree.text_content()).strip();p.with_suffix('.txt').write_text(text)
 units={}
 for el in tree.xpath('//*[@data-id]'):
  did=el.get('data-id');txt=re.sub(r'\s+',' ',el.text_content()).strip()
  if did.startswith('arti_') or did.startswith('para_'):units[did]={'text':txt,'anchor':el.get('id')}
 return key,{'ref':ref,'title':title,'text':text,'units':units}
with ThreadPoolExecutor(max_workers=4) as pool:out=dict(pool.map(download,meta.items()))
Path('data/legal/sources/owner-corpus.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for k,v in out.items():
 print(k,[(id,u['text'][:100]) for id,u in v['units'].items() if any(t in u['text'].lower() for t in ['postąpien','wadium','dzień rozpoczęcia','nie później','własnością górniczą','formami ochrony'])][:15])
