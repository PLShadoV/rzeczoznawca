"use strict";
const assert = require("node:assert/strict"),
  fs = require("node:fs"),
  path = require("node:path"),
  vm = require("node:vm");
const { setup, ready } = require("./logic.cjs");
async function personalTools() {
  const t = setup();
  await ready();
  assert.equal(t.run("preferences().dailyGoal"), 20);
  assert.equal(t.run("validCalendarDate('2028-02-29')"), true);
  assert.equal(t.run("validCalendarDate('2026-02-29')"), false);
  assert.match(t.run("dailyDashboard()"), /Jeszcze 20 pytań/);
  t.events.submit({
    target: {
      id: "settings-form",
      values: {
        theme: "dark",
        textSize: "large",
        dailyGoal: "35",
        examDate: "2028-02-29",
      },
    },
    preventDefault() {},
  });
  assert.equal(t.run("preferences().theme"), "dark");
  assert.equal(t.run("preferences().dailyGoal"), 35);
  assert.match(t.run("home()"), /Jeszcze 35 pytań/);
  t.run("onAction('theme')");
  assert.equal(t.run("preferences().theme"), "light");
  assert.throws(() =>
    t.run(
      "validateSettings({theme:'evil',textSize:'normal',dailyGoal:20,examDate:''})",
    ),
  );
  assert.throws(() =>
    t.run(
      "validateSettings({theme:'light',textSize:'normal',dailyGoal:0,examDate:''})",
    ),
  );
  const id = t.run("Q[0].id");
  t.run("startQuiz('learn',[Q[0]],1)");
  t.nodes["#note-" + id] = {
    value: "Moja notatka <script>alert(1)</script> & obliczenia.",
  };
  t.run(`saveNote(${JSON.stringify(id)})`);
  assert.match(t.run(`state.notes[${JSON.stringify(id)}]`), /Moja notatka/);
  assert.doesNotMatch(t.run("quizPage()"), /Moja notatka/);
  t.run(
    'quiz.answers[quiz.ids[0]]=[...byId[quiz.ids[0]].correct];onAction("check")',
  );
  assert.match(t.run("quizPage()"), /Moja notatka &lt;script&gt;/);
  assert.doesNotMatch(t.run("quizPage()"), /<script>alert/);
  t.run("toggleFlag()");
  assert.equal(t.run("quiz.flags.length"), 1);
  assert.match(t.run("quizPage()"), /oznaczone do przejrzenia/);
  const restored = setup(t.getStore());
  await ready();
  assert.equal(
    restored.run('state.notes[Q[0].id].includes("Moja notatka")'),
    true,
  );
  assert.equal(restored.run("state.active.flags.length"), 1);
  assert.equal(restored.run("preferences().dailyGoal"), 35);
  restored.run("validateImport({format:'pracownia-v1',state})");
  assert.throws(() =>
    restored.run(
      "validateImport({format:'pracownia-v1',state:{...state,notes:{unknown:'bad'}}})",
    ),
  );
  assert.throws(() =>
    restored.run(
      "validateImport({format:'pracownia-v1',state:{...state,active:{...state.active,flags:['unknown']}}})",
    ),
  );
  t.run("startQuiz('test',[Q[0]],1)");
  assert.doesNotMatch(t.run("quizPage()"), /Moja notatka/);
  t.run("finish()");
  assert.match(t.run("reviewPage()"), /Moja notatka &lt;script&gt;/);
  const review = setup();
  await ready();
  review.run(
    "state.answers[Q[0].id]={correct:false,attempts:1,last:Date.now()};state.answers[Q[1].id]={correct:true,attempts:1,last:Date.now()};smartReview()",
  );
  assert.equal(review.run("quiz.ids.length"), 1);
  assert.equal(review.run("quiz.ids[0]===Q[0].id"), true);
  const original = review.run("JSON.stringify(state.active)");
  review.run("smartReview()");
  assert.equal(review.run("JSON.stringify(state.active)"), original);
  assert.match(review.nodes["#modal"].innerHTML, /Kontynuuj sesję/);
  const keys = setup();
  await ready();
  keys.run("startQuiz('learn',[Q[0],Q[1]],2);view='quiz'");
  const key = (key) =>
    keys.events.keydown({
      key,
      target: { tagName: "BODY" },
      preventDefault() {},
    });
  key("a");
  assert.equal(keys.run("quiz.answers[quiz.ids[0]].join()"), "0");
  key("f");
  assert.equal(keys.run("quiz.flags.length"), 1);
  key("Enter");
  assert.equal(keys.run("Object.hasOwn(quiz.checked,quiz.ids[0])"), true);
  key("ArrowRight");
  assert.equal(keys.run("quiz.index"), 1);
  keys.events.keydown({
    key: "b",
    target: { tagName: "TEXTAREA" },
    preventDefault() {
      throw Error("Do not capture typing");
    },
  });
  assert.equal(keys.run("quiz.answers[quiz.ids[1]]"), undefined);
  const a = t.run("activityChart()");
  assert.match(a, /ostatnie 14 dni/);
  assert.match(a, /role="img"/);
  const limited = setup(null, { failStorage: true });
  await ready();
  const limitedId = limited.run("Q[0].id");
  limited.nodes["#note-" + limitedId] = { value: "Notatka w pamięci" };
  limited.run(`saveNote(${JSON.stringify(limitedId)})`);
  assert.match(
    limited.nodes["#toast"].textContent,
    /Zapis trwały jest niedostępny/,
  );
  assert.doesNotMatch(limited.nodes["#toast"].textContent, /Notatka zapisana/);
  const goal = setup();
  await ready();
  goal.run(
    "state.settings={...defaultSettings(),dailyGoal:200};state.days[today()]=199",
  );
  assert.doesNotMatch(goal.run("dailyDashboard()"), /Cel osiągnięty/);
  assert.match(goal.run("dailyDashboard()"), /Jeszcze 1 pytanie/);
  goal.run("state.days={};startQuiz('exam',Q,90);finish()");
  assert.equal(goal.run("state.days[today()]||0"), 0);
  console.log(
    "PASS: settings, valid calendar dates, daily goals, notes escaped and included in backups, flags, legacy imports, targeted revision, keyboard shortcuts, and chart.",
  );
}
async function offlineWorker() {
  const handlers = {},
    store = new Map(),
    cacheNames = new Set(["pracownia:/another/:0", "pracownia:/repo/:0"]);
  let online = true,
    claimed = false;
  const cache = {
    async addAll(requests) {
      for (const r of requests)
        store.set(r.url, new Response("cached:" + new URL(r.url).pathname));
    },
    async put(req, res) {
      store.set(typeof req === "string" ? req : req.url, res);
    },
    async match(req) {
      const key = typeof req === "string" ? req : req.url;
      const found = [...store.keys()].find(
        (x) => new URL(x).pathname === new URL(key).pathname,
      );
      return found ? store.get(found).clone() : undefined;
    },
  };
  const context = vm.createContext({
    self: {
      registration: { scope: "https://example.com/repo/" },
      location: { origin: "https://example.com" },
      clients: {
        async claim() {
          claimed = true;
        },
      },
      addEventListener(n, f) {
        handlers[n] = f;
      },
      skipWaiting() {},
    },
    caches: {
      async open(n) {
        cacheNames.add(n);
        return cache;
      },
      async keys() {
        return [...cacheNames];
      },
      async delete(n) {
        cacheNames.delete(n);
      },
    },
    URL,
    Request,
    Response,
    Set,
    fetch: async (req) => {
      if (!online) throw Error("offline");
      return new Response("fresh:" + new URL(req.url).pathname);
    },
  });
  vm.runInContext(fs.readFileSync("dist/sw.js", "utf8"), context);
  let job;
  handlers.install({
    waitUntil(p) {
      job = p;
    },
  });
  await job;
  assert(store.has("https://example.com/repo/questions.json"));
  assert(store.has("https://example.com/repo/legal-bases.json"));
  assert(store.has("https://example.com/repo/assets/fonts/fonts.css"));
  for (const url of store.keys())
    assert(new URL(url).pathname.startsWith("/repo/"));
  handlers.activate({
    waitUntil(p) {
      job = p;
    },
  });
  await job;
  assert.equal(claimed, true);
  assert(cacheNames.has("pracownia:/another/:0"));
  assert(!cacheNames.has("pracownia:/repo/:0"));
  const request = async (url) => {
    let response;
    handlers.fetch({
      request: new Request(url),
      respondWith(p) {
        response = p;
      },
    });
    return response ? await response : null;
  };
  online = false;
  const cached = await request("https://example.com/repo/questions.json");
  assert.equal(cached.status, 200);
  assert.match(await cached.text(), /cached:\/repo\/questions/);
  assert.equal(await request("https://eli.gov.pl/some-act"), null);
  assert.equal(await request("https://example.com/api/private"), null);
  online = true;
  assert.match(
    await (await request("https://example.com/repo/legal-bases.json")).text(),
    /cached:/,
  );
  store.delete("https://example.com/repo/legal-bases.json");
  assert.match(
    await (await request("https://example.com/repo/legal-bases.json")).text(),
    /fresh:/,
  );
  const put = cache.put;
  cache.put = async () => {
    throw Error("quota");
  };
  store.delete("https://example.com/repo/questions.json");
  assert.match(
    await (await request("https://example.com/repo/questions.json")).text(),
    /fresh:/,
  );
  cache.put = put;
  online = false;
  assert.match(
    await (await request("https://example.com/repo/legal-bases.json")).text(),
    /fresh:/,
  );
  console.log(
    "PASS: project-subdirectory offline cache, both datasets and fonts, network refresh, and isolation from other apps/external acts.",
  );
}
function assets() {
  const dist = path.resolve("dist"),
    index = fs.readFileSync("dist/index.html", "utf8");
  for (const [, ref] of index.matchAll(/(?:src|href)="([^"]+)"/g)) {
    if (ref.startsWith("#") || /^https?:/.test(ref)) continue;
    assert(
      !ref.startsWith("/"),
      "Asset must work under GitHub Pages subdirectories: " + ref,
    );
    assert(fs.existsSync(path.join(dist, ref)), ref);
  }
  const css = fs.readFileSync("dist/assets/fonts/fonts.css", "utf8");
  for (const [, ref] of css.matchAll(/url\(['"]?([^)'"\s]+)/g))
    assert(fs.existsSync(path.join(dist, "assets/fonts", ref)), ref);
  assert(
    !/fonts\.googleapis\.com/.test(fs.readFileSync("dist/style.css", "utf8")),
  );
  const manifest = JSON.parse(
    fs.readFileSync("dist/manifest.webmanifest", "utf8"),
  );
  assert.equal(manifest.start_url, "./");
  assert.equal(manifest.scope, "./");
  for (const icon of manifest.icons)
    assert(fs.existsSync(path.join(dist, icon.src)), icon.src);
  for (const name of [
    "app.js",
    "enhancements.js",
    "bootstrap.js",
    "offline.js",
    "index.html",
  ])
    assert(
      !/appgprj_|chatgpt\.site|art_v2_/.test(
        fs.readFileSync("dist/" + name, "utf8"),
      ),
      name + " contains hosting identity",
    );
  assert(fs.existsSync("docs/GITHUB.md"));
  assert(fs.existsSync(".github/workflows/pages.yml"));
  console.log(
    "PASS: relative runtime assets, local fonts/icons, PWA manifest, and no platform-bound hosting identifiers in the app.",
  );
}
(async () => {
  assets();
  await personalTools();
  await offlineWorker();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
