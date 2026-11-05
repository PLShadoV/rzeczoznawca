# Komentarze do odpowiedzi bez przypisu prawnego

863 wystąpienia pytań, dla których warstwa `legal-bases.json` nie ma statusu `cited`. Podział plików według kategorii służy redakcji; wystąpienia powtórek zachowują osobne identyfikatory.

Każdy wpis zawiera dopasowany `text` i źródła `{title,url}`. Opcjonalny `caveat` wskazuje historyczność, brakujące założenia albo rozbieżność klucza ze źródłem. Komentarze są autorskim opracowaniem dydaktycznym, a nie treścią urzędowego klucza. Link może wspierać metodę lub definicję, nie każdy szczegół dawnej odpowiedzi; granice weryfikacji są zaznaczone. Niepotwierdzonych szczegółów nie należy traktować jako zweryfikowanej podstawy prawnej.

`python3 data/explanations/assemble.py` buduje publiczne `dist/explanations.json`. `python3 checks/explanations.py` sprawdza kompletność i schemat. Kontrola strukturalna nie zastępuje oceny merytorycznej.

Robocze pobrane źródła, korpusy i skrypty pomocnicze w `sources/` są pomijane w wydaniu. Data opracowania: 5 listopada 2026 r. Przed zmianą treści ponownie sprawdź wskazane dokumenty, historyczny kontekst oraz ewentualne sprostowania.
