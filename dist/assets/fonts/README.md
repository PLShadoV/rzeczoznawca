# Local web fonts

Downloaded 2026-11-05 from official Google Fonts CSS and fonts.gstatic.com. Both families are licensed under the SIL Open Font License 1.1. The original license files are included unchanged.

- DM Sans: normal variable weights 400–700, Latin and Latin Extended subsets.
- Manrope: normal variable weights 400–800, Latin and Latin Extended subsets.
- Both Latin Extended Unicode ranges cover Polish diacritics (ĄĆĘŁŃŚŹŻ and lowercase); Ó/ó are covered by Latin.

Include from the site root HTML:

```html
<link rel="stylesheet" href="assets/fonts/fonts.css">
```

All font URLs used by `fonts.css` are local relative URLs. No Google request is needed at runtime. `google-fonts-source.css` is a provenance snapshot only; do not include it in the page.

## Sources and licenses

CSS request: <https://fonts.googleapis.com/css2?family=DM+Sans:wght@400..700&family=Manrope:wght@400..800&display=swap>.
Requested with Chrome 131 User-Agent to receive variable WOFF2 files. Original CSS is retained in `google-fonts-source.css`; direct asset URLs are also recorded in `sources.json`.

- DM Sans OFL: <https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/OFL.txt>
- Manrope OFL: <https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/OFL.txt>

## Verification

Each downloaded asset has the WOFF2 `wOF2` signature, a valid declared file size and a nonzero table count. Requested weight ranges and Unicode coverage were checked against the official generated CSS. Full font table decoding was unavailable because the environment lacked the Brotli extension for fontTools.

| File | Bytes | SHA-256 | Source |
| --- | ---: | --- | --- |
| `dm-sans-latin-ext-variable.woff2` | 18228 | `a5d38fe99f930275684999b462c7123faa063d9e44e73b4b241723d884aa0f49` | [Google gstatic source](https://fonts.gstatic.com/s/dmsans/v17/rP2Yp2ywxg089UriI5-g4vlH9VoD8Cmcqbu6-K6h9Q.woff2) |
| `dm-sans-latin-variable.woff2` | 36932 | `9fea608a947e67020c33cad9a6fe3d60c54119dfb8cff87768a8117a15ed7543` | [Google gstatic source](https://fonts.gstatic.com/s/dmsans/v17/rP2Yp2ywxg089UriI5-g4vlH9VoD8Cmcqbu0-K4.woff2) |
| `manrope-latin-ext-variable.woff2` | 15160 | `2f7335119075b2079f1d882530bbc18728461612bf90743203d73a74a48f4d9b` | [Google gstatic source](https://fonts.gstatic.com/s/manrope/v23/xn7gYHE41ni1AdIRggmxSuXd.woff2) |
| `manrope-latin-variable.woff2` | 24532 | `8c2def024c1bf31aacf3624ae3c4d701269b4ec3dc765c04830839f0d36b2d9e` | [Google gstatic source](https://fonts.gstatic.com/s/manrope/v23/xn7gYHE41ni1AdIRggexSg.woff2) |
