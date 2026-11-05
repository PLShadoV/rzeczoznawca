from html.parser import HTMLParser
from pathlib import Path
import re,json,concurrent.futures,subprocess,fitz
MONTHS={'marca':'03','kwietnia':'04','maja':'05','czerwca':'06','lipca':'07','września':'09','października':'10','listopada':'11','grudnia':'12'}
new={}
class Parser(HTMLParser):
 def handle_starttag(self,t,a):
  if t=='a':self.href=dict(a).get('href','');self.text=''
 def handle_data(self,d):self.text=getattr(self,'text','')+d
 def handle_endtag(self,t):
  if t!='a' or 'attachment' not in getattr(self,'href',''):return
  text=self.text.lower();m=re.search(r'(\d+) ('+'|'.join(MONTHS)+r') (202[1-4])',text)
  if m and ('test z dnia' in text or 'klucz odpowiedzi' in text):
   date=m[3]+'-'+MONTHS[m[2]]+'-'+m[1].zfill(2)
   new[date+('-key' if 'klucz odpowiedzi' in text else '-test')]=self.href.split('/')[-1]
Parser().feed(Path('data/gov.html').read_text())
dates={k[:10] for k in new};paired={d for d in dates if d+'-test' in new and d+'-key' in new};new={k:v for k,v in new.items() if k[:10] in paired}
print('Older complete sessions:',len(paired),sorted(paired),flush=True)
def get(item):
 k,v=item;pdf=Path('data/'+k+'.pdf');txt=pdf.with_suffix('.txt')
 if pdf.exists() and txt.exists():return k
 temp=pdf.with_suffix('.part')
 subprocess.run(['curl','-fLsS','--retry','3','--max-time','60','https://www.gov.pl/attachment/'+v,'-o',str(temp)],check=True)
 doc=fitz.open(temp,filetype='pdf');assert len(doc)>0;doc.close();temp.replace(pdf)
 subprocess.run(['pdftotext','-layout',str(pdf),str(txt)],check=True)
 return k
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for k in pool.map(get,sorted(new.items())):print('Downloaded:',k,flush=True)
items=json.loads(Path('data/sources.json').read_text());items.update(new);Path('data/sources.json').write_text(json.dumps(items,indent=2))
