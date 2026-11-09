# Publikacja na Cloudflare Pages

Workflow `.github/workflows/cloudflare.yml` przy każdym pushu uruchamia `npm test`, a potem wysyła katalog `dist/` na Cloudflare Pages:

- push do `main` → wdrożenie produkcyjne (o ile w projekcie Pages gałęzią produkcyjną jest `main`),
- push do innej gałęzi → wdrożenie podglądowe pod osobnym adresem `<gałąź>.<projekt>.pages.dev`.

Nie ma kroku budowania — publikowana jest zawartość `dist/`.

## Konfiguracja (jednorazowo)

1. Projekt Pages: jeśli nie istnieje projekt o nazwie z `CLOUDFLARE_PROJECT_NAME` (domyślnie `rzeczoznawca`), workflow utworzy go sam (adres `https://<nazwa>.pages.dev`). Jeśli masz już projekt pod inną nazwą, wpisz ją w zmiennej.
2. Cloudflare → **My Profile → API Tokens → Create Token** → szablon *Edit Cloudflare Workers* lub własny z uprawnieniem **Account → Cloudflare Pages → Edit**. Skopiuj token.
3. Account ID: widoczny w panelu Cloudflare (Workers & Pages, prawa kolumna).
4. GitHub → repozytorium → **Settings → Secrets and variables → Actions**:
   - *Secrets*: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`,
   - *Variables*: `CLOUDFLARE_PROJECT_NAME` = nazwa projektu (domyślnie `rzeczoznawca`).
5. Uruchom ponownie workflow (Actions → *Deploy to Cloudflare Pages* → *Run workflow*) albo zrób push.

## Jeżeli projekt Pages jest podłączony do GitHuba przez Cloudflare (Git integration)

Wtedy Cloudflare buduje sam — wystarczą ustawienia projektu: **Build command** puste, **Build output directory** `dist`, **Production branch** `main`. Zmiany pojawią się na stronie produkcyjnej dopiero po scaleniu do `main`. W takim przypadku workflow z sekretami nie jest potrzebny (bez sekretów publikacja jest pomijana).
