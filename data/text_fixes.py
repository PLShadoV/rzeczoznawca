"""Editorial spelling corrections for question and answer text.

The ministry sheets contain typing errors (e.g. "tymczsowym", "brytto").
These fixes only correct spelling, missing Polish diacritics, doubled
letters and spacing around punctuation.  They never change the meaning of a
question or the official answer key.  Every applied change is logged in
data/text-corrections.json so the original wording stays traceable; the
original PDF is linked from each question (`source`).
"""
import re

# Whole-word replacements (case-sensitive, applied on word boundaries).
WORDS = {
    'nieruchomosci': 'nieruchomości', 'conajmniej': 'co najmniej', 'następujace': 'następujące',
    'budynkow': 'budynków', 'grunu': 'gruntu', 'majatkowych': 'majątkowych', 'majatkowego': 'majątkowego',
    'majatkowym': 'majątkowym', 'majatkowe': 'majątkowe', 'majztkowych': 'majątkowych', 'mąjątkowy': 'majątkowy',
    'przylegajacego': 'przylegającego', 'odpowiadajacej': 'odpowiadającej', 'pojedyńczego': 'pojedynczego',
    'zatwierdzajaca': 'zatwierdzająca', 'zawierdzająca': 'zatwierdzająca', 'zatwierdzajacej': 'zatwierdzającej',
    'oszkodowania': 'odszkodowania', 'nieruchomościamia': 'nieruchomościami', 'wszytkie': 'wszystkie',
    'warości': 'wartości', 'Warość': 'Wartość', 'watość': 'wartość', 'wartośc': 'wartość', 'brytto': 'brutto',
    'znaczniu': 'znaczeniu', 'przędsiębiorcy': 'przedsiębiorcy', 'zdefinioweane': 'zdefiniowane',
    'twałości': 'trwałości', 'dołaczony': 'dołączony', 'kapitalem': 'kapitałem', 'nieruchomośći': 'nieruchomości',
    'zarzadu': 'zarządu', 'monentu': 'momentu', 'zaokraglać': 'zaokrąglać', 'zaokragleniu': 'zaokrągleniu',
    'rzadowej': 'rządowej', 'szcunkowych': 'szacunkowych', 'skrygować': 'skorygować', 'własnosci': 'własności',
    'wpływajacych': 'wpływających', 'wpływajace': 'wpływające', 'uwzglednia': 'uwzględnia', 'uwględnia': 'uwzględnia',
    'uwzglednieniem': 'uwzględnieniem', 'uwzglednienia': 'uwzględnienia', 'uwzględniajacej': 'uwzględniającej',
    'wyjatkiem': 'wyjątkiem', 'przypadajacego': 'przypadającego', 'wycenianiej': 'wycenianej',
    'własciwy': 'właściwy', 'znajdujace': 'znajdujące', 'przyjnuje': 'przyjmuje', 'stosowac': 'stosować',
    'zagospodarownia': 'zagospodarowania', 'konkretenego': 'konkretnego', 'gospodrace': 'gospodarce',
    'aprecjajcja': 'aprecjacja', 'korygujacego': 'korygującego', 'miejsze': 'mniejsze', 'Akermana': 'Ackermana',
    'ksiegi': 'księgi', 'najpóżniej': 'najpóźniej', 'tymczsowym': 'tymczasowym', 'wynikajacych': 'wynikających',
    'wynikajacymi': 'wynikającymi', 'tejemnicy': 'tajemnicy', 'Vat': 'VAT', 'płyności': 'płynności',
    'obejmowac': 'obejmować', 'ostaniego': 'ostatniego', 'ostanim': 'ostatnim', 'ostanich': 'ostatnich',
    'podejscia': 'podejścia', 'podejscie': 'podejście', 'niestanowących': 'niestanowiących', 'stanowące': 'stanowiące',
    'budowalnego': 'budowlanego', 'budowalnych': 'budowlanych', 'rozporzadzeniu': 'rozporządzeniu',
    'rezydydualna': 'rezydualna', 'możliwosci': 'możliwości', 'NVP': 'NPV', 'obowiązujacej': 'obowiązującej',
    'ponadloklanych': 'ponadlokalnych', 'okreslić': 'określić', 'Katologu': 'Katalogu', 'szczególonych': 'szczególnych',
    'usankcjinowany': 'usankcjonowany', 'dotyczacych': 'dotyczących', 'dotyczacej': 'dotyczącej', 'dotyczace': 'dotyczące',
    'Maksymala': 'Maksymalna', 'ceters': 'ceteris', 'zobowiazaniu': 'zobowiązaniu', 'dopusza': 'dopuszcza',
    'wiecystym': 'wieczystym', 'zasilająch': 'zasilających', 'tyłułu': 'tytułu', 'zewoleniu': 'zezwoleniu',
    'konstrukcyne': 'konstrukcyjne', 'kapitalowego': 'kapitałowego', 'pierścnicy': 'pierśnicy',
    'odtworzniowa': 'odtworzeniowa', 'niepozostajacych': 'niepozostających', 'techniced': 'technice',
    'rachunkowosci': 'rachunkowości', 'rachunkowści': 'rachunkowości', 'odszkodwanie': 'odszkodowanie',
    'skladnika': 'składnika', 'upłyneło': 'upłynęło', 'zamknietym': 'zamkniętym', 'podlegajacego': 'podlegającego',
    'punktcie': 'punkcie', 'kleszczowgo': 'kleszczowego', 'Pomieszcenia': 'Pomieszczenia',
    'prowadzacego': 'prowadzącego', 'prowadzacej': 'prowadzącej', 'lini': 'linii', 'porośniete': 'porośnięte',
    'lesnej': 'leśnej', 'wynosza': 'wynoszą', 'urzadzenia': 'urządzenia', 'utrudniąjacej': 'utrudniającej',
    'połżonych': 'położonych', 'wieczystystego': 'wieczystego', 'mkieszkaniowej': 'mieszkaniowej',
    'wlaścicielu': 'właścicielu', 'bezpośrdeni': 'bezpośredni', 'przyleglej': 'przyległej', 'zmianu': 'zmiany',
    'polegajacej': 'polegającej', 'przedsiewzięcia': 'przedsięwzięcia', 'częsci': 'części', 'ęsci': 'ęści',
    'gospoodarstwa': 'gospodarstwa', 'wytycznie': 'wytyczenie', 'zwierzeta': 'zwierzęta', 'żyjace': 'żyjące',
    'Wskażnik': 'Wskaźnik', 'wskażnik': 'wskaźnik', 'zkres': 'zakres', 'popdejścua': 'podejścia',
    'pochodzace': 'pochodzące', 'stosujacej': 'stosującej', 'nieposiadajacym': 'nieposiadającym',
    'wwszystkich': 'wszystkich', 'pożytkii': 'pożytki', 'pojeciem': 'pojęciem', 'pojeciami': 'pojęciami',
    'przemyslowe': 'przemysłowe', 'wkaźniki': 'wskaźniki', 'koniuktury': 'koniunktury',
    'następujacych': 'następujących', 'następujacy': 'następujący', 'gruntemj': 'gruntem',
    'ustuowanego': 'usytuowanego', 'zezwalajacej': 'zezwalającej', 'sporzadzony': 'sporządzony',
    'zastapienia': 'zastąpienia', 'pozbawaienia': 'pozbawienia', 'przysłguje': 'przysługuje',
    'przezydent': 'prezydent', 'przeciętynych': 'przeciętnych', 'prawidłowści': 'prawidłowości',
    'likalu': 'lokalu', 'przejeciu': 'przejęciu', 'kwalifiakcji': 'kwalifikacji', 'odrebną': 'odrębną',
    'istniejace': 'istniejące', 'zycie': 'życie', 'neruchomości': 'nieruchomości', 'wyrażobnego': 'wyrażonego',
    'austryjackiej': 'austriackiej', 'wyłacznie': 'wyłącznie', 'przynaleznych': 'przynależnych',
    'obowązku': 'obowiązku', 'wynajmujacego': 'wynajmującego', 'zwiazanej': 'związanej', 'rocznnych': 'rocznych',
    'kutury': 'kultury', 'korzystniejszydla': 'korzystniejszy dla', 'zrid': 'ZRID',
    # Older (2018-2021) sheets
    'nieruchomosciami': 'nieruchomościami', 'wynikajacej': 'wynikającej', 'stanowiacego': 'stanowiącego',
    'stanowiacych': 'stanowiących', 'stanowiacą': 'stanowiącą', 'stanowiace': 'stanowiące', 'następujace': 'następujące',
    'posiadajacą': 'posiadającą', 'wchodzacych': 'wchodzących', 'występujacych': 'występujących', 'okreslić': 'określić',
    'własciwy': 'właściwy', 'uwzględniajacej': 'uwzględniającej', 'wynikajacych': 'wynikających', 'kapitalu': 'kapitału',
    'wieczysteco': 'wieczystego', 'Rzeczpospolitej': 'Rzeczypospolitej', 'okreslenie': 'określenie',
    'spoleczno': 'społeczno', 'wspołczynnika': 'współczynnika', 'skladowych': 'składowych',
}

# Phrase-level corrections (exact substrings).
PHRASES = {
    'osoba, kta posiadają dyplom': 'osoba, która posiada dyplom',
    'ale ukończyły studia podyplomowe': 'ale ukończyła studia podyplomowe',
    'gruntu leśnego wynie': 'gruntu leśnego wyniesie:',
    'rna obszarze zabudowy': 'na obszarze zabudowy',
    'W wzorze tym': 'We wzorze tym',
    'prze bobry': 'przez bobry',
    'okreslić': 'określić',
    'Właściwości użytkowe w budownictwie"': 'Właściwości użytkowe w budownictwie"',
}


def fix_text(t):
    orig = t
    for a, b in PHRASES.items():
        t = t.replace(a, b)
    t = re.sub(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+', lambda m: WORDS.get(m[0], m[0]), t)
    # unify typographic quotes
    t = t.replace('„', '"').replace('”', '"').replace('“', '"')
    # spacing around punctuation
    t = re.sub(r'(?<=\S)\s+([,;:?!])', r'\1', t)
    t = re.sub(r'\(\s+', '(', t)
    t = re.sub(r'\s+\)', ')', t)
    t = re.sub(r',(?=[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ])', ', ', t)
    t = re.sub(r'\.{2}$', '.', t)
    t = re.sub(r'\s{2,}', ' ', t).strip()
    return t
