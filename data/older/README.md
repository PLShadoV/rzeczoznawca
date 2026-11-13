# Archiwalne sesje 2020–2021 (skany)

4 pełne sesje: 25.06.2020, 30.07.2020, 24.09.2020 i 18.03.2021 (360 pytań). Sesje z lat 2018–2019 zostały odczytane tą samą metodą, ale w wersji 1.3.0 wycofano je z bazy (w `final_text.json` i `keys.json` nadal są surowe wyniki; `merge_into_dist.py` publikuje tylko sesje z `sources-older.json`). Ministerstwo opublikowało je jako **skany PDF z kluczem** (test + kratki klucza w jednym pliku), bez warstwy tekstowej. Linki do oryginałów: `sources-older.json` (pole `pdf`) i `list.txt`.

## Jak powstał tekst

1. `preprocess.py`, `preprocess4.py` — render stron (300 i 400 dpi), usunięcie poziomych linii i szumu marginesów.
2. Tesseract 5 (`pol`), trzy niezależne przebiegi → `parse.py` dzieli tekst na pytania (zawsze 90) i warianty a/b/c → `parsed_ocr*.json`.
3. `build.py` (+ `clean_text.py`, `autofix.json`) — dla każdego pola:
   - jeśli tekst jest identyczny z pytaniem z bazy 2021–2026 (różnice wyłącznie typu OCR, liczby muszą być identyczne) — przyjmowany jest czysty tekst z bazy;
   - w przeciwnym razie głosowanie słowo po słowie między trzema przebiegami OCR i korekta typowych pomyłek (l/i, ł/l, rn/m).
4. **Ręczna korekta** każdego pola, w którym przebiegi OCR się różniły, zawierało nieznane słowo albo liczby, z porównaniem do skanu — zapisana w `corr/<data>.txt` (`<nr> <pole> <tekst>`). Pola `corr/` mają pierwszeństwo przed automatem.
5. `assemble_older.py` → `final_text.json` (tekst końcowy).

## Klucze

`keys_detect.py` wykrywa kratki klucza na skanie (korekta przekosu, gęstość wypełnienia) → `keys.json`. Separacja zaznaczone/puste jest jednoznaczna we wszystkich kluczach (min. gęstość zaznaczenia ≥ 0,46, maks. pustej ≤ 0,03). Wynik porównano wzrokowo z obrazami kluczy.

Uwzględniono **oficjalne sprostowania** opublikowane przy arkuszach:
- 25.06.2020, pytanie 57 — prawidłowa odpowiedź b),
- 30.07.2020, pytanie 61 — prawidłowe odpowiedzi a), b) i c).

Pytania te mają w danych pole `keyNote` i link do sprostowania.

## Scalanie

`merge_into_dist.py` dołącza sesje do `dist/questions.json` (pole `archive: true` w `sessions`), stosuje korekty pisowni z `data/text_fixes.py`, a w warstwie przypisów i komentarzy kopiuje wpis z identycznego pytania z lat 2021–2026 (125 pytań). Pozostałe mają status „do weryfikacji” (`data/legal/archive-2018-2021.json`).

Robocze pliki (PDF-y, obrazy stron, surowy OCR) nie są w repozytorium — odtworzysz je z linków w `list.txt` (wymagane: PyMuPDF, OpenCV, Tesseract z językiem `pol`, hunspell `pl_PL`).

## Ograniczenia

Tekst pochodzi z OCR słabej jakości skanów (1 bit, ok. 170 dpi). Wszystkie pola z rozbieżnościami, liczbami i nieznanymi słowami sprawdzono ze skanem, ale pola zgodne we wszystkich trzech przebiegach OCR nie były porównywane znak po znaku. W razie wątpliwości rozstrzyga oryginalny PDF (link przy każdym pytaniu).
