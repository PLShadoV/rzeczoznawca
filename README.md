![Pracownia Rzeczoznawcy](docs/banner.svg)

# Pracownia Rzeczoznawcy

**Wersja 1.1.1.** Gotowa, samodzielna aplikacja do nauki na egzamin na rzeczoznawcę majątkowego. Działa bez konta i backendu. Możesz opublikować ją na **GitHub Pages** lub dowolnym hostingu statycznym. Wszystkie pliki strony są w `dist/`.

## Szybki start

Wymagany Node.js **22 lub nowszy**. Do kontroli danych potrzebny jest także Python 3. Nie trzeba instalować żadnych pakietów npm.

```sh
npm run dev
```

Otwórz **http://127.0.0.1:4173**. Nie otwieraj `index.html` przez dwuklik — aplikacja pobiera lokalne pliki JSON przez HTTP.

```sh
npm test
```

**Publikacja:** [instrukcja GitHub Pages krok po kroku](docs/GITHUB.md). W repozytorium wybierz **Settings → Pages → Source: GitHub Actions**. Workflow sprawdza kod i publikuje `dist/` po pushu do gałęzi `main` lub ręcznym uruchomieniu. Kod działa także w podkatalogu repozytorium; nie musisz zmieniać adresów w aplikacji.

## Co znajduje się w aplikacji

- **Nauka:** wybór tematu, sesji, liczby i statusu pytań; poprawny komplet odpowiedzi po sprawdzeniu pytania.
- **Losowa nauka i sprawdzian:** 10, 20, 30, 50, 90 lub 100 pytań z całej bazy. Bez identycznych pytań w jednym zestawie; wybierana jest najnowsza wersja powtórzonej treści. Sprawdzian pokazuje wynik dopiero na końcu.
- **Czytelny przegląd wyników:** pełna treść wszystkich odpowiedzi; pełny poprawny zestaw daje 1 punkt i pozostawia niezaznaczone warianty neutralne. Odpowiedź częściowa daje 0 punktów, wskazuje brakujące warianty i oznacza zaznaczenia jako niepełny zestaw. Przy błędzie pokazywane są poprawne warianty oraz błędne zaznaczenia. Każdy wariant ma także podpis poprawności i informację o zaznaczeniu.
- **Egzamin próbny:** pełne historyczne arkusze lub losowy zestaw, 90 pytań / 90 minut, próg 65 punktów, pełny przegląd po zakończeniu. Czas biegnie także po zamknięciu strony.
- **Baza:** wyszukiwanie treści, nazw aktów i artykułów; filtrowanie sesji, kategorii, odpowiedzi i statusu podstawy prawnej.
- **Podstawy prawne:** nazwa aktu, konkretny art./§/ustęp/punkt, urzędowy link i rozwijany fragment źródła.
- **Osobista pracownia:** notatki do pytań, zakładki, flagi „wrócę do tego”, cel dzienny, własna data egzaminu i sugerowane tempo nauki.
- **Powtórki i statystyki:** zestaw błędnych odpowiedzi, historia wyników, seria dni nauki i wykres aktywności z 14 dni.
- **Czytelność:** spójna zielona stylistyka, architektoniczne ilustracje, tryb nocny, większy tekst pytań, responsywny widok i skróty klawiaturowe.
- **Przenoszenie postępu:** eksport/import JSON obejmuje notatki i ustawienia. Starsze kopie pozostają obsługiwane.
- **Praca offline / PWA:** po pierwszym pełnym wczytaniu przez HTTPS aplikacja może działać bez połączenia i zostać dodana do ekranu głównego. Lokalne czcionki i wszystkie dane są częścią strony. Urzędowe PDF-y i witryny aktów nadal wymagają internetu.

## Dane i zakres weryfikacji

Baza zawiera **3240 pytań z 36 pełnych sesji z lat 2021–2026**, od kwietnia 2021 do września 2026. To pytania z arkuszy, więc treści mogą powtarzać się między sesjami. Nie jest to kompletny zbiór wszystkich egzaminów. Każdy rekord zachowuje datę sesji, oryginalny numer, warianty, oficjalny klucz i odnośniki do źródeł.

Źródło arkuszy i kluczy: [oficjalna strona ministerstwa dla kandydatów na rzeczoznawców](https://www.gov.pl/web/rozwoj-technologia/jak-zostac-rzeczoznawca-majatkowym). Podział tematyczny jest pomocniczy. Projekt jest niezależny od ministerstwa i InfoGeoTech.

Warstwa przypisów zawiera **2377 pytań z potwierdzonymi powiązaniami z przepisami**, **540 oznaczeń zagadnień specjalistycznych lub obliczeniowych** i **323 pozycje wymagające dalszej weryfikacji**. Obejmuje wskazany tekst aktu, a nie automatyczne potwierdzenie jego aktualności na dziś lub brzmienia w każdej historycznej dacie. Rozbieżności kluczy z przepisami są oznaczane; oryginalnej punktacji nie zmieniono. Szczegóły: [dokumentacja przypisów](data/legal/README.md).

## Prywatność i kopie zapasowe

Postęp, historia, flagi, notatki i ustawienia są przechowywane w `localStorage` **na urządzeniu użytkownika**. Aplikacja nie wysyła ich na serwer, nie korzysta z zewnętrznych analizatorów ruchu ani z zewnętrznych serwerów czcionek. Hosting może przetwarzać standardowe żądania HTTP zgodnie ze swoimi zasadami. Otwarcie źródła prawnego prowadzi do zewnętrznej witryny urzędowej.

Przed przeniesieniem strony na nową domenę, zmianą przeglądarki lub usunięciem danych przeglądarki pobierz kopię w **Statystykach**. `localhost`, `127.0.0.1`, inny port i GitHub Pages mają różne miejsca zapisu. GitHub nie synchronizuje danych nauki. Nie dodawaj prywatnych eksportów do publicznego repozytorium.

Jeżeli przeglądarka blokuje zapis lub ma zapełnioną pamięć, aplikacja ostrzega i pozwala pobrać kopię bieżącej sesji. Tryb offline wymaga obsługi service worker, miejsca w pamięci i wcześniejszego pełnego wczytania. Nie zastępuje kopii postępu.

## Struktura

```text
.github/workflows/pages.yml    # kontrole + publikacja GitHub Pages
checks/                       # testy logiki, danych i wydania
scripts/serve.mjs              # lokalny serwer bez zależności
scripts/package-release.py     # przygotowanie ZIP-ów do dystrybucji
docs/                         # wdrożenie, rozwój, kontrola jakości
dist/
  index.html                  # punkt wejścia
  app.js                      # baza, tryby nauki, egzamin, przypisy
  enhancements.js             # plan, notatki, flagi, ustawienia, skróty
  bootstrap.js                # zapisany wygląd przed pierwszym renderem
  style.css + release.css     # podstawowe style i oprawa wydania 1.0
  offline.js + sw.js          # opcjonalna praca offline i aktualizacje
  manifest.webmanifest        # instalacja PWA
  questions.json              # oryginalne pytania i klucze
  legal-bases.json             # niezależna warstwa przypisów
  assets/                    # ilustracje, ikony i lokalne czcionki
data/                         # źródła, mapowania i narzędzia redakcyjne
```

Nie ma kroku kompilacji. Na hosting trafia wyłącznie zawartość `dist/`. **GitHub-ready ZIP nie zawiera historii Git, identyfikatorów Sites, poświadczeń ani pobranych roboczych PDF-ów.**

## Rozwój i wydania

[Instrukcja rozwijania i aktualizacji](docs/DEVELOPMENT.md) · [Zakres przeprowadzonych kontroli](docs/QUALITY.md) · [Historia zmian](CHANGELOG.md)

Podstawowe kontrole wymagają jedynie Node.js i standardowej biblioteki Pythona. Dodatkowe odtwarzanie pytań z PDF-ów lub ponowna kontrola cytatów wymaga lokalnych źródeł oraz narzędzi opisanych w dokumentacji danych. Nie jest potrzebne do uruchomienia strony ani standardowego CI.

## Licencja

Oryginalny kod i dokumentacja: [MIT](LICENSE). Urzędowe materiały zachowują własne źródła i status prawny. Czcionki DM Sans i Manrope: osobne licencje **SIL OFL 1.1**, dołączone w `dist/assets/fonts/`.

## Komentarze do odpowiedzi

863 pytania bez potwierdzonego przypisu prawnego mają komentarze dydaktyczne ze źródłami, obliczeniami oraz zastrzeżeniami do historycznych kluczy. Logowanie i Firebase usunięto. Postęp zapisuje się lokalnie bez konta; nie synchronizuje się między urządzeniami.
