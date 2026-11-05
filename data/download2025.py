from html.parser import HTMLParser
import re,json,urllib.request,concurrent.futures,subprocess
months={'marca':'03','maja':'05','czerwca':'06','września':'09','października':'10','listopada':'11'}
items=json.load(open('data/sources.json'));new={}
class P(HTMLParser):
 def handle_starttag(self,t,a):
  if t=='a':self.href=dict(a).get('href','');self.text=''
 def handle_data(self,d):self.text=getattr(self,'text','')+d
 def handle_endtag(self,t):
  if t!='a' or 'attachment' not in getattr(self,'href',''):return
  t=self.text.lower();m=re.search(r'(\d+) (marca|maja|czerwca|września|października|listopada) 2025',t)
  if m and ('test z dnia' in t or 'klucz odpowiedzi' in t):
   date='2025-'+months[m[2]]+'-'+m[1].zfill(2);new[date+('-key' if 'klucz' in t else '-test')]=self.href.split('/')[-1]
P().feed(open('data/gov.html').read())
def get(item):
 k,v=item
 if __import__('pathlib').Path('data/'+k+'.txt').exists():return k
 urllib.request.urlretrieve('https://www.gov.pl/attachment/'+v,'data/'+k+'.pdf');subprocess.run(['pdftotext','-layout','data/'+k+'.pdf','data/'+k+'.txt'],check=True);return k
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for k in pool.map(get,new.items()):print(k)
items.update(new);json.dump(items,open('data/sources.json','w'))
