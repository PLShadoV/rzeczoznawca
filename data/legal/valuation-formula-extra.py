"""Reviewed statutory-formula overrides; does not mutate primary domain files."""
import json,re
from pathlib import Path
b=Path(__file__).parent
ps=json.load(open(b/'sources/valuation-provisions.json'))
titles={'old':'Rozporządzenie Rady Ministrów z dnia 21 września 2004 r. w sprawie wyceny nieruchomości i sporządzania operatu szacunkowego','new':'Rozporządzenie Ministra Rozwoju i Technologii z dnia 5 września 2023 r. w sprawie wyceny nieruchomości'}
f=b/'valuation-extra.json';out=json.load(open(f));before=len(out)
def ref(era,n,ust,key=''):
 p=next(p for p in ps if p['act']==era and p['id'].endswith('-para_'+str(n)))
 t=p['text']; start=t.lower().find(key.lower()) if key else 0
 assert start>=0,(era,n,key)
 end=t.find(' '+str(ust+1)+'. ',start)
 excerpt=t[start:end if end>=0 else len(t)]
 if len(excerpt)>490:excerpt=excerpt[:480].rsplit(' ',1)[0]+'…'
 return {'act':titles[era],'provision':f'§ {n} ust. {ust}','url':p['url'],'evidence':excerpt}
added=[]
def assign(domain,ids,topic,note=''):
 qs=json.load(open(b/f'domains/{domain}-questions.json'))
 for i in ids:
  q=qs[i]
  for o in q['occurrences']:
   era='new' if o['session']>='2023-09-09' else 'old'
   if topic in ['cap','rv','payback']:
    n=11 if era=='new' else 9
    citations=[ref(era,n,3 if topic=='payback' else 1,'Współczynnik kapitalizacji odzwierciedla' if topic=='payback' else 'Przy użyciu techniki kapitalizacji prostej')]
    if topic=='rv':citations.append(ref(era,12 if era=='new' else 10,1,'Wartość rezydualna'))
   else:citations=[ref(era,12 if era=='new' else 10,1,'Przy użyciu techniki dyskontowania')]
   explanation=note or ('Wynik liczbowy jest wyprowadzeniem z zależności kapitalizacji określonej w przepisie. Dane liczbowe podano w zadaniu; przepis nie zawiera gotowej odpowiedzi liczbowej.')
   out[o['id']]={'status':'cited','citations':citations,'note':explanation};added.append(o['id'])
assign('valuation',[107],'cap','Przepis określa kapitalizację dochodu (60 000 zł × 10 = 600 000 zł). Ustalenie dochodu netto jako EDB minus wydatki operacyjne jest krokiem metodycznym rachunku dochodów; ten szczegół nie jest definicją ustawową.')
assign('valuation',[7],'dcf','Wniosek o wyższej wartości przy niższej stopie wynika matematycznie z dyskontowania dodatnich przyszłych dochodów, przy pozostałych danych niezmienionych. Przepis określa zasadę dyskontowania, nie wskazuje liczbowej odpowiedzi.')
assign('economics',[43,55,78,90,160,263],'cap')
assign('economics',[44,88,100,158,233,244,246],'rv')
assign('economics',[120,190],'payback','Przepis wprost określa współczynnik kapitalizacji jako okres zwrotu środków poniesionych na nabycie porównywalnych nieruchomości z uzyskiwanych dochodów.')
assign('building',[152],'rv')
assign('building',[153],'cap')
# Verified book-value formula from the official accounting act already retrieved.
a=next(p for p in json.load(open(b/'sources/economics-corpus.json')) if p['act']=='accounting' and p['number']=='28')
start=a['text'].index('środki trwałe oraz wartości niematerialne i prawne')
t=a['text'][start:start+700];end=t.index(';')+1
qs=json.load(open(b/'domains/valuation-questions.json'))
for o in qs[395]['occurrences']:
 out[o['id']]={'status':'cited','citations':[{'act':'Ustawa z dnia 29 września 1994 r. o rachunkowości','provision':'art. 28 ust. 1 pkt 1','url':a['url'],'evidence':t[:end]}],'note':'Wartość bilansowa uwzględnia pomniejszenie o amortyzację lub umorzenie. Przepis wymaga także uwzględnienia odpisów z tytułu trwałej utraty wartości, jeśli występują.'};added.append(o['id'])
json.dump(out,open(f,'w'),ensure_ascii=False,indent=2)
assert all(len(c['evidence'])>=20 for x in out.values() for c in x['citations'])
print('Added/reviewed',len(added),'occurrences; supplemental',before,'→',len(out))
print(added)
