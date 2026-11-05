"use strict";
const ICONS = {
  home: "M3 10 12 3l9 7v10a1 1 0 0 1-1 1h-6v-7h-4v7H4a1 1 0 0 1-1-1Z",
  book: "M12 5c-3-2-7-2-10-1v15c3-1 7-1 10 1m0-15c3-2 7-2 10-1v15c-3-1-7-1-10 1Zm0 0v15",
  exam: "M8 4H5v17h14V4h-3M8 2h8v5H8ZM8 12h8M8 16h5",
  db: "M20 6c0 2-4 3-8 3S4 8 4 6s4-3 8-3 8 1 8 3ZM4 6v12c0 2 4 3 8 3s8-1 8-3V6M4 12c0 2 4 3 8 3s8-1 8-3",
  chart: "M4 20h17M7 16V9m5 7V4m5 12v-5",
  bookmark: "M6 3h12v19l-6-4-6 4Z",
  arrow: "M4 12h15m-5-5 5 5-5 5",
  chevron: "m9 5 7 7-7 7",
  clock: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18Zm0 4v5l3 2",
  check: "m5 12 4 4L19 6",
  close: "m6 6 12 12M6 18 18 6",
  calendar: "M4 5h16v16H4ZM8 2v6m8-6v6M4 11h16",
  shield: "m12 2 8 3v6c0 5-8 11-8 11S4 16 4 11V5Zm-4 9 3 3 5-5",
  bulb: "M9 18v-2a6 6 0 1 1 6 0v2ZM9 21h6",
  building: "M5 21V7l7-4 7 4v14M2 21h20M9 9v1m6-1v1m-6 3v1m6-1v1m-6 7v-4h6v4",
  scale: "M12 3v18m-7 0h14M3 7h18M6 7l-4 8h8Zm12 0-4 8h8Z",
  map: "m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2Zm6-2v16m6-14v16",
  leaf: "M20 3C9 1 2 7 5 15c6 7 16-1 15-12ZM4 21 16 8",
  target:
    "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18Zm0 5a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm0 3v2",
  refresh: "M20 8a8 8 0 1 0 0 8M20 3v6h-6",
  download: "M12 3v12m-5-5 5 5 5-5M4 17v4h16v-4",
  upload: "M12 16V3m-5 5 5-5 5 5M4 17v4h16v-4",
  external: "M14 3h7v7m0-7L10 14M10 3H3v18h18v-7",
  search: "M10 3a7 7 0 1 0 0 14 7 7 0 0 0 0-14Zm5 12 6 6",
  info: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18Zm0 7v7m0-11v1",
  spark: "m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5Z",
};
Object.assign(ICONS, {
  moon: "M20 14a8 8 0 0 1-10-10 9 9 0 1 0 10 10Z",
  sun: "M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8ZM12 2v2m0 16v2M2 12h2m16 0h2M5 5l2 2m10 10 2 2M5 19l2-2M17 7l2-2",
  settings:
    "M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8ZM9 3h6l1 3 3 1 2 5-2 5-3 1-1 3H9l-1-3-3-1-2-5 2-5 3-1Z",
  flag: "M5 22V3c5-4 9 4 14 0v11c-5 4-9-4-14 0",
  note: "M5 3h14v18H5ZM8 8h8m-8 4h8m-8 4h5",
  help: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18ZM9 9a3 3 0 0 1 6 0c0 2-3 2-3 5m0 3v1",
});
const I = (n) =>
  `<svg class="ico" aria-hidden="true" viewBox="0 0 24 24"><path d="${ICONS[n] || ICONS.book}"/></svg>`;
const esc = (s) =>
  String(s ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const $ = (s) => document.querySelector(s),
  dateLabel = (d) =>
    new Date(d + "T12:00:00").toLocaleDateString("pl-PL", {
      day: "numeric",
      month: "long",
      year: "numeric",
    }),
  today = () => new Date().toLocaleDateString("sv-SE");
const CATS = [
  "Wycena nieruchomości",
  "Prawo i gospodarka nieruchomościami",
  "Planowanie i geodezja",
  "Budownictwo",
  "Ekonomia i finanse",
  "Rolnictwo i leśnictwo",
];
const CAT_ICONS = ["building", "scale", "map", "building", "chart", "leaf"];
const fresh = () => ({
  answers: {},
  bookmarks: [],
  history: [],
  days: {},
  active: null,
  notes: {},
  settings: defaultSettings(),
});
let state = fresh(),
  storageOK = true;
try {
  let x = JSON.parse(localStorage.getItem("pracownia-v1"));
  if (
    x &&
    x.answers &&
    Array.isArray(x.bookmarks) &&
    Array.isArray(x.history) &&
    x.days
  )
    state = { ...fresh(), ...x };
} catch (e) {
  storageOK = false;
}
let legalBases = {},
  legalMeta = null,
  legalReady = false;
let Q = [],
  sessions = [],
  byId = {},
  view = "home",
  filter = { search: "", category: "", session: "", status: "", legal: "" },
  page = 1,
  quiz = null,
  review = null,
  detail = null,
  lastModalFocus = null;
function save() {
  try {
    localStorage.setItem("pracownia-v1", JSON.stringify(state));
    storageOK = true;
    return true;
  } catch (e) {
    storageOK = false;
    if (!$("#storage-warn"))
      toast(
        "Przeglądarka nie pozwala zapisać postępu. Pobierz kopię w Statystykach.",
      );
    return false;
  }
}
function toast(s) {
  $("#toast").textContent = s;
  $("#toast").classList.add("show");
  clearTimeout(toast.t);
  toast.t = setTimeout(() => $("#toast").classList.remove("show"), 3500);
}
const exact = (a, b) =>
  Array.isArray(a) &&
  a.length === b.length &&
  [...a].sort().join() === [...b].sort().join();
const correct = (q) => state.answers[q.id]?.correct === true;
const stats = () => {
  const a = Object.values(state.answers);
  return {
    done: a.length,
    good: a.filter((x) => x.correct).length,
    attempts: a.reduce((s, x) => s + (x.attempts || 1), 0),
  };
};
const pct = (a, b) => (b ? Math.round((a / b) * 100) : 0);
function btn(label, act, icon = "arrow", cls = "") {
  return `<button class="btn ${cls}" data-action="${act}">${label}${I(icon)}</button>`;
}
function shell(content) {
  const nav = [
    ["home", "home", "Pulpit"],
    ["learn", "book", "Tryb nauki"],
    ["exams", "exam", "Egzaminy"],
    ["base", "db", "Baza pytań"],
    ["saved", "bookmark", "Zapisane"],
    ["stats", "chart", "Statystyki"],
  ];
  const titles = {
    home: "Pulpit",
    learn: "Tryb nauki",
    exams: "Egzaminy",
    base: "Baza pytań",
    saved: "Zapisane pytania",
    stats: "Statystyki",
    sources: "Źródła i zasady",
    quiz: quiz ? modeLabel(quiz.mode, quiz.scope) : "Sesja nauki",
    result: "Podsumowanie",
    review: "Przegląd odpowiedzi",
  };
  $("#app").innerHTML =
    `<div class="shell"><aside class="sidebar"><a href="#home" class="brand"><span class="brandmark">${I("building")}</span><span>Pracownia<br>Rzeczoznawcy<small>TWOJA PRZESTRZEŃ DO NAUKI</small></span></a><div class="navlabel">TWOJA PRACOWNIA</div><nav aria-label="Menu główne">${nav.map(([v, i, t]) => `<a href="#${v}" title="${t}" ${view === v ? 'aria-current="page"' : ""} class="${view === v ? "active" : ""}">${I(i)}<span>${t}</span>${v === "base" ? `<span class="count">${Q.length}</span>` : ""}</a>`).join("")}</nav><div class="sidebottom"><div class="sidehelp">${I("bulb")}<h3>Małe kroki. Duży postęp.</h3><p>Nawet 15 minut nauki dziennie przybliża Cię do celu.</p><button data-action="learn-config">Zacznij krótką sesję ↗</button></div><div class="local"><span class="dot"></span>Bez konta. W Twoim tempie.</div></div></aside><main class="main" id="main-content" tabindex="-1"><header class="topbar"><div class="crumb">Twoja pracownia <span>/ &nbsp; ${titles[view] || "Pulpit"}</span></div><a class="mobilebrand" href="#home">Pracownia Rzeczoznawcy</a><div class="topright">${networkBadge()}<span class="date">Przestrzeń do dobrego przygotowania</span><span class="pill">${I("shield")} Bez logowania</span><div class="toolbar"><button class="iconbtn" data-action="theme" aria-label="${preferences().theme === "dark" ? "Włącz jasny wygląd" : "Włącz tryb nocny"}" title="Zmień wygląd">${I(preferences().theme === "dark" ? "sun" : "moon")}</button><button class="iconbtn" data-action="help" aria-label="Pomoc i skróty klawiaturowe" title="Pomoc">${I("help")}</button><button class="iconbtn" data-action="settings" aria-label="Ustawienia i plan nauki" title="Ustawienia pracowni">${I("settings")}</button></div></div></header><div class="content">${!storageOK ? '<div id="storage-warn" class="notice">Zapis lokalny jest niedostępny. Zachowaj postęp, pobierając kopię w Statystykach.</div>' : ""}${content}<footer class="foot"><span>© ${new Date().getFullYear()} Pracownia Rzeczoznawcy · Wersja 1.0 · Ucz się świadomie.</span><span><button data-action="help">Pomoc i skróty</button> &nbsp; · &nbsp; Postęp na tym urządzeniu &nbsp; · &nbsp; <button data-action="sources">Źródła i zasady</button></span></footer></div></main></div>`;
}
const head = (h, p, extra = "") =>
  `<div class="pagehead"><div><h1>${h}</h1><p>${p}</p></div>${extra}</div>`;
function statCards() {
  const s = stats();
  return `<div class="stats">${[
    ["db", "Pytania w bazie", Q.length, "", "z oficjalnych arkuszy"],
    [
      "check",
      "Przerobione pytania",
      s.done,
      `/ ${Q.length}`,
      "każda odpowiedź to krok dalej",
    ],
    [
      "target",
      "Skuteczność",
      s.done ? pct(s.good, s.done) + "%" : "—",
      "",
      "na podstawie ostatnich odpowiedzi",
    ],
    [
      "exam",
      "Ukończone egzaminy",
      state.history.filter((h) => h.mode === "exam").length,
      "",
      "sprawdź swoje przygotowanie",
    ],
  ]
    .map(
      ([i, n, v, u, note]) =>
        `<div class="stat"><div class="stat-icon">${I(i)}</div><div><div class="stat-name">${n}</div><div class="stat-value">${v}<small>${u}</small></div><div class="stat-note">${note}</div></div></div>`,
    )
    .join("")}</div>`;
}
const modeLabel = (mode, scope) =>
  mode === "exam"
    ? "Egzamin"
    : mode === "test"
      ? "Losowy sprawdzian"
      : scope === "all"
        ? "Losowa nauka"
        : "Nauka";
const yearsLabel = () =>
  sessions.length
    ? `${sessions[sessions.length - 1].date.slice(0, 4)}–${sessions[0].date.slice(0, 4)}`
    : "";
function modeCards() {
  return (
    `<div class="modes"><article class="mode"><div class="mode-icon">${I("book")}</div><h3>Ucz się w swoim tempie</h3><p>Wybierz temat, rozwiązuj pytania i od razu sprawdzaj poprawne odpowiedzi.</p><div class="tags"><span>${I("clock")} Bez limitu czasu</span><span>${I("check")} Odpowiedzi po każdym pytaniu</span></div>${btn("Rozpocznij naukę", "learn-config")}</article><article class="mode exam"><div class="mode-icon">${I("exam")}</div><h3>Sprawdź się na egzaminie</h3><p>Poczuj rytm prawdziwego egzaminu. Pełny arkusz, odliczanie czasu i wynik na koniec.</p><div class="tags"><span>${I("db")} 90 pytań</span><span>${I("clock")} 90 minut</span><span>${I("target")} Próg: 65 punktów</span></div>${btn("Rozpocznij egzamin", "exam-config")}</article></div>` +
    randomModes()
  );
}
function randomModes() {
  return `<div class="sectiontitle"><div><h2>Losuj z całej bazy</h2><p>Wszystkie lata i obszary. Za każdym razem nowy zestaw, bez identycznych pytań.</p></div></div><div class="modes random-modes"><article class="mode"><div class="mode-icon">${I("refresh")}</div><h3>Losowa nauka</h3><p>Wymieszaj pytania z całej bazy i utrwalaj wiedzę. Poprawne odpowiedzi sprawdzisz po każdym pytaniu.</p><div class="tags"><span>${I("db")} Cała baza · ${yearsLabel()}</span><span>${I("clock")} Bez limitu czasu</span></div>${btn("Losuj pytania do nauki", "random-learn")}</article><article class="mode exam"><div class="mode-icon">${I("target")}</div><h3>Losowy sprawdzian</h3><p>Sprawdź wiedzę na pytaniach z różnych lat i dziedzin. Wynik i odpowiedzi zobaczysz dopiero na końcu.</p><div class="tags"><span>${I("db")} Wybierasz liczbę pytań</span><span>${I("clock")} Bez limitu czasu</span></div>${btn("Losuj pytania do sprawdzianu", "random-test", "arrow", "secondary")}</article></div>`;
}
function topicRows(action = "topic") {
  return CATS.map((c, i) => {
    const qs = Q.filter((q) => q.category === c),
      done = qs.filter((q) => state.answers[q.id]).length,
      p = pct(done, qs.length);
    return `<div class="topic"><div class="topic-icon">${I(CAT_ICONS[i])}</div><div><div class="topic-name">${c}</div><div class="topic-meta">${qs.length} pytań · ${done} przerobionych</div></div><div class="tinybar"><i style="width:${p}%"></i></div><span class="pct">${p}%</span><button title="Ucz się: ${c}" aria-label="Ucz się: ${c}" data-action="${action}" data-value="${i}">${I("chevron")}</button></div>`;
  }).join("");
}
function habit() {
  let d = new Date();
  let dow = (d.getDay() + 6) % 7;
  let days = [];
  for (let i = 0; i < 7; i++) {
    let x = new Date(d);
    x.setDate(x.getDate() - dow + i);
    let key = x.toLocaleDateString("sv-SE");
    days.push(
      `<div class="day">${["Pn", "Wt", "Śr", "Cz", "Pt", "So", "Nd"][i]}<b class="${state.days[key] ? "done" : ""}">${state.days[key] ? "✓" : i === dow ? "•" : "–"}</b></div>`,
    );
  }
  return `<div class="habit"><div class="habit-head">${I("spark")} REGULARNOŚĆ MA ZNACZENIE</div><h3>Buduj wiedzę.<br>Jeden dzień po drugim.</h3><p>Nie musisz wiedzieć wszystkiego od razu.<br>Wróć do pytań, które sprawiają trudność.</p><div class="week">${days.join("")}</div><p>${state.days[today()] ? `Dzisiaj: ${state.days[today()]} sprawdzonych odpowiedzi. Tak trzymaj!` : "Dziś jest dobry dzień, żeby zacząć."}</p><div class="study-tip">${I("bulb")}<p>Przy pytaniach wielokrotnego wyboru oceniaj każdy wariant osobno. Punkt dostaniesz za cały poprawny zestaw.</p></div></div>`;
}
const ART = `<svg class="hero-art" viewBox="0 0 420 250" fill="none" aria-hidden="true"><circle cx="261" cy="127" r="112" fill="#e0e8d9"/><circle cx="261" cy="127" r="91" stroke="#c5d1ba" stroke-dasharray="3 5"/><path d="M45 213h341M82 199h265" stroke="#a8b89c"/><path d="m130 100 72-39 69 40v104H130Z" fill="#edf1e5" stroke="#91a582" stroke-width="1.3"/><path d="m202 61 1 144m-73-105 73 41 68-40M203 141v64M146 119v23l39 23v-24m-39 17v23l39 23v-23m36-37v23l33-19v-23m-33 60v23l33-19v-23" stroke="#8fa17f" stroke-width="1.3"/><path d="m118 96 84-48 82 49-13 8-69-40-72 41Z" fill="#c1cfb3" stroke="#8da17d"/><path d="m108 196 41-24 74 43 99-58 38 22-136 79Z" fill="#d0dcc1" stroke="#a3b58e"/><path d="m282 118 37-22 34 20v62l-35 21-36-21Z" fill="#e8efdf" stroke="#99ac87"/><path d="m319 96-1 103m-36-81 36 21 35-23m-23 17v14m-41-19v14m41 0v14m-41-19v14" stroke="#99ac87"/><path d="M89 198v-49m0 19c-33-12-18-35-3-24 17-29 39-3 3 24Z" fill="#b5c7a4" stroke="#94a981"/><path d="M365 190v-42m0 16c-27-11-17-32-3-22 15-24 31-1 3 22Z" fill="#bcccae" stroke="#94a981"/><circle cx="326" cy="54" r="15" fill="#f3f5e9"/><path d="m320 54 4 4 8-8" stroke="#91a47c" stroke-width="2"/><path d="m93 81 9-5m-4 12 9-5m227 133 9-5" stroke="#adbfa0"/></svg>`;
function home() {
  let active = state.active;
  return (
    head(
      "Dobrze Cię widzieć.",
      "Kolejny krok do uprawnień zaczyna się tutaj.",
      `<span class="date">${I("calendar")} ${new Date().toLocaleDateString("pl-PL", { day: "numeric", month: "long", year: "numeric" })}</span>`,
    ) +
    `<section class="hero"><div class="hero-copy"><div class="eyebrow"><span class="dot"></span> WIEDZA, KTÓRA BUDUJE PEWNOŚĆ</div><h2>Twoje uprawnienia.<br>Twój kolejny rozdział.</h2><p>Przygotuj się do egzaminu na rzeczoznawcę majątkowego. Krok po kroku, na własnych zasadach.</p><div class="hero-proof"><span>${I("db")} ${Q.length} pytań</span><span>${I("calendar")} ${sessions.length} sesji</span><span>${I("shield")} Oficjalne arkusze</span></div>${active ? btn("Kontynuuj rozpoczętą sesję", "resume") : btn("Zacznij dzisiejszą naukę", "learn-config")}</div>${ART}</section>` +
    statCards() +
    dailyDashboard() +
    `<div class="sectiontitle"><div><h2>Jak chcesz się dzisiaj uczyć?</h2><p>Dwa tryby. Jeden cel — dobre przygotowanie.</p></div></div>` +
    modeCards() +
    `<div class="lower"><section><div class="sectiontitle"><h2>Twoje obszary nauki</h2><a class="textlink" href="#base">Cała baza pytań ${I("arrow")}</a></div><div class="panel">${topicRows()}</div></section><section><div class="sectiontitle"><h2>Dobry nawyk na przyszłość</h2></div>${habit()}</section></div>`
  );
}
function learnPage() {
  return (
    head(
      "Wiedza rośnie z każdym pytaniem.",
      "Wybierz swój zakres i ucz się bez presji czasu.",
    ) +
    modeCards() +
    `<div class="sectiontitle"><h2>Wybierz obszar nauki</h2>${state.active ? btn("Wznów sesję", "resume", "arrow", "secondary") : ""}</div><div class="panel">${topicRows()}</div><div class="notice">Klucze są historyczne — odpowiedzi odpowiadają stanowi prawnemu w dniu danej sesji. Kategorie są pomocniczym podziałem tematycznym.</div>`
  );
}
function examPage() {
  return (
    head(
      "Generalna próba przed egzaminem.",
      "Pełne arkusze, prawdziwe zasady punktacji, Twoje tempo przygotowań.",
      btn("Losowy egzamin · 90 pytań", "exam-config"),
    ) +
    `<div class="notice">90 pytań wielokrotnego wyboru · 90 minut · minimum 65 punktów. Punkt otrzymasz za wskazanie całego poprawnego zestawu odpowiedzi. ${state.active?.mode === "exam" ? '<button class="textlink" data-action="resume">Wznów trwający egzamin →</button>' : ""}</div>${randomModes()}<div class="sectiontitle"><h2>Wybierz historyczny arkusz</h2><a href="#sources" class="textlink">Oficjalne źródła ${I("external")}</a></div><div class="modes">${sessions.map((s) => `<article class="mode exam"><div class="eyebrow">SESJA EGZAMINACYJNA · ${s.date.slice(0, 4)}</div><h3>${dateLabel(s.date)}</h3><p>Oryginalna kolejność pytań i oficjalny klucz odpowiedzi. Odpowiedzi zobaczysz po zakończeniu.</p><div class="tags"><span>${I("db")} ${s.count} pytań</span><span>${I("clock")} 90 minut</span></div><button class="btn secondary" data-action="exam-session" data-value="${s.date}">Rozwiąż arkusz ${I("arrow")}</button></article>`).join("")}</div>`
  );
}
function filtered() {
  const term = (filter.search || "").toLocaleLowerCase("pl-PL");
  return Q.filter(
    (q) =>
      (view !== "saved" || state.bookmarks.includes(q.id)) &&
      (!filter.category || q.category === filter.category) &&
      (!filter.session || q.session === filter.session) &&
      (!term ||
        `${q.question} ${q.options.join(" ")} ${(legalBases[q.id]?.citations || []).map((c) => c.act + " " + c.provision).join(" ")}`
          .toLocaleLowerCase("pl-PL")
          .includes(term)) &&
      (!filter.legal || legalBases[q.id]?.status === filter.legal) &&
      (!filter.status ||
        (filter.status === "new"
          ? !state.answers[q.id]
          : filter.status === "wrong"
            ? state.answers[q.id] && !correct(q)
            : correct(q))),
  );
}
function opts(arr, value) {
  return arr
    .map(
      (x) =>
        `<option value="${esc(x.value ?? x)}" ${(x.value ?? x) === value ? "selected" : ""}>${esc(x.label ?? x)}</option>`,
    )
    .join("");
}
function basePage() {
  const found = filtered(),
    pages = Math.max(1, Math.ceil(found.length / 12));
  page = Math.min(page, pages);
  return (
    head(
      view === "saved"
        ? "Pytania, do których warto wrócić."
        : "Dobra nauka zaczyna się od pytań.",
      view === "saved"
        ? "Twoja własna kolekcja do powtórek."
        : `${Q.length} pytań z ${sessions.length} oficjalnych arkuszy · lata ${yearsLabel()}`,
    ) +
    `<div class="filters"><label class="sr" for="search">Szukaj pytania</label><input id="search" type="search" placeholder="Szukaj pytania, ustawy lub artykułu…" value="${esc(filter.search)}"><label class="sr" for="catfilter">Obszar nauki</label><select id="catfilter"><option value="">Wszystkie obszary</option>${opts(CATS, filter.category)}</select><label class="sr" for="sessionfilter">Sesja</label><select id="sessionfilter"><option value="">Wszystkie sesje</option>${opts(
      sessions.map((s) => ({ value: s.date, label: dateLabel(s.date) })),
      filter.session,
    )}</select><label class="sr" for="statusfilter">Status pytania</label><select id="statusfilter"><option value="">Każdy status</option>${opts(
      [
        { value: "new", label: "Nieprzerobione" },
        { value: "wrong", label: "Do powtórki" },
        { value: "good", label: "Poprawne" },
      ],
      filter.status,
    )}</select><label class="sr" for="legalfilter">Podstawa odpowiedzi</label><select id="legalfilter"><option value="">Każda podstawa odpowiedzi</option>${opts(
      [
        { value: "cited", label: "Z przypisem prawnym" },
        { value: "nonlegal", label: "Specjalistyczne i obliczeniowe" },
        { value: "unresolved", label: "Podstawa do weryfikacji" },
      ],
      filter.legal,
    )}</select></div><div class="sectiontitle"><p>Znaleziono ${found.length} pytań${filter.search || filter.category || filter.session || filter.status || filter.legal ? ' · <button class="textlink" data-action="clear-filters">Wyczyść filtry</button>' : ""}</p>${found.length ? `<button class="textlink" data-action="learn-filtered">Ucz się z tego wyboru ${I("arrow")}</button>` : ""}</div>${
      found.length
        ? `<div class="questions">${found
            .slice((page - 1) * 12, page * 12)
            .map((q) => qRow(q))
            .join(
              "",
            )}</div><div class="pagination"><button class="btn secondary" data-action="prev-page" ${page === 1 ? "disabled" : ""}>← Poprzednia</button><span>Strona ${page} z ${pages}</span><button class="btn secondary" data-action="next-page" ${page === pages ? "disabled" : ""}>Następna →</button></div>`
        : `<div class="empty">${I(view === "saved" ? "bookmark" : "search")}<h3>${view === "saved" && !state.bookmarks.length ? "Tutaj zacznie się Twoja kolekcja." : "Brak pytań dla tego wyboru."}</h3><p>${view === "saved" && !state.bookmarks.length ? "Zapisuj pytania zakładką podczas nauki lub przeglądania bazy." : "Zmień wyszukiwanie lub wyczyść filtry."}</p>${btn("Przejdź do bazy", "go-base", "db", "secondary")}</div>`
    }`
  );
}
function bookmarkButton(q) {
  let b = state.bookmarks.includes(q.id);
  return `<button class="iconbtn ${b ? "saved" : ""}" aria-label="${b ? "Usuń z zapisanych" : "Zapisz pytanie"}" aria-pressed="${b}" data-action="bookmark" data-value="${q.id}">${I("bookmark")}</button>`;
}
function qRow(q, r) {
  return `<article class="qrow"><div class="qmeta"><span class="badge">${esc(q.category)}</span><span>${dateLabel(q.session)} · pytanie ${q.number}</span>${r !== undefined ? `<span class="badge">${r ? "Poprawnie" : "Do powtórki"}</span>` : state.answers[q.id] ? `<span>${correct(q) ? "✓ Poprawnie" : "↻ Do powtórki"}</span>` : ""}</div><h3>${esc(q.question)}</h3><div class="qrow-foot"><button class="textlink" data-action="detail" data-value="${q.id}">Zobacz odpowiedzi ${I("arrow")}</button>${bookmarkButton(q)}</div></article>`;
}
function sourcesPage() {
  return (
    head(
      "Przejrzyste źródła. Rzetelna nauka.",
      "Baza pochodzi z publicznych arkuszy ministerstwa, a nie z serwisu InfoGeoTech.",
    ) +
    `<div class="panel" style="padding:23px;margin-bottom:22px"><h2>Jak korzystać z bazy?</h2><p class="muted" style="margin-top:12px;font-size:14px;line-height:1.9">Pytania oraz klucze pochodzą z materiałów opublikowanych na <a href="https://www.gov.pl/web/rozwoj-technologia/jak-zostac-rzeczoznawca-majatkowym" target="_blank" rel="noopener">oficjalnej stronie ministerstwa</a>. Baza obejmuje ${sessions.length} pełnych sesji (${Q.length} pytań, z możliwymi powtórzeniami między arkuszami). Nie jest to kompletny zbiór wszystkich dotychczasowych egzaminów. Podział tematyczny jest pomocniczy.</p><div class="notice">Odpowiedzi są zgodne z historycznym kluczem danej sesji. Nie zostały zweryfikowane z aktualnym stanem prawnym. W razie wątpliwości sprawdź oryginalny arkusz i obowiązujące przepisy. Serwis nie jest oficjalną stroną ministerstwa.</div><p class="muted" style="font-size:14px;line-height:1.9">Tryb egzaminu: 90 pytań, 90 minut, próg 65 punktów. Za pytanie przyznawany jest 1 punkt wyłącznie za zaznaczenie wszystkich poprawnych wariantów i żadnego błędnego. <a href="https://eli.gov.pl/eli/DU/2025/88/ogl/pol/pdf" target="_blank" rel="noopener">Zasady egzaminu (§ 27)</a>.</p><h3 style="margin:23px 0 8px">Twoje dane zostają w przeglądarce</h3><p class="muted" style="font-size:14px;line-height:1.9">Nie potrzebujesz konta. Postęp, zakładki oraz historia są przechowywane lokalnie na tym urządzeniu. Nie synchronizują się między urządzeniami. Usunięcie danych przeglądarki usuwa także postęp — kopię można pobrać w Statystykach. Czcionki są przechowywane razem ze stroną. Aplikacja nie korzysta z zewnętrznych analizatorów ruchu. Po pełnym wczytaniu może działać offline; zewnętrzne akty prawne i PDF-y wymagają internetu.</p></div>${legalOverview()}<div class="sectiontitle"><h2>Arkusze i oficjalne klucze odpowiedzi</h2></div><div class="panel">${sessions.map((s) => `<div class="source-row"><div><strong>${dateLabel(s.date)}</strong><p>${s.count} pytań · materiały ministerstwa</p></div><div><a href="${s.source}" target="_blank" rel="noopener">Arkusz PDF ↗</a><a href="${s.keySource}" target="_blank" rel="noopener">Klucz PDF ↗</a></div></div>`).join("")}</div>`
  );
}
function statsPage() {
  return (
    head(
      "Zobacz, jak daleko już jesteś.",
      "Postęp na tym urządzeniu. Każda sesja ma znaczenie.",
    ) +
    statCards() +
    activityChart() +
    `<div class="sectiontitle"><h2>Postęp w obszarach</h2></div><div class="panel">${topicRows()}</div><div class="sectiontitle" style="margin-top:28px"><h2>Historia sesji</h2></div>${
      state.history.length
        ? `<div class="panel"><table class="history"><thead><tr><th>Data</th><th>Tryb</th><th>Wynik</th><th>Rezultat</th></tr></thead><tbody>${state.history
            .slice()
            .reverse()
            .map(
              (h) =>
                `<tr><td>${new Date(h.date).toLocaleDateString("pl-PL")}</td><td>${modeLabel(h.mode, h.scope)}</td><td>${h.score} / ${h.total}</td><td>${h.mode === "exam" ? (h.score >= 65 ? "Zaliczony" : "Do powtórki") : pct(h.score, h.total) + "%"}</td></tr>`,
            )
            .join("")}</tbody></table></div>`
        : `<div class="empty">${I("chart")}<h3>Pierwszy wynik jest jeszcze przed Tobą.</h3><p>Ukończ naukę lub egzamin, a zobaczysz tu historię sesji.</p>${btn("Rozpocznij naukę", "learn-config")}</div>`
    }<div class="sectiontitle" style="margin-top:28px"><div><h2>Twój postęp, Twoja kopia</h2><p>Zapisz kopię, żeby przenieść wyniki do innej przeglądarki.</p></div></div><div class="filters">${btn("Pobierz kopię postępu", "export", "download", "secondary")}${btn("Wczytaj kopię", "import", "upload", "secondary")}<input type="file" id="import-file" accept="application/json,.json" hidden>${btn("Wyczyść postęp", "reset-dialog", "refresh", "ghost")}</div>`
  );
}
function showModal(content) {
  lastModalFocus = document.activeElement;
  $("#modal").innerHTML =
    `<div class="overlay"><section class="dialog" role="dialog" aria-modal="true" aria-labelledby="dialog-title">${content}</section></div>`;
  $("#modal button, #modal select, #modal input")?.focus();
}
const modalHead = (t) =>
  `<div class="dialog-head"><h2 id="dialog-title">${t}</h2><button class="iconbtn" data-action="close-modal" aria-label="Zamknij">${I("close")}</button></div>`;
function closeModal() {
  $("#modal").innerHTML = "";
  lastModalFocus?.focus?.();
}
function config(mode, cat = "", session = "", wholeBase = false) {
  if (state.active) {
    showModal(
      modalHead("Masz rozpoczętą sesję.") +
        `<p>Możesz wrócić do niej albo zastąpić ją nową. Sprawdzone odpowiedzi z nauki pozostaną w postępie. Trwający egzamin nadal odlicza czas.</p><div class="actions">${btn("Kontynuuj", "resume")}<button class="btn secondary" data-action="replace-session" data-value="${mode}|${cat}|${session}|${wholeBase ? "all" : ""}">Nowa sesja</button></div>`,
    );
    return;
  }
  openConfig(mode, cat, session, wholeBase);
}
function openConfig(mode, cat = "", session = "", wholeBase = false) {
  let exam = mode === "exam",
    test = mode === "test";
  showModal(
    modalHead(
      exam
        ? "Przygotuj swój egzamin"
        : test
          ? "Losowy sprawdzian z całej bazy"
          : wholeBase
            ? "Losowa nauka z całej bazy"
            : "Twoja następna sesja nauki",
    ) +
      `<p>${exam ? "90 pytań · 90 minut · próg 65 punktów. Poprawne odpowiedzi poznasz na końcu." : test ? "Wybierz liczbę pytań. Odpowiadaj bez limitu czasu, a wynik i poprawne odpowiedzi poznasz po zakończeniu." : wholeBase ? "Wybierz liczbę pytań. Po każdym pytaniu możesz sprawdzić odpowiedzi z oficjalnego klucza." : "Wybierz zakres. Po każdym pytaniu sprawdzisz odpowiedzi z oficjalnego klucza."}</p><form id="config-form" class="form"><input type="hidden" name="mode" value="${mode}"><input type="hidden" name="scope" value="${wholeBase ? "all" : ""}">${
        wholeBase
          ? `<div class="scope-note">${I("db")}<div><strong>Cała baza: ${Q.length} pytań · ${yearsLabel()}</strong><p>Wszystkie obszary i sesje. Identyczne pytanie pojawi się w zestawie tylko raz; użyjemy jego najnowszej wersji w bazie.</p></div></div>`
          : `<label>Arkusz egzaminacyjny<select name="session"><option value="">${exam ? "Losowy zestaw z całej bazy" : "Wszystkie sesje"}</option>${opts(
              sessions.map((s) => ({
                value: s.date,
                label: dateLabel(s.date),
              })),
              session,
            )}</select></label>`
      }${!exam ? `${wholeBase ? "" : `<label>Obszar nauki<select name="category"><option value="">Wszystkie obszary</option>${opts(CATS, cat)}</select></label>`}<div class="${wholeBase ? "" : "row"}"><label>Liczba pytań<select name="limit">${opts(["10", "20", "30", "50", "90", "100"], "20")}</select></label>${wholeBase ? "" : `<label>Wybierz pytania<select name="pool"><option value="all">Wszystkie</option><option value="new">Nieprzerobione</option><option value="wrong">Błędne odpowiedzi</option><option value="saved">Zapisane</option></select></label>`}</div>` : ""}<div class="notice">${wholeBase ? "Każde pytanie ma podaną datę źródłowego egzaminu. " : ""}Klucze dotyczą stanu prawnego z dnia danej sesji. Odpowiedzi mogą być wielokrotnego wyboru.</div><div id="config-error" role="alert"></div><button type="submit" class="btn">${exam ? "Rozpocznij egzamin" : test ? "Wylosuj i rozpocznij sprawdzian" : wholeBase ? "Wylosuj i rozpocznij naukę" : "Rozpocznij naukę"} ${I("arrow")}</button></form>`,
  );
}
function shuffle(a) {
  a = [...a];
  for (let i = a.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function uniqueQuestions(list) {
  const latest = new Map();
  for (const q of list) {
    const key = (q.question + "|" + q.options.join("|"))
      .normalize("NFC")
      .replace(/\s+/g, " ")
      .trim();
    const old = latest.get(key);
    if (!old || q.session > old.session) latest.set(key, q);
  }
  return [...latest.values()];
}
function startQuiz(mode, list, limit = 20, ordered = false, wholeBase = false) {
  if (!list.length) {
    toast("Brak pytań dla tego wyboru.");
    return false;
  }
  if (!ordered) {
    list = uniqueQuestions(list);
  }
  const size = mode === "exam" ? 90 : limit;
  if (mode === "exam" && list.length < 90) {
    toast("Brakuje pytań do pełnego egzaminu. Wybierz inny zakres.");
    return false;
  }
  let ids = (ordered ? list : shuffle(list)).slice(0, size).map((q) => q.id);
  const started = Date.now();
  quiz = {
    mode,
    scope: wholeBase ? "all" : "selection",
    ids,
    index: 0,
    answers: {},
    checked: {},
    flags: [],
    started,
    deadline: mode === "exam" ? started + 90 * 60 * 1000 : null,
  };
  state.active = quiz;
  save();
  closeModal();
  navigate("quiz");
  return true;
}
function markLearn(q) {
  const previousDaily = state.days[today()] || 0;
  let selected = quiz.answers[q.id] || [];
  let ok = exact(selected, q.correct);
  quiz.checked[q.id] = ok;
  let old = state.answers[q.id];
  state.answers[q.id] = {
    correct: ok,
    attempts: (old?.attempts || 0) + 1,
    last: Date.now(),
  };
  state.days[today()] = (state.days[today()] || 0) + 1;
  state.active = quiz;
  save();
  render();
  goalMilestone(previousDaily);
}
function quizPage() {
  if (!quiz) return home();
  let q = byId[quiz.ids[quiz.index]],
    isExam = quiz.mode === "exam",
    isTest = quiz.mode === "test",
    delayed = quiz.mode !== "learn",
    selected = quiz.answers[q.id] || [],
    checked = !delayed && Object.hasOwn(quiz.checked, q.id),
    answered = quiz.ids.filter((id) => (quiz.answers[id] || []).length).length;
  return (
    head(
      isExam
        ? "Skup się. Masz to w sobie."
        : isTest
          ? "Sprawdź wiedzę z całej bazy."
          : "Krok po kroku, pytanie po pytaniu.",
      delayed
        ? "Odpowiedzi możesz zmieniać do zakończenia. Wynik poznasz na końcu."
        : "Zaznacz wszystkie odpowiedzi, które uważasz za poprawne.",
      `<button class="btn secondary" data-action="leave-quiz">${isExam ? "Wyjdź z egzaminu" : "Zapisz i wyjdź"}</button>`,
    ) +
    `<div class="quizlayout"><section class="quizcard"><div class="qmeta"><span class="badge">${modeLabel(quiz.mode, quiz.scope).toLocaleUpperCase("pl-PL")}</span><span>Pytanie ${quiz.index + 1} z ${quiz.ids.length}</span><span class="question-tools" style="margin-left:auto">${flagButton(q)}${bookmarkButton(q)}</span></div><div class="bar"><i style="width:${((quiz.index + 1) / quiz.ids.length) * 100}%"></i></div><div class="qmeta" style="margin-top:22px"><span>${esc(q.category)}</span><span>· ${dateLabel(q.session)}, nr ${q.number}</span></div><h2>${esc(q.question)}</h2><p class="quizhint">Pytanie wielokrotnego wyboru — jedna, dwie lub trzy odpowiedzi mogą być poprawne.</p><div class="options" role="group" aria-label="Odpowiedzi">${q.options.map((o, i) => `<button class="option ${selected.includes(i) ? "selected" : ""} ${checked && q.correct.includes(i) ? "correct" : ""} ${checked && selected.includes(i) && !q.correct.includes(i) ? "wrong" : ""}" role="checkbox" aria-checked="${selected.includes(i)}" data-action="answer" data-value="${i}" ${checked ? "disabled" : ""}><span class="letter">${"ABC"[i]}</span><span>${esc(o)}</span></button>`).join("")}</div>${checked ? feedback(q, quiz.checked[q.id]) : ""}<div class="quizactions"><button class="btn secondary" data-action="quiz-prev" ${quiz.index === 0 ? "disabled" : ""}>← Wstecz</button>${!delayed && !checked ? `<button class="btn" data-action="check" ${!selected.length ? "disabled" : ""}>Sprawdź odpowiedź ${I("check")}</button>` : btn(quiz.index === quiz.ids.length - 1 ? (isExam ? "Zakończ egzamin" : isTest ? "Zakończ sprawdzian" : "Zakończ naukę") : "Następne pytanie", "quiz-next")}</div></section><aside class="quizside">${isExam ? `<p class="muted" style="font-size:14px">POZOSTAŁY CZAS</p><div class="timer" id="timer">${formatTime(quiz.deadline - Date.now())}</div><div class="bar" style="margin-bottom:20px"></div>` : ""}<h3>Twój zestaw pytań</h3>${quiz.scope === "all" ? '<p class="legend">Wylosowane z całej bazy · bez identycznych pytań</p>' : ""}<div class="qgrid">${quiz.ids.map((id, i) => `<button title="Pytanie ${i + 1}${(quiz.flags || []).includes(id) ? " — do przejrzenia" : ""}" aria-label="Pytanie ${i + 1}${(quiz.flags || []).includes(id) ? ", oznaczone do przejrzenia" : ""}" ${i === quiz.index ? 'aria-current="step"' : ""} data-action="quiz-jump" data-value="${i}" class="${i === quiz.index ? "current" : ""} ${(quiz.flags || []).includes(id) ? "flagged" : ""} ${(quiz.answers[id] || []).length ? "answered" : ""} ${!delayed && quiz.checked[id] === false ? "bad" : ""}">${i + 1}</button>`).join("")}</div><p class="legend">${answered} / ${quiz.ids.length} z zaznaczoną odpowiedzią${(quiz.flags || []).length ? ` · ${quiz.flags.length} do przejrzenia` : ""}</p><p class="keyboard-hint"><kbd>A</kbd><kbd>B</kbd><kbd>C</kbd> — odpowiedzi · <kbd>Enter</kbd> — dalej</p>${delayed ? `<button class="btn secondary" style="width:100%;margin-top:18px" data-action="finish-dialog">${isExam ? "Zakończ egzamin" : "Zakończ sprawdzian"}</button>` : ""}<p class="legend">${isExam ? "Czas biegnie także po zamknięciu strony. Egzamin zostanie rozliczony po upływie 90 minut." : isTest ? "Bez limitu czasu. Możesz zmieniać odpowiedzi. Poprawny zestaw i wynik poznasz po zakończeniu." : "Możesz wrócić do poprzednich pytań. Sprawdzone odpowiedzi pozostają zapisane."}</p></aside></div>`
  );
}
function legalURL(value) {
  try {
    const u = new URL(value);
    return u.protocol === "https:" &&
      (u.hostname === "eli.gov.pl" || u.hostname.endsWith(".gov.pl"))
      ? u.href
      : null;
  } catch {
    return null;
  }
}
function legalBasis(q) {
  const entry = legalBases[q.id];
  if (!legalReady)
    return `<section class="legal-basis legal-pending"><h3>${I("scale")} Podstawa prawna</h3><p>Nie udało się wczytać przypisów prawnych. Odśwież stronę; pytania i postęp nadal działają.</p></section>`;
  if (!entry || entry.status === "unresolved")
    return `<section class="legal-basis legal-pending"><h3>${I("scale")} Podstawa prawna do weryfikacji</h3><p>Do tego pytania nie przypisano jeszcze potwierdzonego przepisu. Nie podajemy niezweryfikowanego numeru artykułu.</p>${entry?.note ? `<p>${esc(entry.note)}</p>` : ""}</section>`;
  if (entry.status === "nonlegal")
    return `<section class="legal-basis legal-technical"><h3>${I("book")} Podstawa odpowiedzi</h3><p class="legal-caption">Pytanie specjalistyczne lub obliczeniowe — bez wskazanej bezpośredniej podstawy ustawowej.</p><p>${esc(entry.note || "Odpowiedź opiera się na wiedzy specjalistycznej, a nie na pojedynczym przepisie ustawy.")}</p></section>`;
  const citations = (entry.citations || []).filter((c) => legalURL(c.url));
  if (!citations.length)
    return `<section class="legal-basis legal-pending"><h3>${I("scale")} Podstawa prawna do weryfikacji</h3><p>Brak potwierdzonego odnośnika do przepisu.</p></section>`;
  return `<section class="legal-basis"><h3>${I("scale")} Podstawa prawna odpowiedzi</h3>${citations.map((c) => `<article class="legal-citation"><div class="legal-provision">${esc(c.provision)}</div><p class="legal-act">${esc(c.act)}</p><a href="${esc(legalURL(c.url))}" target="_blank" rel="noopener">Otwórz oficjalny tekst aktu ${I("external")}</a>${c.evidence ? `<details><summary>Pokaż fragment przepisu</summary><blockquote>${esc(c.evidence)}</blockquote></details>` : ""}${c.note ? `<p class="legal-note">${esc(c.note)}</p>` : ""}</article>`).join("")}${entry.note ? `<p class="legal-note">${esc(entry.note)}</p>` : ""}<p class="legal-caption">Przypis opracowany na podstawie wskazanego tekstu aktu; nie jest częścią oficjalnego klucza. Przepisy mogły zmieniać się między sesjami. Data pytania: ${dateLabel(q.session)}.</p></section>`;
}
function legalOverview() {
  if (!legalMeta) return "";
  const c = legalMeta.counts;
  return `<section class="panel legal-overview"><h2>Podstawy prawne odpowiedzi</h2><p>Przy odpowiedziach w trybie nauki, w podglądzie pytania oraz po zakończeniu sprawdzianu i egzaminu znajdziesz przypisy z konkretnym artykułem lub paragrafem, nazwą aktu i odnośnikiem do oficjalnego tekstu.</p><div class="legal-counts"><span><b>${c.cited}</b> pytań z przypisem prawnym</span><span><b>${c.nonlegal}</b> pytań specjalistycznych lub obliczeniowych</span><span><b>${c.unresolved}</b> pytań z podstawą do dalszej weryfikacji</span></div><p>Każdy przypis wymagał sprawdzenia treści wskazanego przepisu. Nie oznacza to pełnej weryfikacji obowiązywania tego brzmienia w dniu każdej historycznej sesji ani aktualności na dziś. Datę i wersję sprawdzisz w źródłowym akcie. Wątpliwe przypisania są oznaczone zamiast uzupełniane domyślnym artykułem.</p><p class="muted">Data opracowania przypisów: ${esc(legalMeta.checkedAt)}. Odpowiedzi i punktacja nadal pochodzą z historycznych kluczy ministerstwa.</p></section>`;
}
function feedback(q, ok) {
  return `<div class="feedback ${ok ? "" : "error"}" role="status"><strong>${ok ? "✓ Dobra odpowiedź." : "↻ To pytanie warto powtórzyć."}</strong><p>Poprawny zestaw z klucza: <b>${q.correct.map((i) => "ABC"[i]).join(", ")}</b>.</p>${q.correct.map((i) => `<p>${"ABC"[i]}. ${esc(q.options[i])}</p>`).join("")}<p style="margin-top:9px;font-size:12px;color:#7f8773">Klucz historyczny — stan na ${dateLabel(q.session)}. Bez weryfikacji z obecnymi przepisami.</p><a href="${q.keySource}" target="_blank" rel="noopener">Oficjalny klucz PDF ↗</a> &nbsp; <a href="${q.source}" target="_blank" rel="noopener">Arkusz źródłowy PDF ↗</a>${legalBasis(q)}${noteEditor(q)}</div>`;
}
function finish() {
  if (!quiz) return;
  const previousDaily = state.days[today()] || 0;
  let score = 0;
  for (let id of quiz.ids) {
    let q = byId[id],
      ok = exact(quiz.answers[id] || [], q.correct);
    if (ok) score++;
    if (
      quiz.mode !== "learn" ||
      (!Object.hasOwn(quiz.checked, id) && (quiz.answers[id] || []).length)
    ) {
      let old = state.answers[id];
      state.answers[id] = {
        correct: ok,
        attempts: (old?.attempts || 0) + 1,
        last: Date.now(),
      };
      if ((quiz.answers[id] || []).length)
        state.days[today()] = (state.days[today()] || 0) + 1;
    }
  }
  review = {
    ...JSON.parse(JSON.stringify(quiz)),
    score,
    total: quiz.ids.length,
    date: new Date().toISOString(),
  };
  state.history.push({
    mode: review.mode,
    scope: review.scope,
    score,
    total: review.total,
    date: review.date,
  });
  state.active = null;
  save();
  quiz = null;
  closeModal();
  navigate("result");
  goalMilestone(previousDaily);
}
function resultPage() {
  if (!review) return statsPage();
  let exam = review.mode === "exam",
    test = review.mode === "test",
    pass = review.score >= 65;
  return (
    head(
      "Każda próba uczy czegoś nowego.",
      "Zatrzymaj się na chwilę i zobacz swój wynik.",
    ) +
    `<div class="result"><div class="scorecircle">${review.score}<small style="font:13px 'DM Sans';display:block">z ${review.total} punktów</small></div><div class="eyebrow" style="justify-content:center">${modeLabel(review.mode, review.scope).toLocaleUpperCase("pl-PL")} — KONIEC SESJI</div><h2>${exam ? (pass ? "Dobra robota. Egzamin zaliczony!" : "Wiesz już, nad czym warto popracować.") : test ? "Twój sprawdzian jest zakończony." : "Kolejny krok za Tobą."}</h2><p>${exam ? `Próg zaliczenia: 65 punktów. Twój wynik: ${review.score} / ${review.total}.` : `Poprawne odpowiedzi: ${review.score} z ${review.total} (${pct(review.score, review.total)}%). Przejrzyj zestaw i wróć do trudniejszych pytań.`}</p><div class="actions">${btn("Przejrzyj odpowiedzi", "review")}${btn("Powtórz błędne pytania", "repeat-wrong", "refresh", "secondary")}${btn("Wróć do pulpitu", "go-home", "home", "ghost")}</div></div>`
  );
}
function reviewPage() {
  return review
    ? head(
        "Zrozum swój wynik.",
        "Zielony zestaw odpowiedzi odpowiada oficjalnemu kluczowi historycznej sesji.",
      ) +
        `<div class="questions">${review.ids
          .map((id) => {
            let q = byId[id],
              a = review.answers[id] || [],
              ok = exact(a, q.correct);
            return `<article class="qrow"><div class="qmeta"><span class="badge">${ok ? "✓ Poprawnie" : "↻ Do powtórki"}</span><span>${dateLabel(q.session)} · pytanie ${q.number}</span></div><h3>${esc(q.question)}</h3><p class="muted" style="font-size:13px">Twoja odpowiedź: ${a.length ? a.map((i) => "ABC"[i]).join(", ") : "Brak odpowiedzi"}</p>${feedback(q, ok)}</article>`;
          })
          .join("")}</div>`
    : statsPage();
}
function showDetail(id) {
  detail = byId[id];
  let q = detail;
  showModal(
    modalHead("Pytanie z bazy") +
      `<div class="qmeta"><span class="badge">${esc(q.category)}</span><span>${dateLabel(q.session)} · nr ${q.number}</span></div><h3 style="line-height:1.8;margin-bottom:18px">${esc(q.question)}</h3><div class="options">${q.options.map((o, i) => `<div class="option"><span class="letter">${"ABC"[i]}</span><span>${esc(o)}</span></div>`).join("")}</div><div id="detail-key" hidden>${feedback(q, true).replace("✓ Dobra odpowiedź.", "Odpowiedzi według oficjalnego klucza")}</div><div class="actions">${bookmarkButton(q)}${btn("Pokaż poprawne odpowiedzi", "reveal-key", "check")}${btn("Ucz się tego pytania", "learn-one", "arrow", "secondary")}</div>`,
  );
}
function navigate(v) {
  if (location.hash === "#" + v) {
    view = v;
    render();
    window.scrollTo(0, 0);
  } else location.hash = v;
}
function render() {
  applyPreferences();
  let builders = {
    home,
    learn: learnPage,
    exams: examPage,
    base: basePage,
    saved: basePage,
    stats: statsPage,
    sources: sourcesPage,
    quiz: quizPage,
    result: resultPage,
    review: reviewPage,
  };
  shell((builders[view] || home)());
  document.querySelector("#app")?.setAttribute?.("aria-busy", "false");
}
function formatTime(ms) {
  let s = Math.max(0, Math.ceil(ms / 1000));
  return (
    Math.floor(s / 60)
      .toString()
      .padStart(2, "0") +
    ":" +
    (s % 60).toString().padStart(2, "0")
  );
}
function syncQuiz() {
  state.active = quiz;
  save();
}
function requestFinish() {
  let blanks = quiz.ids.filter((id) => !(quiz.answers[id] || []).length).length,
    exam = quiz.mode === "exam";
  showModal(
    modalHead(exam ? "Zakończyć egzamin?" : "Zakończyć sprawdzian?") +
      `<p>${blanks ? `Pozostało ${blanks} pytań bez odpowiedzi. Brak odpowiedzi oznacza 0 punktów za pytanie.` : "Wszystkie pytania mają zaznaczone odpowiedzi."} Po zakończeniu zobaczysz wynik i oficjalny klucz.</p><div class="actions">${btn("Wróć do pytań", "close-modal", "arrow", "secondary")}${btn("Zakończ i pokaż wynik", "finish", "check")}</div>`,
  );
}
function onAction(a, v) {
  switch (a) {
    case "theme":
      toggleTheme();
      break;
    case "settings":
      settingsDialog();
      break;
    case "help":
      helpDialog();
      break;
    case "smart-review":
      smartReview();
      break;
    case "replace-smart":
      smartReview(true);
      break;
    case "save-note":
      saveNote(v);
      break;
    case "flag-question":
      toggleFlag();
      break;
    case "learn-config":
      config("learn");
      break;
    case "exam-config":
      config("exam");
      break;
    case "random-learn":
      config("learn", "", "", true);
      break;
    case "random-test":
      config("test", "", "", true);
      break;
    case "exam-session":
      config("exam", "", v);
      break;
    case "topic":
      config("learn", CATS[Number(v)]);
      break;
    case "close-modal":
      closeModal();
      break;
    case "replace-session": {
      state.active = null;
      quiz = null;
      save();
      let [mode, cat, s, scope] = v.split("|");
      openConfig(mode, cat, s, scope === "all");
      break;
    }
    case "resume":
      quiz = state.active;
      if (!quiz) {
        toast("Brak rozpoczętej sesji.");
        break;
      }
      closeModal();
      if (quiz.mode === "exam" && quiz.deadline <= Date.now()) finish();
      else navigate("quiz");
      break;
    case "sources":
      navigate("sources");
      break;
    case "go-home":
      navigate("home");
      break;
    case "go-base":
      filter = { search: "", category: "", session: "", status: "", legal: "" };
      navigate("base");
      break;
    case "bookmark": {
      let n = state.bookmarks.indexOf(v);
      if (n < 0) state.bookmarks.push(v);
      else state.bookmarks.splice(n, 1);
      save();
      if ($("#modal").innerHTML && detail?.id === v) {
        const b = $('#modal [data-action="bookmark"]');
        b.outerHTML = bookmarkButton(detail);
      }
      render();
      toast(n < 0 ? "Pytanie dodane do zapisanych." : "Usunięto z zapisanych.");
      break;
    }
    case "detail":
      showDetail(v);
      break;
    case "reveal-key":
      $("#detail-key").hidden = false;
      $('#modal [data-action="reveal-key"]').hidden = true;
      break;
    case "learn-one":
      if (state.active) {
        closeModal();
        toast(
          "Najpierw ukończ rozpoczętą sesję lub utwórz nową w Trybie nauki.",
        );
      } else startQuiz("learn", [detail], 1);
      break;
    case "clear-filters":
      filter = { search: "", category: "", session: "", status: "", legal: "" };
      page = 1;
      render();
      break;
    case "prev-page":
      page--;
      render();
      window.scrollTo(0, 0);
      break;
    case "next-page":
      page++;
      render();
      window.scrollTo(0, 0);
      break;
    case "learn-filtered":
      if (state.active) config("learn", filter.category, filter.session);
      else startQuiz("learn", filtered(), 20);
      break;
    case "answer": {
      let q = byId[quiz.ids[quiz.index]];
      if (quiz.mode === "learn" && Object.hasOwn(quiz.checked, q.id)) break;
      let a = quiz.answers[q.id] || [];
      let n = Number(v);
      quiz.answers[q.id] = a.includes(n)
        ? a.filter((x) => x !== n)
        : [...a, n].sort();
      syncQuiz();
      render();
      break;
    }
    case "check": {
      let q = byId[quiz.ids[quiz.index]];
      if (
        quiz.mode === "learn" &&
        (quiz.answers[q.id] || []).length &&
        !Object.hasOwn(quiz.checked, q.id)
      )
        markLearn(q);
      break;
    }
    case "quiz-prev":
      quiz.index = Math.max(0, quiz.index - 1);
      syncQuiz();
      render();
      break;
    case "quiz-jump":
      quiz.index = Number(v);
      syncQuiz();
      render();
      window.scrollTo(0, 0);
      break;
    case "quiz-next":
      if (quiz.index === quiz.ids.length - 1) {
        if (quiz.mode !== "learn") requestFinish();
        else if (quiz.ids.some((id) => !Object.hasOwn(quiz.checked, id)))
          showModal(
            modalHead("Jeszcze kilka pytań przed Tobą.") +
              `<p>Nie wszystkie pytania zostały sprawdzone. Możesz wrócić do zestawu lub zakończyć naukę z obecnym wynikiem.</p><div class="actions">${btn("Wróć do pytań", "close-modal", "arrow", "secondary")}${btn("Zakończ naukę", "finish", "check")}</div>`,
          );
        else finish();
      } else {
        quiz.index++;
        syncQuiz();
        render();
        window.scrollTo(0, 0);
      }
      break;
    case "finish-dialog":
      requestFinish();
      break;
    case "finish":
      finish();
      break;
    case "leave-quiz":
      syncQuiz();
      navigate("home");
      toast(
        quiz.mode === "exam"
          ? "Egzamin zapisany. Czas nadal biegnie."
          : quiz.mode === "test"
            ? "Sprawdzian zapisany. Możesz wrócić do niego później."
            : "Sesja zapisana. Możesz wrócić do niej później.",
      );
      break;
    case "review":
      navigate("review");
      break;
    case "repeat-wrong": {
      let wrong = review.ids.filter(
        (id) => !exact(review.answers[id] || [], byId[id].correct),
      );
      if (!wrong.length)
        toast("Wszystkie odpowiedzi są poprawne. Wybierz nowy zestaw!");
      else
        startQuiz(
          "learn",
          wrong.map((id) => byId[id]),
          wrong.length,
        );
      break;
    }
    case "export": {
      let blob = new Blob(
          [
            JSON.stringify(
              {
                format: "pracownia-v1",
                exportedAt: new Date().toISOString(),
                state,
              },
              null,
              2,
            ),
          ],
          { type: "application/json" },
        ),
        url = URL.createObjectURL(blob),
        a = document.createElement("a");
      a.href = url;
      a.download = "pracownia-postep-" + today() + ".json";
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      break;
    }
    case "import":
      $("#import-file").click();
      break;
    case "reset-dialog":
      showModal(
        modalHead("Wyczyścić postęp na tym urządzeniu?") +
          `<p>Usunięte zostaną odpowiedzi, notatki, zapisane pytania, historia, ustawienia i rozpoczęta sesja. Warto wcześniej pobrać kopię postępu.</p><div class="actions">${btn("Anuluj", "close-modal", "close", "secondary")}${btn("Wyczyść postęp", "reset", "refresh", "danger")}</div>`,
      );
      break;
    case "reset":
      state = fresh();
      quiz = null;
      review = null;
      save();
      closeModal();
      render();
      toast("Postęp został wyczyszczony.");
      break;
  }
}
document.addEventListener("click", (e) => {
  let b = e.target.closest("[data-action]");
  if (b && !b.disabled) onAction(b.dataset.action, b.dataset.value);
});
document.addEventListener("submit", (e) => {
  if (e.target.id !== "config-form") return;
  e.preventDefault();
  let f = new FormData(e.target),
    mode = f.get("mode"),
    wholeBase = f.get("scope") === "all",
    session = wholeBase ? "" : f.get("session"),
    cat = wholeBase ? "" : f.get("category"),
    pool = wholeBase ? "all" : f.get("pool");
  let list = Q.filter(
    (q) =>
      (!session || q.session === session) &&
      (!cat || q.category === cat) &&
      (!pool ||
        pool === "all" ||
        (pool === "new" && !state.answers[q.id]) ||
        (pool === "wrong" && state.answers[q.id] && !correct(q)) ||
        (pool === "saved" && state.bookmarks.includes(q.id))),
  );
  if (!list.length) {
    $("#config-error").innerHTML =
      '<p style="color:#a14e4e">W tym zakresie nie ma pytań. Wybierz inny zakres.</p>';
    return;
  }
  startQuiz(
    mode,
    list,
    Number(f.get("limit") || 90),
    mode === "exam" && !!session,
    wholeBase,
  );
});
document.addEventListener("input", (e) => {
  if (e.target.id === "search") {
    filter.search = e.target.value;
    page = 1;
    let pos = e.target.selectionStart;
    render();
    $("#search").focus();
    $("#search").setSelectionRange(pos, pos);
  }
});
document.addEventListener("change", async (e) => {
  let map = {
    catfilter: "category",
    sessionfilter: "session",
    statusfilter: "status",
    legalfilter: "legal",
  };
  if (map[e.target.id]) {
    filter[map[e.target.id]] = e.target.value;
    page = 1;
    render();
  }
  if (e.target.id === "import-file") {
    let file = e.target.files[0];
    if (!file) return;
    if (file.size > 20 * 1024 * 1024) {
      toast("Kopia jest zbyt duża (maksymalnie 20 MB).");
      return;
    }
    try {
      let x = JSON.parse(await file.text());
      validateImport(x);
      window.pendingImport = x.state;
      showModal(
        modalHead("Wczytać kopię postępu?") +
          `<p>Wczytanie zastąpi obecne odpowiedzi, historię i zakładki na tym urządzeniu. Kopia zawiera ${Object.keys(x.state.answers).length} odpowiedzi i ${x.state.history.length} sesji.</p><div class="actions">${btn("Anuluj", "close-modal", "close", "secondary")}<button class="btn" id="confirm-import">Zastąp obecny postęp</button></div>`,
      );
      $("#confirm-import").onclick = () => {
        state = window.pendingImport;
        delete window.pendingImport;
        quiz = null;
        review = null;
        save();
        closeModal();
        render();
        toast("Kopia postępu została wczytana.");
      };
    } catch (err) {
      toast("Nieprawidłowy plik kopii postępu. Wybierz eksport z Pracowni.");
    }
  }
});
function validateImport(x) {
  const s = x?.state;
  if (
    x?.format !== "pracownia-v1" ||
    !s ||
    typeof s.answers !== "object" ||
    Array.isArray(s.answers) ||
    !s.answers ||
    !Array.isArray(s.bookmarks) ||
    !Array.isArray(s.history) ||
    !s.days ||
    typeof s.days !== "object"
  )
    throw Error();
  if (!s.bookmarks.every((id) => typeof id === "string" && byId[id]))
    throw Error();
  for (let [id, a] of Object.entries(s.answers))
    if (
      !byId[id] ||
      typeof a.correct !== "boolean" ||
      !Number.isSafeInteger(a.attempts) ||
      a.attempts < 1
    )
      throw Error();
  for (let h of s.history)
    if (
      !["learn", "exam", "test"].includes(h.mode) ||
      !Number.isInteger(h.score) ||
      !Number.isInteger(h.total) ||
      h.total < 1 ||
      h.score < 0 ||
      h.score > h.total ||
      !Number.isFinite(Date.parse(h.date))
    )
      throw Error();
  for (let [d, n] of Object.entries(s.days))
    if (!/^\d{4}-\d{2}-\d{2}$/.test(d) || !Number.isSafeInteger(n) || n < 0)
      throw Error();
  if (s.settings !== undefined) validateSettings(s.settings);
  if (s.notes !== undefined) {
    if (!s.notes || typeof s.notes !== "object" || Array.isArray(s.notes))
      throw Error();
    for (let [id, note] of Object.entries(s.notes))
      if (!byId[id] || typeof note !== "string" || note.length > 3000)
        throw Error();
  }
  if (s.active) {
    let a = s.active;
    if (
      !["exam", "learn", "test"].includes(a.mode) ||
      !Array.isArray(a.ids) ||
      !a.ids.length ||
      !a.ids.every((id) => byId[id]) ||
      !Number.isInteger(a.index) ||
      a.index < 0 ||
      a.index >= a.ids.length ||
      !a.answers ||
      !a.checked ||
      (a.mode === "exam" &&
        (!Number.isFinite(a.deadline) || a.ids.length !== 90))
    )
      throw Error();
    if (
      a.flags !== undefined &&
      (!Array.isArray(a.flags) ||
        !a.flags.every((id) => a.ids.includes(id)) ||
        new Set(a.flags).size !== a.flags.length)
    )
      throw Error();
    for (let [id, v] of Object.entries(a.answers))
      if (
        !a.ids.includes(id) ||
        !Array.isArray(v) ||
        new Set(v).size !== v.length ||
        !v.every((n) => [0, 1, 2].includes(n))
      )
        throw Error();
    for (let [id, v] of Object.entries(a.checked))
      if (!a.ids.includes(id) || typeof v !== "boolean") throw Error();
  }
}
document.addEventListener("keydown", (e) => {
  if (!$("#modal").innerHTML) return;
  if (e.key === "Escape") {
    closeModal();
    return;
  }
  if (e.key === "Tab") {
    let f = [
        ...$("#modal").querySelectorAll(
          "button:not([disabled]):not([hidden]),select,textarea,summary,input:not([type=hidden]),a[href]",
        ),
      ].filter((n) => n.offsetParent !== null),
      first = f[0],
      last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }
});
window.addEventListener("hashchange", () => {
  let next = location.hash.slice(1) || "home";
  if (
    ![
      "home",
      "learn",
      "exams",
      "base",
      "saved",
      "stats",
      "sources",
      "quiz",
      "result",
      "review",
    ].includes(next)
  )
    next = "home";
  view = next;
  if (view === "quiz" && !quiz) {
    quiz = state.active;
    if (!quiz) view = "home";
  }
  if (["result", "review"].includes(view) && !review) view = "stats";
  closeModal();
  render();
  window.scrollTo(0, 0);
});
setInterval(() => {
  let active = state.active;
  if (active?.mode === "exam") {
    if (active.deadline <= Date.now()) {
      quiz = active;
      finish();
      toast("Czas egzaminu upłynął. Wynik został zapisany.");
    } else if ($("#timer")) {
      $("#timer").textContent = formatTime(active.deadline - Date.now());
      $("#timer").classList.toggle(
        "low",
        active.deadline - Date.now() < 5 * 60000,
      );
    }
  }
}, 1000);
Promise.all([
  fetch("questions.json").then((r) => {
    if (!r.ok) throw Error();
    return r.json();
  }),
  fetch("legal-bases.json")
    .then((r) => {
      if (!r.ok) throw Error();
      return r.json();
    })
    .catch(() => null),
])
  .then(([data, legal]) => {
    if (legal?.schemaVersion === 1 && legal.items && legal.counts) {
      legalBases = legal.items;
      legalMeta = legal;
      legalReady = true;
    }
    Q = data.questions;
    sessions = data.sessions;
    byId = Object.fromEntries(Q.map((q) => [q.id, q]));
    try {
      validateImport({ format: "pracownia-v1", state });
    } catch (e) {
      state = fresh();
      toast("Zapisany postęp był uszkodzony. Rozpoczęto nowy zapis.");
    }
    view = location.hash.slice(1) || "home";
    if (view === "quiz") {
      quiz = state.active;
      if (!quiz) view = "home";
    }
    if (["result", "review"].includes(view)) view = "stats";
    render();
    if (state.active?.mode === "exam" && state.active.deadline <= Date.now()) {
      quiz = state.active;
      finish();
    }
  })
  .catch(() => {
    $("#app").innerHTML =
      '<div class="loaderror"><h1>Nie udało się wczytać bazy.</h1><p>Sprawdź połączenie i odśwież stronę. Zapisany postęp pozostaje w przeglądarce.</p><button class="btn" onclick="location.reload()">Spróbuj ponownie</button></div>';
  });
