import json,re,collections
from pathlib import Path
BASE=Path(__file__).parent
qs=json.load(open(BASE/'domains/valuation-questions.json'))
ps=json.load(open(BASE/'sources/valuation-provisions.json'))
ACTS={'old':'Rozporządzenie Rady Ministrów z dnia 21 września 2004 r. w sprawie wyceny nieruchomości i sporządzania operatu szacunkowego','new':'Rozporządzenie Ministra Rozwoju i Technologii z dnia 5 września 2023 r. w sprawie wyceny nieruchomości','ugn':'Ustawa z dnia 21 sierpnia 1997 r. o gospodarce nieruchomościami','zabug':'Ustawa z dnia 8 lipca 2005 r. o realizacji prawa do rekompensaty z tytułu pozostawienia nieruchomości poza obecnymi granicami Rzeczypospolitej Polskiej'}
# Explicit topic groups reviewed against question text and marked answers. Each old/new
# pair is a checked substantive provision, not a keyword-inferred paragraph number.
maps={}; notes={}; theoretical=set()
def put(ids,old,new=None,key='',note=''):
 for i in map(int,ids.split()):
  maps[i]=('reg',str(old),str(new if new is not None else old),key)
  if note:notes[i]=note
def law(ids,num,key='',detail=''):
 for i in map(int,ids.split()): maps[i]=('ugn',str(num),detail,key)
def zlaw(ids,num,key='',detail=''):
 for i in map(int,ids.split()): maps[i]=('zabug',str(num),detail,key)
def theory(ids): theoretical.update(map(int,ids.split()))
put('4 19 268 383 399',1,1)
put('457 558',36,49)
put('5 14 37 79 199 219 340 380 381 508 569',8,10)
put('6 134 143 162 165 261 384 415 475 503 527 634',10,12)
put('306 336 386 539 560',10,12,'liczba lat')
put('354 416 619',10,12,'Stopę dyskontową')
put('192 372',12,14,'bezpiecznych')
put('53 74 239 264 284 321 346 396 405 440 446 463 466 497 498 516 532 562 31',9,11)
put('91 121 208 324',10,12,note='Wynik rachunku wynika z definicji wartości rezydualnej i kapitalizacji dochodu; dane liczbowe pochodzą z zadania.')
put('10 34 140 273 357 548',4,8,'Przy metodzie korygowania ceny średniej')
put('341 637',4,7)
put('8 103',4,8,'Przy metodzie porównywania parami',note='Przepis określa porównywanie cech i korektę cen; sposób uśredniania skorygowanych cen stanowi element metodyki wyceny.')
put('11 145 159 238 247 378 413 483 583',29,30,'R -')
put('17 71 109 136 183 188 281 325 351 481 618',29,30)
put('83 123',27,29)
put('12 36 605',23,28,'koszty opracowania dokumentacji',note='Przepis uzasadnia uwzględnienie dokumentacji i nadzoru. Szczegółowa kalkulacja lokalnych cen jest elementem metodyki kosztorysowej.')
put('55 78 344 369 370',20,25)
put('255',22,27,'Przy metodzie kosztów zastąpienia')
put('494 453',22,27,'Przy metodzie kosztów odtworzenia')
put('241',23,28,'Technikę wskaźnikową')
put('501',23,28,'koszty opracowania dokumentacji')
put('15 101 117 132 240 293 312 337 377 431 588 622',49,47)
put('16 304',54,70)
put('18 43 182',33,69,note='Przepis dotyczy określenia wartości budynków i urządzeń stanowiących odrębny przedmiot własności; przypadki wyceny odtworzeniowej określa również art. 150 ust. 3 UGN.')
put('20 45 154 278',None,3,'oględzin')
put('25 366 582 617',36,49,'lokalnego i regionalnego')
put('26 50 150 155 294 367 385 412 524 620',17,19)
put('27',None,31,'rodzaj i cel')
put('32 112 146 269 371 515 520',32,68)
put('38 76 166 272 302 330 449 541',34,43)
put('41 47 206 221 237 251 288 480',45,63)
put('42 161 420 586 593',44,65)
put('46 49 99 106 630',58,83)
put('52 181 245 316 626',52,45)
put('60 100 124 170 172 200 202 277 333 374 417',15,16)
put('61',23,28,'dokumentacji',note='Przepis wskazuje koszty dokumentacji i nadzoru; wymienione szczegółowe rodzaje dokumentacji należą do metodyki kosztorysowania.')
put('72 129 217 232',56,79,'Do operatu',note='Dokument ubezpieczenia stanowi załącznik do operatu albo umowy zgodnie z art. 175 ust. 4a UGN. Przepis rozporządzenia określa istotne dokumenty dotyczące wycenianej nieruchomości.')
put('75 432 435',47,67)
put('80 110 142 270',26,3,note='Przepis uzasadnia rozszerzenie obszaru rynku; możliwość wyceny dochodowej przy znanych dochodach wynika dodatkowo z przepisów o podejściu dochodowym.')
put('90',36,49,'drodze umowy')
put('94 359 485',None,39)
put('95',None,41)
put('108 147 259 465 551',16,18)
put('201',16,17,'różnicę')
put('111 211 303 309 373',7,10)
put('125',33,None)
put('130 222 409 464 628',46,66)
put('131 163 285 493 598',40,35)
put('149',47,67,'przed eksploatacją')
put('164 21 592 533 540',36,49)
put('169 567',44,65,note='Przepis wskazuje odrębnie wycenę zabytków w podejściu porównawczym i dochodowym; wybór zależy od danych i celu wyceny (art. 154 ust. 1 UGN).')
put('176 225 318 391',7,10,'Metodę zysków')
put('193 226 242 262 298 335 348 356 418 437 502 512 547 565 579 596 623',28,42)
put('205 594',43,75)
put('218 338 492 549',11,13)
put('228 299 428 456 496 529 616 627 67',36,49)
put('236 382 460',38,34)
put('243 387',21,26)
put('249',None,64)
put('266 434 531 621',35,72)
put('287 525',24,74)
put('328',None,36)
put('343 444 488',36,49,note='Wskazano przepis wykonawczy dotyczący wyceny drogowej. Przepis odsyła do UGN oraz ustawy z 10 kwietnia 2003 r. o szczególnych zasadach przygotowania i realizacji inwestycji w zakresie dróg publicznych.')
put('347 544',46,66,note='Przepisy szczegółowe znajdują się także w sąsiednim paragrafie dotyczącym złóż niestanowiących własności górniczej.')
put('363',None,38)
put('368 591 538',56,79,'opis stanu')
put('401 467 523',25,48)
put('452',56,79,'dat istotnych')
put('459 546',44,65,'Przy stosowaniu podejścia dochodowego')
put('476',None,6)
put('528 611',56,79,'pełnych złotych')
put('608',4,5)
# UGN: relevant statutes were read from official ELI full text.
law('13',151,'Wartość odtworzeniowa','ust. 2')
law('22 292',67,'jeżeli drugi przetarg','ust. 2 pkt 4')
law('24 122',4,'nieruchomości podobnej','pkt 16')
law('29 104 308 451 474 482',153,'Ceny te koryguje','ust. 1')
law('30 472',151,'Wartość rynkową','ust. 1')
law('33 98 339 421 606',152,'Przy zastosowaniu podejścia','ust. 3')
law('35 191 404 522',149)
law('39 58 73 310 379 563 568 349',154,'Wyboru','ust. 1')
law('44 490',68,'Przepisu ust. 2 nie stosuje','ust. 2a pkt 1')
law('59',156,'Operat szacunkowy może być wykorzystywany do celu','ust. 3')
law('62 570',134,'Podstawę ustalenia wysokości','ust. 1')
law('64 119 137 153 178 212 227 253 291 407 517 550 574 581 625', '98a')
law('65 156',146,'Wysokość opłaty','ust. 2')
law('68 252',175,'Przedsiębiorca prowadzący','ust. 4')
law('69 376',68,'Jeżeli nabywca','ust. 2')
law('115 635',150,'Określenia wartości','ust. 5')
law('141 197',155,'Przy wycenie nieruchomości na potrzeby','ust. 4')
law('148 311 576',4,'wycenie nieruchomości','pkt 6')
law('171 559',153,'Podejście dochodowe','ust. 2')
law('177 469',4,'wycenie nieruchomości','pkt 6 i 8')
law('195 603',134,'Przy określaniu wartości','ust. 2')
law('198 470 632',145)
law('203 216 553 597',157)
law('204 500 595 97 320',153,'Podejście kosztowe','ust. 3')
law('210 297 358 439 535 600',150)
law('214 224 461 599 168 580',4,'określaniu wartości','pkt 6a')
law('229 447 3',140,'W razie zmniejszenia','ust. 4')
law('248 427 458 93 257 301',146)
law('487 572',77)
law('296',156,'Rzeczoznawca majątkowy sporządza','ust. 1')
law('443',67,'cenę wywoławczą w drugim','ust. 2 pkt 2')
law('445',68,'Cenę nieruchomości lub jej części wpisanych','ust. 3')
law('450',None)
law('495 275',130)
law('499',135)
law('543',153,'Podejście kosztowe','ust. 3')
# Reparation statute, official consolidated text (Dz.U.2017 poz.2097).
zlaw('0',11,'Za porównywalne województwa','ust. 1–2')
zlaw('144 604',11,'W przypadku braku cen transakcyjnych','ust. 4')
zlaw('194',11,'Wartość nieruchomości stanowiących lasy','ust. 3')
zlaw('394 601',13,'Zaliczenia wartości','ust. 2')
zlaw('438',11,'według stanu na dzień','ust. 5')
zlaw('578',11)
# Not directly prescribed by a specific legal provision: theory, arithmetic and
# technical cost estimating. These are not represented as guessed statutory bases.
theory('1 7 9 40 48 56 57 66 77 81 82 107 126 128 139 167 173 184 187 189 190 207 220 223 230 233 234 239 246 254 256 258 260 263 265 267 271 276 280 286 289 295 305 307 314 315 317 323 331 332 334 345 350 355 360 361 388 395 397 400 402 408 419 423 425 433 436 455 473 478 486 504 505 507 511 513 514 519 521 537 556 561 564 587 589 590')
# Remove theoretical numbers that are governed explicitly by a formula provision.
theoretical-=set(maps)

# Additional individually reviewed provisions.
put('84',44,65)
put('85',4,5)
put('86',7,10,'Metodę zysków')
put('89',36,49,'lokalnego i regionalnego')
zlaw('87',11,'według stanu na dzień','ust. 5')
theory('88 105 555')
law('92',164,'Podstawą','ust. 1')
law('113',161,'Wartość katastralną','ust. 2')
law('133',151,'Wartość katastralną','ust. 3')
law('186 462',170,'Organ prowadzący','ust. 1')
law('235',170,'mogą być aktualizowane','ust. 4')
law('322',131,'Różnicę','ust. 4')
law('290',107,'Terminy i sposób','ust. 3')
law('403',167,'wykazuje się w tabelach','ust. 2')
law('429',165)
law('448',148,'Na poczet opłaty','ust. 4')
law('326 454',178,'Wobec rzeczoznawcy','ust. 2 pkt 1 i 5')
put('51 135',None,54,'Rzeczoznawca majątkowy wskazuje')
put('282 430',4,4)
put('573',26,3,'Rodzaj rynku')
put('566',6,9)
put('450',38,51,'dożywocia')
put('518',18,20)
# Use statutory general provisions for legal purpose questions, with specific context notes.
law('2',152,'Przy zastosowaniu podejścia','ust. 3')
law('250',144,'użytkownicy wieczyści','ust. 2')
# Corrections after comparing the exact 2023 provision to the former rule.
for i in [18,43,182]:
 maps[i]=('ugn','150','ust. 3','Wartość odtworzeniową'); notes.pop(i,None)
for i in [164,21,592,533,540]:maps[i]=('ugn','134','ust. 3–4','Wartość nieruchomości dla celów odszkodowania')
for i in [12,36,605,501]:
 a,n,nn,k=maps[i]; maps[i]=(a,n,nn,'dokumentacji')
for i in [354,416,619]:maps[i]=('reg','10','12','ryzyko')
maps[27]=('reg','None','31','rodzaj obciążenia')
maps[452]=('reg','56','79','dat')
# These keys do not directly support all marked choices; retain them for further review.
for i in [218,492,549,352,530,102,459,476]: maps.pop(i,None)
for i in [57,77,315,332,397,419,555,587]:
 maps[i]=('reg','None','6','Cechy rynkowe'); theoretical.discard(i)
 notes[i]='Przepis określa badanie wpływu cech rynkowych. Szczegółowe pozyskiwanie opinii o preferencjach nabywców stanowi element metodyki analizy rynku.'

# Reuse official primary-source extracts fetched by the law/economics researchers.
aux=json.load(open(BASE/'sources/law-corpus.json'))
for a in ['sd','pcc','kc','kpa']:
 ACTS[a]=aux[a]['title']
 for number,p in aux[a]['articles'].items():
  ps.append({'act':a,'id':p['anchor'],'text':p['text'],'url':f"https://eli.gov.pl/api/acts/DU/{aux[a]['ref']}/text.html#"+p['anchor']})
for p in json.load(open(BASE/'sources/economics-corpus.json')):
 if p['act'] in ['accounting','cit']:ps.append(p)
ACTS['accounting']='Ustawa z dnia 29 września 1994 r. o rachunkowości'
ACTS['cit']='Ustawa z dnia 15 lutego 1992 r. o podatku dochodowym od osób prawnych'
def auxlaw(ids,act,n,key='',detail=''):
 for i in map(int,ids.split()):maps[i]=(act,str(n),detail,key); theoretical.discard(i)
auxlaw('23 313','sd',7,'Podstawę opodatkowania','ust. 1')
auxlaw('174 319','sd',8,'Wartość rynkową rzeczy','ust. 3')
auxlaw('489','sd',13,'Roczną wartość','ust. 3')
# Q96 says total value of easement but the 4% formula is annual; leave unresolved.
auxlaw('414 602','sd','4a','Zwalnia się','ust. 1')
auxlaw('410 534','pcc',6,'Wartość rynkową przedmiotu','ust. 1 pkt 1 i ust. 2')
auxlaw('63 362 585','kc',231,'Właściciel gruntu','§ 2')
auxlaw('389','kc',925)
auxlaw('213','kpa',17,'w stosunku do organów jednostek','pkt 1')
auxlaw('554 629','kpa',75,'Jako dowód','§ 1')
auxlaw('48','accounting',28,'Za wartość godziwą','ust. 6')
auxlaw('185','accounting',29,'Jeżeli założenie kontynuacji','ust. 1')
auxlaw('116 442','cit','16g','Za wartość początkową','ust. 1 pkt 1–3')
auxlaw('160','cit',14,'Wartość rynkową','ust. 2')
# Specific verified theories are retained as non-statutory methodology throughout.
for i in [57,77,315,332,397,419,555,587,104,308]:
 maps.pop(i,None); theoretical.add(i)
# Independent QA fixes: match the actual marked options and state methodological limits.
maps[36]=('reg','23','28','Przy użyciu techniki szczegółowej')
notes[36]='Przepis określa ilość robót i ceny jednostkowe. Obmiar oraz dobór lokalnych cen stanowią sposób ustalenia tych danych w metodyce kosztorysowej.'
notes[605]='Przepis wymaga uwzględnienia dokumentacji i nadzoru. Nie ustanawia reguły mnożnika regionalnego; mnożnik jest narzędziem metodyki kosztorysowej i specjalistycznych wydawnictw.'
# Final audit: avoid carrying a repealed paragraph number into the new regulation.
maps[125]=('reg','33','None','')
for i in [18,43,182]:maps[i]=('reg','33','None','wartość odtworzeniową')
for i in [179,279,342]:maps[i]=('reg','None','5','rynkowy charakter')
for i in [426,613]:maps[i]=('reg','18','21','dt')
for i in [114,392,631]:maps.pop(i,None)
# The date of the decision in Q530 conflicts with the general compensation-date rule.
# It intentionally remains unresolved above.

# Build direct excerpts from the verified provision text; no invented text.
def citation(act,n,key='',detail=''):
 suffix=('-para_' if act in ['old','new'] else 'arti_')+str(n)
 cand=[p for p in ps if p['act']==act and (p['id'].endswith(suffix) or p['id']==suffix)]
 if not cand:raise ValueError((act,n))
 p=max(cand,key=lambda p:len(p['text']))
 text=p['text']; start=text.lower().find(key.lower()) if key else 0
 if start<0:start=0
 if start>0:
  # Keep a complete sentence around matching terms rather than an isolated suffix.
  boundaries=list(re.finditer(r'\. (?=[A-ZĄĆĘŁŃÓŚŹŻ])',text[:start]))
  if key not in ['R -']:
   start=boundaries[-1].end() if boundaries else 0
 evidence=text[start:start+490]
 if len(text)>start+490:evidence=evidence.rsplit(' ',1)[0]+'…'
 out={'act':ACTS[act],'provision':('§ ' if act in ['old','new'] else 'art. ')+str(n)+((' '+detail) if detail else ''),'url':p['url'],'evidence':evidence}
 if act=='old':out['note']='Historyczne rozporządzenie; przytoczono urzędowy tekst jednolity z 2021 r. (Dz.U. poz. 555).'
 return out
out={}
for i,q in enumerate(qs):
 for occ in q['occurrences']:
  rec={'status':'unresolved','citations':[],'note':'Nie potwierdzono jeszcze szczegółowej podstawy prawnej dla wskazanych odpowiedzi; wymaga dalszej weryfikacji.'}
  if i in theoretical:rec={'status':'nonlegal','citations':[],'note':'Pytanie dotyczy metodyki, obliczeń lub wiedzy technicznej/ekonomicznej. Nie przypisano mu przepisu ustawy jako źródła szczegółowej odpowiedzi.'}
  if i in maps:
   a,n,new,key=maps[i]
   if a=='reg':
    a='new' if occ['session']>='2023-09-09' else 'old'; n=new if a=='new' else n; detail=''
   else:detail=new
   if n!='None':
    rec={'status':'cited','citations':[citation(a,n,key,detail)]}
    if i in notes:rec['note']=notes[i]
  if rec['status']=='cited':
   # Supporting provisions for questions with several directly statutory elements.
   extras=[]
   if i==4:
    extras.append(('new',5,'Na podstawie znajomości cen transakcyjnych','ust. 2'))
    extras.append(('new',5,'Do zbioru nieruchomości podobnych','ust. 4–6'))
   if i in [19,399]:
    era='new' if occ['session']>='2023-09-09' else 'old'
    extras.extend([(era,49 if era=='new' else 36,'Wartość rynkową nieruchomości dla potrzeb','ust. 1'),(era,45 if era=='new' else 52,'Przy określaniu wartości','ust. 1–2'),(era,26 if era=='new' else 21,'Przy określaniu wartości odtworzeniowej','ust. 1–2')])
   if i in [72,129,217,232]:extras.append(('ugn',175,'Kopia dokumentu ubezpieczenia','ust. 4a'))
   if i in [91,121,208,324]:extras.append(('old' if occ['session']<'2023-09-09' else 'new',9 if occ['session']<'2023-09-09' else 11,'',''))
   if i in [172,333]:
    extras.extend([('old' if occ['session']<'2023-09-09' else 'new',20 if occ['session']<'2023-09-09' else 25,'','')])
   if i==172:extras.append(('old' if occ['session']<'2023-09-09' else 'new',7 if occ['session']<'2023-09-09' else 10,'',''))
   if i in [108,147,259] and occ['session']>='2023-09-09':extras.append(('new',17,'',''))
   if i==60:extras.extend([('old' if occ['session']<'2023-09-09' else 'new',16 if occ['session']<'2023-09-09' else 17,'',''),('old' if occ['session']<'2023-09-09' else 'new',17 if occ['session']<'2023-09-09' else 19,'','')])
   if i in [85,608]:extras.append(('ugn',155,'Przy szacowaniu','ust. 1'))
   if i==389:extras.append(('kc',924,'',''))
   if i==554:extras.append(('kpa',84,'Gdy w sprawie','§ 1'))
   if i in [326,454]:extras.append(('ugn','195a','Minister właściwy','ust. 1'))
   for aa,nn,kk,dd in extras:rec['citations'].append(citation(aa,nn,kk,dd))
  # The former regulation does not substantiate the special new-law answers.
  if occ['session']<'2023-09-09' and i in [17,71,136,183,325,51,135]:
   rec={'status':'unresolved','citations':[],'note':'Wskazane odpowiedzi wymagają odrębnej weryfikacji według regulacji i standardów obowiązujących w dacie historycznej sesji.'}
  if i in [96,102,352,459,530,630]:
   rec={'status':'unresolved','citations':[],'note':'Wskazane odpowiedzi lub ich zakres nie znajdują pełnego potwierdzenia w zweryfikowanym przepisie; potrzebne sprawdzenie treści pytania i stanu prawnego sesji.'}
  out[occ['id']]=rec
# Verified special cases from the official annex (pre-2023 only) and forestry act.
from lxml import html
oldtxt=re.sub(r'\s+',' ',html.fromstring(open(BASE/'sources/valuation-old.html').read()).text_content())
for ids,point,key in [('28 231 393',6,'Dla gruntów stanowiących zadrzewienia'),('614',5,'Dla gruntów pod stawami')]:
 start=oldtxt.index(key); end=oldtxt.find(str(point+1)+'. ',start)
 excerpt=oldtxt[start:end].strip()
 for i in map(int,ids.split()):
  for o in qs[i]['occurrences']:
   if o['session']<'2023-09-09':out[o['id']]={'status':'cited','citations':[{'act':ACTS['old'],'provision':f'Załącznik, pkt {point}','url':'https://eli.gov.pl/api/acts/DU/2021/555/text.html','evidence':excerpt[:490]}]}
lasy=open(BASE/'sources/rural-lasy.txt').read()
key='Jeżeli osobą uprawnioną jest emeryt lub rencista, cena nabycia lokalu ustalona jest na 5 % jego wartości.'
assert key in lasy
for i in [157,274]:
 for o in qs[i]['occurrences']:out[o['id']]={'status':'cited','citations':[{'act':'Ustawa z dnia 28 września 1991 r. o lasach','provision':'art. 40a ust. 4','url':'https://eli.gov.pl/api/acts/DU/2024/530/text.html','evidence':key}]}
json.dump(out,open(BASE/'domains/valuation-citations.json','w'),ensure_ascii=False,indent=2)
print(collections.Counter(x['status'] for x in out.values()))
print('Unresolved question indexes:',[i for i,q in enumerate(qs) if any(out[o['id']]['status']=='unresolved' for o in q['occurrences'])])
