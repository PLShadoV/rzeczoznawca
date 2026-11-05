# Uruchomienie i publikacja na GitHub Pages

Projekt jest statyczną aplikacją. Gotowe pliki strony znajdują się w `dist/`; nie ma backendu, bazy serwerowej ani logowania. Do uruchomienia lokalnie wystarczy Node.js 22 lub nowszy. Kontrole wymagają także Pythona 3 dostępnego jako `python3`. Aplikacja i serwer lokalny nie wymagają instalowania pakietów npm.

## Lokalnie

W katalogu projektu uruchom:

```sh
npm run dev
```

Otwórz `http://127.0.0.1:4173`. Serwer udostępnia wyłącznie `dist/`. Nie otwieraj `index.html` bezpośrednio przez `file://`, ponieważ aplikacja pobiera pliki JSON.

Inny adres lub port:

```sh
npm run dev -- --host 127.0.0.1 --port 8080
```

Możesz także ustawić zmienne `HOST` i `PORT`. Parametry polecenia mają pierwszeństwo. Domyślny adres `127.0.0.1` udostępnia stronę na tym komputerze; `--host 0.0.0.0` pozwala otworzyć ją z innych urządzeń w dostępnej sieci. Zatrzymanie: `Ctrl+C`.

Przed wysłaniem zmian:

```sh
npm test
```

Polecenie uruchamia `node checks/logic.cjs`, `python3 checks/legal.py` oraz `checks/release.cjs`, jeżeli ten ostatni plik istnieje. Nie pobiera zależności. To kontrola działania i spójności danych; nie zastępuje merytorycznej weryfikacji historycznego klucza i przepisów.

## Wysłanie projektu do GitHuba

1. Zaloguj się samodzielnie na `https://github.com` i wybierz **New repository**. Dla bezpłatnego hostingu Pages wybierz repozytorium publiczne, np. `pracownia-rzeczoznawcy`. Utwórz puste repozytorium, bez dodawania README, licencji lub `.gitignore` przez formularz.
2. Zainstaluj Git, jeśli jeszcze go nie masz. Skopiuj adres HTTPS nowego repozytorium z przycisku **Code**. Uwierzytelnij Git własnym kontem, np. przez Git Credential Manager. Projekt nie wymaga tokenu wpisanego w plikach ani integracji z kontem.
3. Sklonuj puste repozytorium do nowego katalogu:

   ```sh
   git clone https://github.com/TWOJ_LOGIN/pracownia-rzeczoznawcy.git
   cd pracownia-rzeczoznawcy
   ```

4. Skopiuj do tego katalogu pliki projektu: `dist/`, `checks/`, `scripts/`, `docs/`, `data/`, `.github/`, `.gitignore`, `package.json`, `README.md` i `LICENSE`. Zachowaj ukryty katalog `.github` z workflow. Jeżeli dołączono inne pliki konfiguracyjne, również je skopiuj. Nie kopiuj katalogów `.git`, `.openai`, `node_modules` ani lokalnych kopii postępów nauki.
5. Sprawdź projekt i wyślij pliki:

   ```sh
   npm test
   git add .
   git commit -m "Dodaj aplikację Pracownia Rzeczoznawcy"
   git branch -M main
   git push -u origin main
   ```

   Zastąp `TWOJ_LOGIN` swoim loginem. Jeśli Git poprosi o nazwę autora lub adres e-mail, skonfiguruj własne dane; nie publikuj danych innej osoby. Przed zatwierdzeniem możesz sprawdzić `git status` i `git diff --cached`.

## Włączenie strony

1. W repozytorium wejdź w **Settings → Pages**.
2. W sekcji **Build and deployment**, w polu **Source**, wybierz **GitHub Actions**.
3. Otwórz **Actions → Validate and publish GitHub Pages → Run workflow**. Wybierz gałąź `main` i uruchom workflow. Jeśli pierwszy przebieg po wysłaniu plików zakończył się przed włączeniem Pages, uruchom go ponownie.
4. Po zakończeniu zadania `deploy` adres strony znajdziesz w wyniku wdrożenia oraz w **Settings → Pages**. Zwykle będzie to `https://TWOJ_LOGIN.github.io/pracownia-rzeczoznawcy/`.

Każdy push i pull request uruchamia kontrole. Publikacja odbywa się dopiero po ich powodzeniu, z gałęzi `main`, po pushu albo ręcznym uruchomieniu. Pull requesty i inne gałęzie nie publikują strony. Do Pages trafia wyłącznie `dist/`; pliki robocze i dokumentacja nie są częścią publikowanej witryny. Nie ma kroku kompilacji: zmiany strony wprowadza się w plikach `dist/`.

Ścieżki zasobów aplikacji są względne, a widoki korzystają z fragmentu adresu (`#…`), więc strona może działać w podkatalogu repozytorium na Pages. Zachowaj tę zasadę przy zmianach: używaj np. `questions.json` i `assets/...`, zamiast ścieżek zaczynających się od `/`. Nie jest potrzebna konfiguracja przekierowań serwera ani stała nazwa repozytorium w kodzie.

## Postępy i przenoszenie strony

Postępy, zakładki i historia są zapisywane w `localStorage` przeglądarki, osobno dla originu, czyli połączenia protokołu, domeny i portu. Nie synchronizują się przez GitHub ani między urządzeniami. `localhost`, `127.0.0.1`, inny port i domena Pages to różne miejsca zapisu. Różne podkatalogi tej samej domeny mają wspólny origin; dwie kopie aplikacji mogą korzystać z tego samego klucza danych.

Przed zmianą domeny, przejściem z lokalnego adresu na Pages, czyszczeniem danych przeglądarki lub większą aktualizacją wyeksportuj kopię postępów w aplikacji. Zachowaj plik na swoim urządzeniu, otwórz nową stronę i zaimportuj kopię. Nie dodawaj prywatnego eksportu do publicznego repozytorium. Samo skopiowanie plików strony nie przenosi postępów.

## Licencje i źródła

Oryginalny kod i dokumentacja projektu są objęte licencją MIT z pliku `LICENSE`. Ta licencja nie zmienia statusu urzędowych pytań, kluczy, aktów prawnych i cytowanych dokumentów. Zachowaj informacje o ich pochodzeniu w aplikacji oraz plikach danych. To niezależna pomoc edukacyjna, bez deklaracji poparcia instytucji państwowych.

Fonty DM Sans i Manrope mają osobne licencje SIL Open Font License 1.1 w `dist/assets/fonts/`. Publikuj je wraz z dołączonymi informacjami o prawach autorskich i licencjami.

Workflow oparto na oficjalnej dokumentacji GitHuba sprawdzonej 5 listopada 2026 r.: [publikowanie Pages przez własny workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) i [kontrole projektu Node.js](https://docs.github.com/en/actions/tutorials/build-and-test-code/nodejs). Użyte wersje z dokumentacji: checkout v6, setup-node v7, configure-pages v5, upload-pages-artifact v4 i deploy-pages v4. Uprawnienia zapisu Pages i token OIDC ma tylko zadanie wdrożenia.
