import runpy,json
from pathlib import Path
b=Path(__file__).parent
v=runpy.run_path(str(b/'valuation-map.py')); citation=v['citation']
qs=json.load(open(b/'domains/law-questions.json')); prior=json.load(open(b/'domains/law-citations.json'))
m={}
def reg(ids,old,new,key=''):
 for i in map(int,ids.split()):m[i]=(str(old),str(new),key)
reg('0',54,70)
reg('2 181',17,19)
reg('19',36,49,'stan nieruchomości')
reg('21',5,5,'rażąco')
reg('46',8,10)
reg('69 287',21,26,'zużycia')
reg('85',28,42,'Jeżeli nieruchomość gruntowa')
reg('103 263 613 759',56,79,'opis stanu')
reg('129 354',None,84)
reg('160',7,10,'udziałowi')
reg('212',34,43)
reg('237',23,28)
reg('239',44,65,'Przy stosowaniu podejścia dochodowego')
reg('419 715',None,54,'Rzeczoznawca majątkowy wskazuje')
reg('454 614',23,28,'Technikę wskaźnikową')
reg('681 186',26,3,'Rodzaj rynku')
reg('211',None,5,'Ceny uzyskiwane przy sprzedaży')
reg('757',5,None,'nie odbiegają o więcej niż 20%')
# Verified high-level provisions supplementary to regulation citations.
ug={679:(155,'Przy szacowaniu','ust. 1 i 3'),683:(107,'Terminy i sposób','ust. 3')}
out=json.load(open(b/'valuation-extra.json')) if (b/'valuation-extra.json').exists() else {}
for i,q in enumerate(qs):
 for o in q['occurrences']:
  if prior[o['id']]['status']!='unresolved':continue
  if i in m:
   old,new,k=m[i];a='new' if o['session']>='2023-09-09' else 'old'; n=new if a=='new' else old
   if n=='None':continue
   r={'status':'cited','citations':[citation(a,n,k)]}
   if i in [419]:r['note']='Przepis nakazuje wskazać obszary ryzyka. Nie nakazuje rzeczoznawcy zastępowania oceny ryzyka kredytowego dokonywanej przez wierzyciela.'
   out[o['id']]=r
  elif i in ug:
   n,k,d=ug[i];out[o['id']]={'status':'cited','citations':[citation('ugn',n,k,d)]}
  elif i in [48,87,163]:out[o['id']]={'status':'nonlegal','citations':[],'note':'Szczegółowa odpowiedź wynika z metodyki wyceny lub kosztorysowania; nie przypisano jej arbitralnie przepisu ustawy.'}
json.dump(out,open(b/'valuation-extra.json','w'),ensure_ascii=False,indent=2)
print('Supplemental law mappings:',len(out))
