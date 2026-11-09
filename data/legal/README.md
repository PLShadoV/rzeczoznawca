# Editorial legal references

The question bank and historical official answer keys are unchanged. References are an additional editorial layer, assembled into `dist/legal-bases.json` by `python data/legal/assemble.py`.

Current coverage: 2377 question occurrences with confirmed relevant provisions, 540 methodological/technical/mathematical questions without a directly assigned statutory basis, and 323 unresolved entries. Occurrences may repeat across sessions. All 3240 IDs of the 2021–2026 sessions have an explicit status. The 1710 archive questions (2018–2021) are mapped in `archive-2018-2021.json`: 655 identical to later questions inherit their entry; the rest are `unresolved` until researched. These counts describe coverage, not a guarantee that every historical answer matches the law currently in force.

## Research and evidence

`domains/*-questions.json` groups identical questions, answer options and key sets; occurrence IDs and session dates remain available. `domains/*-citations.json` contains researched mappings for each assigned occurrence. Supplemental `*-extra.json` records and `owner-citations.json` extend those mappings where a verified source resolves an earlier omission. Supplements upgrade unresolved/methodological records; they do not silently replace an already accepted citation.

Each accepted citation contains the full act title, exact editorial unit, official ELI/Sejm URL and an excerpt actually retrieved from that source. Retained source corpora under `sources/` are ignored in Git; they include original official texts and scripts used for extraction. Two PKOB provisions were visually verified in the official scanned PDF (source pages are recorded). Statutory text quotations are government legal materials.

Some provisions explain a method or a formula rather than the numerical result itself. Those records explicitly separate the legal rule from the calculation or technical inference. Historical numbering changes are noted, particularly the valuation regulation replaced in September 2023 and the EGiB regulation replaced in July 2021. A consolidated text published after an examination is not asserted to prove the wording in force on that examination date.

Known contradictions between an official historical key and a statute are unresolved, with an explanatory note. Unsupported candidate provisions are retained only in research files and excluded from the published data. No article is assigned merely because a question contains a keyword.

## Checks

- `python checks/legal.py`: coverage, exact units, official-domain URLs, evidence fields, and potential misclassification of explicitly statutory questions.
- `python checks/legal-evidence.py`: independent comparison of unique excerpts against retained official corpora; manually reviewed scans are explicitly distinguished. Requires the local downloaded source files.
- `node checks/logic.cjs`: references remain hidden during exam/test answering, appear with revealed answers and final review, search/filter behavior, unsafe-link rejection, and existing quiz/persistence functionality.

Independent semantic spot audits of law and valuation mappings were recorded during preparation. Those audits led to corrected units, additional supporting provisions and removal of disputed mappings. They are not a substitute for complete historical legislative version control. Do not present this layer as an official ministerial answer-key annotation or as comprehensive current legal advice.
