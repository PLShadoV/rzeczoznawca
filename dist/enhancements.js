"use strict";

// Optional personal tools. Historical questions, keys and grading remain in app.js.
function defaultSettings() {
  return { theme: "light", textSize: "normal", dailyGoal: 20, examDate: "", shuffleAnswers: true };
}
function preferences() {
  return { ...defaultSettings(), ...(state.settings || {}) };
}
function validCalendarDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const d = new Date(value + "T12:00:00Z");
  return Number.isFinite(d.getTime()) && d.toISOString().slice(0, 10) === value;
}
function validateSettings(value) {
  if (!value || typeof value !== "object" || Array.isArray(value))
    throw Error("settings");
  if (
    !["light", "dark"].includes(value.theme) ||
    !["normal", "large"].includes(value.textSize)
  )
    throw Error("appearance");
  if (
    !Number.isInteger(value.dailyGoal) ||
    value.dailyGoal < 5 ||
    value.dailyGoal > 200
  )
    throw Error("goal");
  if (value.examDate !== "" && !validCalendarDate(value.examDate))
    throw Error("date");
  if (value.shuffleAnswers !== undefined && typeof value.shuffleAnswers !== "boolean")
    throw Error("shuffle");
}
function applyPreferences() {
  const p = preferences();
  if (document.documentElement) {
    document.documentElement.dataset.theme = p.theme;
    document.documentElement.dataset.textSize = p.textSize;
    document.documentElement.style.colorScheme = p.theme;
  }
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute?.("content", p.theme === "dark" ? "#152c26" : "#285a47");
}
function toggleTheme() {
  state.settings = {
    ...preferences(),
    theme: preferences().theme === "dark" ? "light" : "dark",
  };
  save();
  render();
}
function settingsDialog() {
  const p = preferences();
  showModal(
    modalHead("Urządź swoją pracownię") +
      `<p>Dopasuj wygląd i rytm nauki. Ustawienia zapisują się na tym urządzeniu razem z postępem.</p><form id="settings-form" class="form"><div class="row"><label>Wygląd<select name="theme">${opts(
        [
          { value: "light", label: "Jasny — papier i zieleń" },
          { value: "dark", label: "Nocny — spokojna nauka" },
        ],
        p.theme,
      )}</select></label><label>Tekst pytań i odpowiedzi<select name="textSize">${opts(
        [
          { value: "normal", label: "Standardowy" },
          { value: "large", label: "Większy" },
        ],
        p.textSize,
      )}</select></label></div><label>Kolejność odpowiedzi w nauce, sprawdzianach i egzaminach<select name="shuffleAnswers">${opts(
        [
          { value: "on", label: "Losowa — poprawna odpowiedź raz pod A, raz pod B lub C" },
          { value: "off", label: "Jak w oryginalnym arkuszu" },
        ],
        p.shuffleAnswers ? "on" : "off",
      )}</select></label><p class="field-hint">Losowanie zmienia tylko litery i kolejność wariantów — każda odpowiedź zachowuje swoją treść, a punktacja wynika z oficjalnego klucza. Dotyczy sesji rozpoczętych po zmianie.</p><label>Cel dzienny — sprawdzone pytania<input type="number" name="dailyGoal" min="5" max="200" step="1" value="${p.dailyGoal}" required></label><label>Twój termin egzaminu (opcjonalnie)<input type="date" name="examDate" value="${esc(p.examDate)}"></label><p class="field-hint">To Twój własny plan, nie kalendarz ministerstwa. Obliczenia planu dotyczą pytań w arkuszach, w tym powtórzeń między sesjami.</p><div id="settings-error" role="alert"></div><div class="actions">${btn("Anuluj", "close-modal", "close", "secondary")}<button type="submit" class="btn">Zapisz ustawienia ${I("check")}</button></div></form>`,
  );
}
function questionCount(n) {
  const mod = n % 100;
  return (
    n +
    " " +
    (n === 1
      ? "pytanie"
      : n % 10 >= 2 && n % 10 <= 4 && !(mod >= 12 && mod <= 14)
        ? "pytania"
        : "pytań")
  );
}
function daysUntil(date) {
  if (!date || !validCalendarDate(date)) return null;
  const utc = (s) => {
    const [y, m, d] = s.split("-").map(Number);
    return Date.UTC(y, m - 1, d);
  };
  return Math.round((utc(date) - utc(today())) / 86400000);
}
function streakDays() {
  const d = new Date();
  if (!state.days[today()]) d.setDate(d.getDate() - 1);
  let count = 0;
  while (count < 3650 && state.days[d.toLocaleDateString("sv-SE")]) {
    count++;
    d.setDate(d.getDate() - 1);
  }
  return count;
}
function wrongQuestions() {
  return uniqueQuestions(
    Q.filter((q) => state.answers[q.id]?.correct === false),
  );
}
function dailyDashboard() {
  const p = preferences(),
    done = state.days[today()] || 0,
    progress = Math.min(100, (done / p.dailyGoal) * 100),
    reached = done >= p.dailyGoal;
  const left = daysUntil(p.examDate),
    remaining = Math.max(0, Q.length - stats().done),
    wrong = wrongQuestions().length;
  const planTitle =
    left === null
      ? "Zaplanuj swój egzamin"
      : left < 0
        ? "Zaktualizuj swój termin"
        : left === 0
          ? "Dzisiaj Twój egzamin"
          : `${left} dni do Twojego celu`;
  const planText =
    left === null
      ? "Wybierz datę i zobacz, jak rozłożyć materiał."
      : left < 0
        ? "Twój zapisany termin już minął. Możesz ustawić kolejny."
        : left === 0
          ? "Zaufaj wykonanej pracy. Powodzenia!"
          : remaining
            ? `Do przejrzenia ${remaining} pytań w arkuszach — około ${Math.ceil(remaining / left)} dziennie.`
            : "Cała baza została przerobiona. To dobry moment na powtórkę.";
  return `<section class="daily-dashboard" aria-label="Twój plan nauki"><article class="goal-card"><div class="goal-ring ${reached ? "complete" : ""}" style="--progress:${progress}%" role="img" aria-label="Dzienny cel: ${done} z ${p.dailyGoal} pytań"><span><b>${done}</b><small>/ ${p.dailyGoal}</small></span></div><div><div class="eyebrow">TWÓJ DZISIEJSZY KROK</div><h3>${reached ? "Cel osiągnięty. Dobra robota!" : `Jeszcze ${questionCount(Math.max(0, p.dailyGoal - done))} do celu`}</h3><p>${streakDays() ? `Seria nauki: ${streakDays()} dni` : "Mały krok dzisiaj, większa pewność jutro."}</p><button class="textlink" data-action="settings">Zmień cel ${I("chevron")}</button></div></article><article class="plan-card"><div class="mini-icon">${I("calendar")}</div><div><h3>${planTitle}</h3><p>${planText}</p><button class="textlink" data-action="settings">${left === null ? "Ustaw termin" : "Edytuj plan"} ${I("chevron")}</button></div></article><article class="recommend-card"><div class="mini-icon">${I("refresh")}</div><div><h3>${wrong ? `${questionCount(wrong)} do powtórki` : "Zbuduj swój rytm nauki"}</h3><p>${wrong ? "Wróć do błędnych odpowiedzi. Zestaw dobierzemy z Twojego postępu." : "Zacznij od krótkiej sesji. Kolejne kroki podpowie Twój postęp."}</p><button class="textlink" data-action="smart-review">${wrong ? "Powtórz trudne pytania" : "Zacznij krótką naukę"} ${I("arrow")}</button></div></article></section>`;
}
function smartReview(replace = false) {
  if (state.active && !replace) {
    showModal(
      modalHead("Wrócić do rozpoczętej sesji?") +
        `<p>Masz już zapisany zestaw. Możesz go kontynuować albo rozpocząć nową powtórkę. Nowa sesja zastąpi poprzedni zestaw; sprawdzone odpowiedzi pozostaną w postępie.</p><div class="actions">${btn("Kontynuuj sesję", "resume")}${btn("Nowa powtórka", "replace-smart", "refresh", "secondary")}</div>`,
    );
    return;
  }
  if (replace) {
    state.active = null;
    quiz = null;
    save();
  }
  const wrong = wrongQuestions();
  const unseen = Q.filter((q) => !state.answers[q.id]);
  startQuiz(
    "learn",
    wrong.length ? wrong : unseen.length ? unseen : Q,
    20,
    false,
    !wrong.length,
  );
}
function activityChart() {
  const days = [],
    d = new Date();
  for (let i = 13; i >= 0; i--) {
    const day = new Date(d);
    day.setDate(day.getDate() - i);
    const key = day.toLocaleDateString("sv-SE");
    days.push({
      key,
      count: state.days[key] || 0,
      label: day.toLocaleDateString("pl-PL", {
        day: "numeric",
        month: "short",
      }),
    });
  }
  const max = Math.max(preferences().dailyGoal, ...days.map((d) => d.count)),
    total = days.reduce((sum, d) => sum + d.count, 0);
  return `<section class="panel activity-panel"><div class="sectiontitle"><div><h2>Małe kroki tworzą postęp</h2><p>Twoje ostatnie 14 dni · ${total} sprawdzonych pytań</p></div><span class="pill">${I("spark")} ${streakDays()} dni serii</span></div><div class="activity-chart" role="img" aria-label="Sprawdzone pytania w ostatnich 14 dniach: ${days.map((d) => d.label + ": " + d.count).join("; ")}">${days.map((d, i) => `<div class="activity-day ${d.count >= preferences().dailyGoal ? "met" : ""}" title="${d.label}: ${d.count} pytań"><span>${d.count || ""}</span><div class="activity-track"><i style="height:${d.count ? Math.max(5, (d.count / max) * 100) : 3}%"></i></div><small>${i % 2 === 0 || i === 13 ? esc(d.label) : "&nbsp;"}</small></div>`).join("")}</div><p class="field-hint">Złoty kolor oznacza osiągnięcie obecnego celu dziennego. Wykres liczy sprawdzone odpowiedzi, w tym powtórki.</p></section>`;
}
function noteEditor(q) {
  const value = state.notes?.[q.id] || "";
  return `<details class="note-editor" ${value ? "open" : ""}><summary>${I("note")} ${value ? "Twoja notatka do pytania" : "Dodaj własną notatkę"}${value ? `<span class="note-saved">${storageOK ? "Zapisana" : "W tej sesji"}</span>` : ""}</summary><label for="note-${q.id}">Twoje skojarzenia, obliczenia lub ważny fragment przepisu</label><textarea id="note-${q.id}" rows="4" maxlength="3000" placeholder="Zapisz to, co pomoże Ci przy następnej powtórce…">${esc(value)}</textarea><div class="note-actions"><span>Do 3000 znaków · tylko na tym urządzeniu</span><button class="btn secondary" data-action="save-note" data-value="${q.id}">Zapisz notatkę ${I("check")}</button></div></details>`;
}
function saveNote(id) {
  if (!byId[id]) return;
  const field = document.querySelector("#note-" + id);
  if (!field) return;
  const value = String(field.value || "").trim();
  if (value.length > 3000) {
    toast("Notatka może mieć do 3000 znaków.");
    return;
  }
  state.notes ||= {};
  if (value) state.notes[id] = value;
  else delete state.notes[id];
  const saved = save();
  toast(
    saved
      ? value
        ? "Notatka zapisana."
        : "Notatka usunięta."
      : "Notatka jest dostępna w tej sesji. Zapis trwały jest niedostępny — pobierz kopię w Statystykach.",
  );
}
function flagButton(q) {
  const flagged = (quiz?.flags || []).includes(q.id);
  return `<button class="iconbtn ${flagged ? "flagged" : ""}" data-action="flag-question" aria-pressed="${flagged}" aria-label="${flagged ? "Usuń oznaczenie do przejrzenia" : "Oznacz do przejrzenia przed końcem"}" title="${flagged ? "Oznaczone do przejrzenia" : "Wrócę do tego pytania"}">${I("flag")}</button>`;
}
function toggleFlag() {
  if (!quiz) return;
  const id = quiz.ids[quiz.index];
  quiz.flags ||= [];
  quiz.flags = quiz.flags.includes(id)
    ? quiz.flags.filter((v) => v !== id)
    : [...quiz.flags, id];
  syncQuiz();
  render();
}
function goalMilestone(previous) {
  const goal = preferences().dailyGoal;
  if (previous < goal && (state.days[today()] || 0) >= goal)
    toast("Dzienny cel osiągnięty. Dobra robota!");
}
function helpDialog() {
  showModal(
    modalHead("Dobrze mieć wszystko pod ręką") +
      `<div class="help-grid"><article><h3>${I("book")} Nauka i powtórki</h3><p>Wybierz zakres lub losuj z całej bazy. Po zaznaczeniu wszystkich poprawnych wariantów sprawdź odpowiedź, przeczytaj przypis prawny i dodaj własną notatkę.</p></article><article><h3>${I("exam")} Sprawdzian i egzamin</h3><p>Sprawdzian nie ma limitu czasu. Egzamin to 90 pytań w 90 minut, z progiem 65 punktów. Flaga oznacza pytanie, do którego chcesz wrócić. Wynik i podstawy prawne zobaczysz na końcu.</p></article><article><h3>${I("shield")} Twój postęp</h3><p>Postęp, notatki i ustawienia zostają w tej przeglądarce. Przed zmianą urządzenia lub adresu strony pobierz kopię w Statystykach. Możesz ją potem wczytać.</p></article><article><h3>${I("download")} Nauka bez połączenia</h3><p>Po pierwszym pełnym wczytaniu przez HTTPS aplikacja może zapisać się do pracy offline. Urzędowe PDF-y i strony aktów prawnych nadal wymagają internetu. Instalację na ekranie głównym wybierzesz z menu przeglądarki.</p></article></div><section class="shortcuts"><h3>Skróty podczas rozwiązywania</h3><p><kbd>A</kbd><kbd>B</kbd><kbd>C</kbd> lub <kbd>1</kbd><kbd>2</kbd><kbd>3</kbd> — zaznacz wariant</p><p><kbd>Enter</kbd> — sprawdź odpowiedź lub przejdź dalej</p><p><kbd>←</kbd><kbd>→</kbd> — nawiguj między pytaniami &nbsp; <kbd>F</kbd> — oznacz do przejrzenia</p><p class="field-hint">Skróty nie działają podczas pisania notatki ani w otwartym oknie dialogowym.</p></section><div class="actions">${btn("Rozumiem", "close-modal", "check")}</div>`,
  );
}
function networkBadge() {
  return typeof navigator !== "undefined" && navigator.onLine === false
    ? '<span class="offline-badge">Tryb offline</span>'
    : "";
}

// Settings and keyboard handling are independent of the question and law datasets.
document.addEventListener("submit", (e) => {
  if (e.target.id !== "settings-form") return;
  e.preventDefault();
  const f = new FormData(e.target);
  const next = {
    theme: f.get("theme"),
    textSize: f.get("textSize"),
    dailyGoal: Number(f.get("dailyGoal")),
    examDate: f.get("examDate") || "",
    shuffleAnswers: f.get("shuffleAnswers") !== "off",
  };
  try {
    validateSettings(next);
  } catch {
    $("#settings-error").textContent =
      "Sprawdź dane: cel to 5–200 pytań, a termin musi być poprawną datą.";
    return;
  }
  state.settings = next;
  const saved = save();
  closeModal();
  render();
  toast(
    saved
      ? "Twoja pracownia jest gotowa."
      : "Ustawienia działają w tej sesji. Zapis trwały jest niedostępny — pobierz kopię w Statystykach.",
  );
});
document.addEventListener("keydown", (e) => {
  if (
    typeof quiz === "undefined" ||
    view !== "quiz" ||
    !quiz ||
    $("#modal").innerHTML ||
    e.ctrlKey ||
    e.metaKey ||
    e.altKey ||
    e.repeat
  )
    return;
  const target = e.target;
  if (
    target?.isContentEditable ||
    /^(INPUT|TEXTAREA|SELECT|BUTTON|A)$/.test(target?.tagName || "")
  )
    return;
  const key = e.key.toLocaleLowerCase("pl-PL"),
    map = { a: 0, b: 1, c: 2, 1: 0, 2: 1, 3: 2 };
  if (Object.hasOwn(map, key)) {
    e.preventDefault();
    // Keys pick the displayed position; translate it to the original option index.
    const q = byId[quiz.ids[quiz.index]];
    onAction("answer", String(answerOrder(q, quiz)[map[key]]));
    return;
  }
  if (key === "f") {
    e.preventDefault();
    toggleFlag();
    return;
  }
  if (key === "arrowleft" || key === "arrowright") {
    const next = Math.max(
      0,
      Math.min(
        quiz.ids.length - 1,
        quiz.index + (key === "arrowleft" ? -1 : 1),
      ),
    );
    e.preventDefault();
    onAction("quiz-jump", String(next));
    return;
  }
  if (key === "enter") {
    e.preventDefault();
    const id = quiz.ids[quiz.index];
    if (quiz.mode === "learn" && !Object.hasOwn(quiz.checked, id))
      onAction("check");
    else onAction("quiz-next");
  }
});
document.addEventListener("click", (e) => {
  if (!e.target.closest?.(".skip-link")) return;
  e.preventDefault();
  const main = document.querySelector("#main-content");
  main?.focus?.();
  main?.scrollIntoView?.({ block: "start" });
});
