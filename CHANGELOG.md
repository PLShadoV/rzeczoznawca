# Historia zmian

## 1.1.1 — 2026-11-05

- Usunięto konta, logowanie i integrację Firebase.
- Przywrócono lokalny zapis postępów, notatek i historii bez konta, wraz z eksportem/importem i obsługą starszych zapisów.
- Zachowano wszystkie 863 komentarze ze źródłami oraz wcześniejsze zasady oceniania.

## 1.1.0 — 2026-11-05

- Dodano 863 dopasowane komentarze do pytań bez przypisu prawnego, z rachunkami, źródłami i zastrzeżeniami do historycznych kluczy.
- Dodano panel kont Firebase: rejestrację, logowanie, reset hasła i zapis postępu tylko po zalogowaniu. Uruchomienie wymaga własnego projektu i publicznej konfiguracji.
- Gość nie zapisuje postępu w przeglądarce; dawne dane lokalne można świadomie przenieść na konto.
- Zapis jest potwierdzany przez serwer, chroniony przed nadpisaniem nowszej wersji i zatrzymywany przy nieudanym odczycie.
- Wylogowanie czyści widok, aktualizacja czeka na zapis, a awarie wymagają ponowienia lub eksportu kopii.
- Dołączono reguły Firestore, lokalny SDK z licencją, instrukcję wdrożenia i testy integracji klienta.

## 1.0.2 — 2026-11-05

- Ocena pytania wyraźnie pokazuje 1/1 lub 0/1 punktu; odpowiedź częściowa jest błędem i wymienia brakujące poprawne warianty.
- Przy pełnej poprawnej odpowiedzi podświetlone są wyłącznie trafione warianty. Pozostałe są neutralne, bez oznaczeń błędu.
- Przy niepełnym lub błędnym zestawie własne zaznaczenia są wyróżnione, a brakujące poprawne odpowiedzi podpisane.
- Zachowano punktację wymagającą dokładnego kompletu, historię oraz dane użytkownika.

## 1.0.1 — 2026-11-05

- Przegląd wyników nauki, sprawdzianu i egzaminu pokazuje pełną treść wszystkich wariantów odpowiedzi.
- Zielony wskazuje poprawny wariant, pomarańczowy własne błędne zaznaczenie, a czerwony pozostały błędny wariant. Podpisy zapewniają zrozumienie wyniku także bez kolorów.
- Poprawne, lecz pominięte odpowiedzi są wyraźnie podpisane. Zachowano przypisy prawne i notatki.
- Punktacja i historyczne klucze pozostają niezmienione.
- Zwiększono wersję cache offline; użytkownik może zaakceptować aktualizację przyciskiem Odśwież.

## 1.0.0 — 2026-11-05

Pierwsze samodzielne wydanie gotowe do GitHub Pages.

- Dopracowany wygląd, architektoniczne ilustracje, lokalne czcionki i ikony.
- Jasny/nocny motyw oraz wybór większego tekstu pytań i odpowiedzi.
- Cel dzienny, własny termin egzaminu, plan tempa nauki i wykres aktywności.
- Osobiste notatki, flagi pytań, celowane powtórki i skróty klawiaturowe.
- Opcjonalna instalacja PWA i praca offline; kontrolowana aktualizacja cache.
- 3240 historycznych pytań z 36 sesji, nauka, losowe sprawdziany, pełne egzaminy.
- 2377 pytań z przypisami prawnymi; pozostałe jawnie sklasyfikowane.
- Zgodne ze starszymi kopiami postępu przechowywanie i import.
- Testy automatyczne, lokalny serwer bez zależności, workflow Pages i paczki dystrybucyjne.
