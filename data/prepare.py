import fitz,json,re,pathlib
root=pathlib.Path(__file__).parent
sources=json.loads((root/'sources.json').read_text())
allq=[];sessions=[]
def clean(t):return re.sub(r'\s+',' ',t).replace('\xad','-').replace(';',';').strip()
def category(t,n):
 t=t.lower()
 if any(x in t for x in ['lasu','leśn','drzewostan','drewna','roln','żyta','upraw','plantac','siedlisk']):return 'Rolnictwo i leśnictwo'
 if any(x in t for x in ['ewidenc','geodez','rozgranicz','planowania','planowani','planu miejscow','planem miejscow','zagospodarowania przestrzen','warunkach zabudowy','lokalizacji inwestycji']):return 'Planowanie i geodezja'
 if n<=9 or any(x in t for x in ['prawo budowlane','strop','fundament','kondygnac','budowlanych']):return 'Budownictwo'
 if n<=18 or any(x in t for x in ['rachunkowo','inflac','rynk','ekonom','kapitał','statyst','warianc','odchylen','korelac'] ) and n<19:return 'Ekonomia i finanse'
 if any(x in t for x in ['wycen','wartoś','podejści','operat','kapitaliz','dyskont','porównywan','ceny średniej','zużyci','kosztów odtworzenia','dochod']):return 'Wycena nieruchomości'
 return 'Prawo i gospodarka nieruchomościami'
for date in sorted({k[:10] for k in sources if not k.startswith('2026-10')},reverse=True):
 keys={}
 doc=fitz.open(root/(date+'-key.pdf'))
 for page in doc:
  words=page.get_text('words');draw=page.get_drawings()
  marks=[d['rect'] for d in draw if d['fill']==(1.,1.,1.) and 6<d['rect'].width<11 and 6<d['rect'].height<11]
  for w in words:
   if not w[4].isdigit() or not 1<=int(w[4])<=90:continue
   x0,y0,x1,y1=w[:4]
   if not 70<x0<335 or not 125<y0<710:continue
   k=int(w[4]);ans=[]
   for r in marks:
    if x1<r.x0<x1+100 and abs(r.y0-y0)<3:
     col=round((r.x0-x1-31.5)/24)
     if 0<=col<=2:ans.append(col)
   if ans:keys[k]=sorted(set(ans))
 assert set(keys)==set(range(1,91)),(date,len(keys),set(range(1,91))-keys.keys())
 text=(root/(date+'-test.txt')).read_text()
 lines=[l for l in text.splitlines() if not any(x in l for x in ['EGZAMIN NA UPRAWNIENIA','RZECZOZNAWCY MAJ','Część pisemna przeprowadzona','Proszę nie zaznaczać']) and not re.fullmatch(r'(?:(?:EGZAMIN|NA|UPRAWNIENIA|ZAWODOWE)\s*)+',l.strip())]
 text=re.sub(r'Strona \d+ z \d+','','\n'.join(lines))
 parts=re.split(r'\bPyt\s+(\d+)\s+',text)[1:]
 assert len(parts)==180,(date,len(parts))
 for i in range(0,len(parts),2):
  n=int(parts[i]);body=parts[i+1];a=re.split(r'Odp\.\s*([abc])\s+',body)
  assert len(a)%2==1,(date,n,a)
  choices={}
  for j in range(1,len(a),2):
   label,value=a[j],clean(a[j+1])
   assert label not in choices or choices[label]==value,(date,n,'conflicting duplicate option',label)
   choices[label]=value
  assert set(choices)==set('abc'),(date,n,a)
  options=[choices[label] for label in 'abc']
  q={'id':date+'-'+str(n),'number':n,'session':date,'question':clean(a[0]),'options':options,'correct':keys[n],'category':category(clean(a[0]),n),'source':'https://www.gov.pl/attachment/'+sources[date+'-test'],'keySource':'https://www.gov.pl/attachment/'+sources[date+'-key']}
  assert all(options) and q['question'],q
  allq.append(q)
 sessions.append({'date':date,'count':90,'source':'https://www.gov.pl/attachment/'+sources[date+'-test'],'keySource':'https://www.gov.pl/attachment/'+sources[date+'-key']})
pathlib.Path('dist/questions.json').write_text(json.dumps({'questions':allq,'sessions':sessions},ensure_ascii=False))
print('Questions:',len(allq),'Sessions:',len(sessions))
assert len({q['id'] for q in allq})==len(allq)
print('September first 25:', [''.join('ABC'[i] for i in q['correct']) for q in allq[:25]])
