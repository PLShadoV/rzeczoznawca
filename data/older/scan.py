import json,re
F=json.load(open('final_text.json'))
pat=[(r'\bOdp\b|\bPyt\b|Odp\.','odp'),(r'(?<=[a-ząćęłńóśźż,] )[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+','cap'),(r'\s{2,}','2sp'),(r'(?<![\w\-/])[b-hj-npr-tvxył](?![\w.\-/*=])','1ch'),(r'[|\[\]{}_$#@<>«»„”©®]','sym'),(r'[a-ząćęłńóśźż][A-ZĄĆĘŁŃÓŚŹŻ]','mix'),(r'\d[a-ząćęłńóśźż]{2,}','dl'),(r'(?<!m\.in)[;:,.]{2,}','pp')]
ALLOWCAP=set('Skarbu Skarb Państwa Ministrów Rady Rada Prezesa Prezes GUS Lasów Lasy Państwowych Państwowe Prawo Prawa Kodeks Kodeksem Rzeczypospolitej Polskiej Polska Gminy Gmina Spółdzielni Spółdzielnia Mieszkaniowej Komisja Odpowiedzialności Zawodowej Agencja Mienia Wojskowego Krajowy Ośrodek Wsparcia Rolnictwa Zasobu Własności Rolnej Dyrektor Generalny Regionalnej Dyrekcji Wód Polskich Ministra Minister Rozwoju Wsi Środowiska Infrastruktury Sejmu Urzędu Geodezji Kartografii Głównego Specjalnej Strefy Rewitalizacji Wojewoda Interpretacyjnej Noty Federację Stowarzyszeń Rzeczoznawców Majątkowych Federacji Polską Biuletynu Urząd Mieszkalnictwa Miast Prezes Banku Centralnego Rozporządzeniem Rozporządzenia Rozporządzeniu Dziale Dział Inwestycji Ustawą Ustawy Konstytucja Państwowego Gospodarstwa Leśnego Regionalnego Zarządu Gospodarki Wodnej Izba Księgi Wieczystej Radę Radzie Jednostki Specjalnej Wojewódzkiego Krajowej Rady Najwyższa Izby Zabytków'.split())
for k,r in F.items():
    for f,t in zip('qabc',[r['q']]+r['o']):
        for p,name in pat:
            for m in re.finditer(p,t):
                if name=='cap' and m[0] in ALLOWCAP: continue
                print(k,f,name,'|',t[max(0,m.start()-30):m.end()+30]);break
