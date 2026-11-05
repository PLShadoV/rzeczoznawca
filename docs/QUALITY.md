# Kontrola wydania 1.0.0

## Wykonane kontrole automatyczne

- Renderowanie widoków i poprawność składni skryptów.
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
- Spójność statusów przypisów i dopuszczone urzędowe odnośniki. Dotychczasowe 3240 pytań i klucze pozostają niezmienione.
- Paczki dystrybucyjne nie zawierają konfiguracji Sites ani poświadczeń; dołączone manifesty pozwalają sprawdzić integralność.

## Granice potwierdzenia

W tym środowisku nie był dostępny obsługiwany podgląd przeglądarkowy. Nie wykonano końcowego testu wizualnego w rzeczywistym Chrome/Safari ani instalacji na fizycznym telefonie. Testy service worker są symulacją zachowania API, nie pełnym testem przeglądarki.

Po uruchomieniu na własnym GitHub Pages zalecany jest krótki przegląd: widok telefonu i komputera, jasny/nocny motyw, klawiatura i focus dialogu, notatka z eksportem/importem, egzamin po odświeżeniu oraz przejście offline po zakończonej instalacji cache. Nie stanowi to dodatkowego wymogu do zbudowania strony — jest jawnym zakresem niewykonanego sprawdzenia.

Biblioteka jest historyczna. 2377 pytań ma przypis prawny, 540 oznaczenie wiedzy specjalistycznej lub obliczeń, a 323 wymaga dalszej weryfikacji podstawy. Potwierdzenie fragmentu w wskazanym tekście aktu nie oznacza pełnego audytu wszystkich historycznych wersji prawa ani zgodności z dzisiejszym egzaminem. Szczegóły w `data/legal/README.md`.
