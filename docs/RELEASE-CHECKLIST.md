# Skrócona instrukcja wydania

1. Wprowadź zmiany w `dist/` i dokumentacji.
2. Zwiększ numer w `package.json` i `dist/sw.js`; uzupełnij `CHANGELOG.md`.
3. Uruchom `npm test` i przejrzyj wygląd w przeglądarce.
4. Zachowaj zgodność eksportów postępu lub dodaj migrację.
5. Dodaj pliki do Git. Uruchom `python3 scripts/package-release.py --output ../wydania`.
6. Sprawdź sumy SHA-256. W ZIP-ie repozytorium jest `RELEASE-MANIFEST.json` oraz `SHA256SUMS.txt`.
7. Do GitHuba wrzuć **zawartość folderu `pracownia-rzeczoznawcy`** z paczki, razem z ukrytym `.github/`. Następnie włącz GitHub Actions w ustawieniach Pages, zgodnie z `GITHUB.md`.
8. Na zwykły hosting wgraj zawartość paczki `strona`, tak aby `index.html` był plikiem głównym.

Paczka źródłowa jest samodzielna i nie zawiera `.openai`, `.git`, poświadczeń ani roboczych dokumentów źródłowych. Bieżący katalog używany do publikacji w Sites zachowuje własną konfigurację; nie kopiuj jej do repozytorium GitHub.
