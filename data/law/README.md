# Stan prawny pytań (weryfikacja na 19.11.2026)

Warstwa obok historycznych kluczy. Mówi, czy odpowiedź z danej sesji zgadza się z prawem obowiązującym w dniu weryfikacji, a dla pytań nieaktualnych podaje klucz według obecnych przepisów (`currentCorrect`) albo oznacza pytanie jako unieważnione (`annulled` — żaden wariant nie jest dziś poprawny, punkt dla każdego). Aplikacja liczy punkty według tej warstwy; `dist/questions.json` zachowuje klucze z arkuszy, a klucz z arkusza jest wyświetlany obok.

- `review-2020-2023.json` — wynik przeglądu 1759 unikalnych pytań z sesji 2020–2023 (grupy identycznych pytań, z identyfikatorami wszystkich wystąpień, także identycznych pytań z lat 2024–2026). Pole `verdict`: `OUT` (nieaktualne; `currentKey` = indeksy poprawnych wariantów dziś lub `null` = unieważnione), `UNC` (do potwierdzenia), `CHG` (zmieniona podstawa, odpowiedź aktualna), `OK` (sprawdzone, bez zmian); brak pola = nie stwierdzono zmian.
- `assemble.py` — buduje `dist/law-status.json` i raport `REPORT.md`. Uruchom: `python3 data/law/assemble.py`.
- `REPORT.md` — lista pytań nieaktualnych i z niepewnym stanem prawnym, z wyjaśnieniem.

## Metoda

1. Dla 30 ustaw powołanych w przypisach pobrano z API Sejmu (ELI) najstarszy tekst jednolity z lat 2020–2022 oraz obecny tekst jednolity. Każdy powołany artykuł porównano automatycznie; 131 artykułów ze zmienioną treścią przejrzano ręcznie razem z pytaniami, które się na nie powołują.
2. Pytania oparte na aktach zastąpionych nowymi (rozporządzenie RM z 2004 r. o wycenie → rozporządzenie MRiT z 5.09.2023 r.; rozporządzenie o EGiB z 2001 r. → z 27.07.2021 r., zmiany 2023, 2024 i 2026) porównano z nowym tekstem ręcznie.
3. Wszystkie pytania bez przypisu prawnego (415 grup) przeczytano i zweryfikowano wybiórczo z aktualnymi tekstami tam, gdzie dotyczą przepisów (AMW, KOWR, ochrona gruntów, PZP, UGN, specustawa drogowa itd.).
4. Pytania czysto rachunkowe, techniczne i ekonomiczne nie dostają statusu.

## Ograniczenia

- Rozporządzenie MI z 12.04.2002 r. (warunki techniczne budynków) jest według ISAP „uznane za uchylone” z dniem 21.09.2026 r. (art. 66 ustawy o zapewnianiu dostępności). Nie znaleziono w Dz.U. nowego rozporządzenia dla budynków — pytania na nim oparte (także z lat 2024–2026) mają status „do potwierdzenia”, a nie „nieaktualne”.
- Reforma planowania: studia uwarunkowań utraciły moc z końcem sierpnia 2026 r.; od 1.09.2026 decyzja o WZ wymaga położenia na obszarze uzupełnienia zabudowy w planie ogólnym.
- Status „bez stwierdzonych zmian” oznacza, że przegląd nie wykazał zmiany wpływającej na odpowiedź — nie jest opinią prawną. Pytania z sesji 2024–2026 (poza warunkami technicznymi) nie były w tym przeglądzie sprawdzane.
