# Kontrola wydania 1.3.0

## Wykonane kontrole automatyczne

- Renderowanie widoków i poprawność składni skryptów.
- Pełny komplet daje 1 punkt; częściowy lub z nadmiarowym wariantem daje 0 punktów. Poprawna odpowiedź nie podświetla niezaznaczonych wariantów jako błędów.
- Wszystkie 56 kombinacji kompletów poprawnych odpowiedzi i zaznaczeń dla A/B/C: pełna treść, poprawny status i podpis każdego wariantu; sprawdzone pominięcia, brak odpowiedzi, kodowanie tekstu oraz przegląd nauki/sprawdzianu/egzaminu.
- Wielokrotny wybór oceniany jako kompletny zestaw; próg 65/64 punktów na egzaminie.
- Odpowiedzi i przypisy ukryte podczas sprawdzianu/egzaminu, dostępne po zakończeniu.
- Losowanie, brak identycznych pytań w zestawie, wybór zakresu i filtry.
- Wznowienie sesji, wygaśnięcie czasu, eksport i import starszych zapisów.
- Walidacja ustawień, rzeczywiste daty kalendarzowe, cel dzienny (w tym 199/200), błędne importy.
- Notatki w kopii postępu, bezpieczne wyświetlanie tekstu użytkownika, flagi i celowane powtórki.
- Skróty klawiaturowe oraz brak przechwytywania tekstu w polach notatek.
- Błąd trwałego zapisu nie jest potwierdzany jako sukces; treść pozostaje w pamięci sesji.
- Ścieżki względne, czcionki lokalne, ikony i manifest dla Pages w podkatalogu.
- Scenariusze service worker: zapis obu baz i czcionek, praca bez sieci, osobny cache dla ścieżki projektu, zachowanie odpowiedzi z sieci przy pełnej pamięci cache.
- Spójność statusów przypisów i dopuszczone urzędowe odnośniki.
- Klucze 3240 pytań z lat 2021–2026 ponownie porównane z kratkami w oryginalnych PDF-ach (`checks/keys.py`: 3240/3240 zgodnych). Treść tych pytań porównana z tekstem PDF-ów (0 rozbieżności przed korektą pisowni).
- Korekta pisowni (493 pola w pytaniach 2021–2026) — wyłącznie ortografia i interpunkcja, log w `data/text-corrections.json`; klucze bez zmian.
- Losowa kolejność odpowiedzi: testy sprawdzają, że każdy wariant zachowuje treść, poprawna odpowiedź trafia na A, B i C, skróty klawiaturowe wybierają widoczną pozycję, punktacja i przegląd wyników używają oryginalnych wariantów, a zapisana kolejność jest walidowana przy imporcie.
- Postęp z usuniętymi pytaniami (2018–2019) jest oczyszczany zamiast odrzucany (test na przykładowej kopii).
- 4 sesje archiwalne 2020–03.2021 (sesje 2018–2019 wycofano w 1.3.0): klucze odczytane automatycznie z kratek skanu i porównane wzrokowo; tekst z OCR z ręczną korektą pól z rozbieżnościami, liczbami i nieznanymi słowami (opis: `data/older/README.md`).
- Paczki dystrybucyjne nie zawierają konfiguracji Sites ani poświadczeń; dołączone manifesty pozwalają sprawdzić integralność.

## Granice potwierdzenia

W tym środowisku nie był dostępny obsługiwany podgląd przeglądarkowy. Nie wykonano końcowego testu wizualnego w rzeczywistym Chrome/Safari ani instalacji na fizycznym telefonie. Testy service worker są symulacją zachowania API, nie pełnym testem przeglądarki.

Po uruchomieniu na własnym GitHub Pages zalecany jest krótki przegląd: widok telefonu i komputera, jasny/nocny motyw, klawiatura i focus dialogu, notatka z eksportem/importem, egzamin po odświeżeniu oraz przejście offline po zakończonej instalacji cache. Nie stanowi to dodatkowego wymogu do zbudowania strony — jest jawnym zakresem niewykonanego sprawdzenia.

Biblioteka jest historyczna. 2457 pytań ma przypis prawny, 571 oznaczenie wiedzy specjalistycznej lub obliczeń, a 572 wymaga dalszej weryfikacji podstawy. Tekst pytań archiwalnych pochodzi z OCR skanów; pola zgodne we wszystkich przebiegach OCR nie były porównywane ze skanem znak po znaku. Potwierdzenie fragmentu w wskazanym tekście aktu nie oznacza pełnego audytu wszystkich historycznych wersji prawa ani zgodności z dzisiejszym egzaminem. Szczegóły w `data/legal/README.md`.

## Komentarze do odpowiedzi

863 pytania bez potwierdzonego przypisu prawnego mają komentarze dydaktyczne ze źródłami, obliczeniami oraz zastrzeżeniami do historycznych kluczy. Logowanie i Firebase usunięto. Postęp zapisuje się lokalnie bez konta; nie synchronizuje się między urządzeniami.
