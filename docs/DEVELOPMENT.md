# Rozwój i aktualizacja

## Edycja strony

1. Uruchom `npm run dev` w głównym katalogu. Dostępne opcje: `--host` i `--port`.
2. Edytuj pliki `dist/`. Widoki używają fragmentów URL, a zasoby ścieżek względnych — zachowaj tę zasadę, aby obsługiwać Pages w podkatalogu.
3. Zmiany związane z nauką i oceną są w `app.js`. Osobiste narzędzia i wygląd obsługuje `enhancements.js`. Ten drugi plik jest ładowany przed `app.js`; wspólne funkcje widzą się w klasycznym kontekście skryptów.
4. Nowy stan zapisuj w sposób zgodny ze starszymi eksportami. Format `pracownia-v1` i stabilne identyfikatory pytań są używane do migracji. Nowe opcjonalne pola wymagają wartości domyślnych oraz walidacji importu.
5. Uruchom `npm test`. Sprawdź stronę w przeglądarce na komputerze i telefonie oraz kontrast w obu motywach. Testy automatyczne nie potwierdzają układu wizualnego.

Klawisze podczas sesji: A/B/C lub 1/2/3 wybierają wariant, Enter sprawdza/przechodzi dalej, strzałki nawigują, F przełącza flagę. Nie przechwytujemy skrótów w edytowanych polach, na przyciskach/linkach ani w otwartym dialogu.

## Nowe wydanie i cache offline

- Zwiększ wersję w `package.json` oraz `VERSION` w `dist/sw.js`. Cache ma osobną nazwę dla ścieżki aplikacji, aby nie usuwać danych innych projektów na tej samej domenie.
- Jeżeli dodasz zasób niezbędny offline, dopisz jego względną ścieżkę do `CORE` w `sw.js` i sprawdź testy.
- Service worker instaluje pełen zestaw zasobów nowej wersji i czeka. Aktywna wersja korzysta z własnego cache, aby nie mieszać skryptów kolejnych wydań. Użytkownik otrzymuje przycisk **Odśwież**. Przed akceptacją zapisywany jest stan sesji.
- Nie zmieniaj klucza danych `pracownia-v1` bez opracowania migracji. Cache plików strony i zapis postępu to oddzielne mechanizmy.
- Po zmianie wersji przejrzyj scenariusz: otwarta stara wersja → nowa publikacja → informacja o aktualizacji → odświeżenie → zachowany postęp.
- Przy diagnostyce możesz w DevTools usunąć rejestrację service worker i cache tej aplikacji. Nie usuwaj `localStorage`, jeśli chcesz zachować postęp; najpierw pobierz kopię.

## Przygotowanie paczek

```sh
npm test
python3 scripts/package-release.py --output ../wydania
```

Skrypt zapisuje ZIP repozytorium, ZIP samej strony, manifest plików i sumy SHA-256. W repozytorium Git wybiera śledzone pliki (nowe pliki najpierw dodaj przez `git add`). W wyeksportowanej paczce korzysta z dołączonego manifestu. Nie dołącza `.git`, `.openai`, `.env`, poświadczeń, zależności ani surowych pobranych dokumentów. Paczka statyczna ma pliki `dist/` bez dodatkowego katalogu — jej zawartość można wgrać na hosting.

## Dane pytań i przypisy

`questions.json` przechowuje historyczne klucze ministerstwa, a `legal-bases.json` opracowanie redakcyjne. Nie zmieniaj klucza tylko dlatego, że dzisiejszy przepis jest inny; najpierw zweryfikuj właściwą wersję prawa i oficjalne sprostowanie. Sprzeczność lub brak potwierdzenia oznacz jako wymagające weryfikacji. Kategorie pytań są pomocnicze.

Standardowe testy danych: `python3 checks/legal.py`. Dodatkowa kontrola kluczy z PDF-ów (`checks/keys.py`) wymaga PyMuPDF, Pillow i lokalnych oryginalnych dokumentów. Kontrola fragmentów (`checks/legal-evidence.py`) wymaga pobranych urzędowych korpusów, które są pomijane w paczce. Samo mapowanie można odtworzyć z plików `data/legal/` przez `assemble.py`; przed publikacją ponownie sprawdź treść źródeł.
