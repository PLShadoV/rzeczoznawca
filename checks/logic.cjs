const vm = require("node:vm"),
  fs = require("node:fs"),
  assert = require("node:assert/strict"),
  cp = require("node:child_process");
const source =
    fs.readFileSync("dist/enhancements.js", "utf8") +
    "\n" +
    fs.readFileSync("dist/app.js", "utf8"),
  data = JSON.parse(fs.readFileSync("dist/questions.json", "utf8"));
function setup(saved, options = {}) {
  let nodes = {},
    events = {},
    store = saved ? JSON.stringify(saved) : null;
  let doc = {
    activeElement: { focus() {} },
    querySelector(s) {
      return (nodes[s] ??= {
        innerHTML: "",
        textContent: "",
        hidden: false,
        classList: { add() {}, remove() {}, toggle() {} },
        focus() {},
        querySelectorAll() {
          return [];
        },
      });
    },
    addEventListener(name, fn) {
      const previous = events[name];
      events[name] = previous
        ? (e) => {
            previous(e);
            fn(e);
          }
        : fn;
    },
    createElement() {
      return { click() {} };
    },
  };
  class TestFormData {
    constructor(form) {
      this.values = form.values;
    }
    get(key) {
      return this.values[key] ?? null;
    }
  }
  let ctx = vm.createContext({
    document: doc,
    location: { hash: "" },
    window: { scrollTo() {}, addEventListener() {} },
    localStorage: {
      getItem() {
        return store;
      },
      setItem(k, v) {
        if (options.failStorage) throw Error("Storage unavailable");
        store = v;
      },
    },
    fetch: async (path) => ({
      ok: true,
      json: async () => (path === "legal-bases.json" ? legalFixture : data),
    }),
    setInterval() {},
    setTimeout() {},
    clearTimeout() {},
    console,
    Blob,
    URL,
    FormData: TestFormData,
  });
  vm.runInContext(source, ctx);
  return {
    ctx,
    run: (s) => vm.runInContext(s, ctx),
    nodes,
    events,
    getStore: () => JSON.parse(store),
  };
}
const legalFixture = fs.existsSync("dist/legal-bases.json")
  ? JSON.parse(fs.readFileSync("dist/legal-bases.json", "utf8"))
  : {
      schemaVersion: 1,
      checkedAt: "2026-11-05",
      counts: { cited: 0, nonlegal: 0, unresolved: 3240 },
      items: {},
    };
const ready = () => new Promise((r) => setImmediate(r));
async function runLogicChecks() {
  let t = setup();
  await ready();
  assert.equal(t.run("Q.length"), 3240);
  assert.equal(t.run("sessions.length"), 36);
  assert.equal(t.run("yearsLabel()"), "2021–2026");
  assert.match(t.nodes["#app"].innerHTML, /Twoje uprawnienia/);
  for (let view of [
    "home",
    "learn",
    "exams",
    "base",
    "saved",
    "stats",
    "sources",
  ])
    t.run(`view='${view}';render()`);
  assert.equal(t.run("exact([0],[0,1])"), false);
  assert.equal(t.run("exact([1,0],[0,1])"), true);
  assert.equal(t.run("exact([0,1,2],[0,1])"), false);
  t.run("startQuiz('exam',Q.filter(q=>q.session===sessions[0].date),90,true)");
  assert.equal(t.run("quiz.ids.length"), 90);
  assert.equal(t.run("quiz.deadline-quiz.started"), 5400000);
  t.run(
    "quiz.ids.slice(0,65).forEach(id=>quiz.answers[id]=[...byId[id].correct]);finish()",
  );
  assert.equal(t.run("review.score"), 65);
  assert.equal(t.run("state.active"), null);
  assert.equal(t.run("state.history[0].score"), 65);
  assert.match(t.run("resultPage()"), /Egzamin zaliczony/);
  t.run(
    "startQuiz('exam',Q.filter(q=>q.session===sessions[1].date),90,true);quiz.ids.slice(0,64).forEach(id=>quiz.answers[id]=[...byId[id].correct]);finish()",
  );
  assert.equal(t.run("review.score"), 64);
  assert.doesNotMatch(t.run("resultPage()"), /Egzamin zaliczony/);
  t.run(
    "startQuiz('learn',Q,10);quiz.answers[quiz.ids[0]]=[...byId[quiz.ids[0]].correct];markLearn(byId[quiz.ids[0]])",
  );
  assert.equal(t.run("quiz.checked[quiz.ids[0]]"), true);
  let before = t.run("state.answers[quiz.ids[0]].attempts");
  t.run("onAction('check')");
  assert.equal(t.run("state.answers[quiz.ids[0]].attempts"), before);
  t.run("onAction('bookmark',quiz.ids[0])");
  assert.equal(t.run("state.bookmarks.length"), 1);
  assert.equal(t.getStore().bookmarks.length, 1);
  let restored = setup(t.getStore());
  await ready();
  assert.equal(restored.run("state.active.ids.length"), 10);
  assert.equal(restored.run("state.bookmarks.length"), 1);
  t.run("validateImport({format:'pracownia-v1',state})");
  assert.throws(() => t.run("validateImport({format:'bad',state})"));
  t.run(
    "state.active=null;quiz=null;startQuiz('exam',Q,90);quiz.deadline=Date.now()-1;syncQuiz()",
  );
  let expired = setup(t.getStore());
  await ready();
  assert.equal(expired.run("state.active"), null);
  assert.equal(expired.run("review.score"), 0);
  assert.equal(expired.run("state.history.length"), 3);
  // Dedicated whole-base actions and the form must ignore previous browsing filters.
  let random = setup();
  await ready();
  random.run(
    "filter={search:'las',category:CATS[0],session:sessions[0].date,status:'wrong'};onAction('random-learn')",
  );
  assert.match(random.nodes["#modal"].innerHTML, /Losowa nauka z całej bazy/);
  assert.match(random.nodes["#modal"].innerHTML, /name="scope" value="all"/);
  assert.doesNotMatch(
    random.nodes["#modal"].innerHTML,
    /name="session"|name="category"|name="pool"/,
  );
  random.events.submit({
    target: {
      id: "config-form",
      values: {
        mode: "learn",
        scope: "all",
        limit: "100",
        session: data.sessions[0].date,
        category: data.questions[0].category,
        pool: "wrong",
      },
    },
    preventDefault() {},
  });
  assert.equal(random.run("quiz.ids.length"), 100);
  assert.equal(random.run("quiz.scope"), "all");
  assert.equal(random.run("quiz.deadline"), null);
  assert.equal(random.run("new Set(quiz.ids).size"), 100);
  assert.equal(
    random.run(
      'new Set(quiz.ids.map(id=>byId[id].question+byId[id].options.join("|"))).size',
    ),
    100,
  );
  assert.equal(random.run("uniqueQuestions(Q).length<Q.length"), true);
  assert.deepEqual(
    JSON.parse(
      random.run(
        "JSON.stringify([...new Set(uniqueQuestions(Q).map(q=>q.session.slice(0,4)))].sort())",
      ),
    ),
    ["2021", "2022", "2023", "2024", "2025", "2026"],
  );
  random.run(
    "quiz.answers[quiz.ids[0]]=[...byId[quiz.ids[0]].correct];onAction('check')",
  );
  assert.match(random.run("quizPage()"), /Poprawny zestaw z klucza/);
  random.run("state=fresh();quiz=null;onAction('random-test')");
  assert.match(
    random.nodes["#modal"].innerHTML,
    /Losowy sprawdzian z całej bazy/,
  );
  random.events.submit({
    target: {
      id: "config-form",
      values: { mode: "test", scope: "all", limit: "30" },
    },
    preventDefault() {},
  });
  assert.equal(random.run("quiz.ids.length"), 30);
  assert.equal(random.run("quiz.mode"), "test");
  assert.equal(random.run("quiz.deadline"), null);
  random.run("onAction('answer','0');onAction('check')");
  assert.equal(random.run("Object.keys(state.answers).length"), 0);
  assert.equal(random.run("Object.keys(quiz.checked).length"), 0);
  assert.doesNotMatch(
    random.run("quizPage()"),
    /data-action="check"|Poprawny zestaw z klucza|class="feedback|id="timer"/,
  );
  random.run("onAction('answer','0');onAction('answer','1')");
  assert.equal(random.run("quiz.answers[quiz.ids[0]].join()"), "1");
  let testRestored = setup(random.getStore());
  await ready();
  assert.equal(testRestored.run("state.active.mode"), "test");
  assert.equal(testRestored.run("state.active.ids.length"), 30);
  assert.equal(
    testRestored.run("state.active.answers[state.active.ids[0]].join()"),
    "1",
  );
  testRestored.run("validateImport({format:'pracownia-v1',state})");
  random.run(
    "quiz.answers={};quiz.ids.slice(0,12).forEach(id=>quiz.answers[id]=[...byId[id].correct]);finish()",
  );
  assert.equal(random.run("review.score"), 12);
  assert.equal(random.run("state.history[0].mode"), "test");
  assert.equal(random.run("Object.keys(state.answers).length"), 30);
  assert.match(random.run("resultPage()"), /12 z 30 \(40%\)/);
  assert.doesNotMatch(random.run("resultPage()"), /Próg zaliczenia/);
  assert.match(random.run("reviewPage()"), /Poprawny zestaw z klucza/);
  assert.match(random.run("statsPage()"), /Losowy sprawdzian/);
  // Most recent copy wins when a question recurs, independent of input ordering.
  assert.equal(
    random.run(
      "uniqueQuestions([{question:'Pytanie',options:['A','B','C'],session:'2021-01-01',id:'old'},{question:'Pytanie',options:['A','B','C'],session:'2026-01-01',id:'new'}])[0].id",
    ),
    "new",
  );
  // Older backups and ongoing sessions remain valid after expanding the question bank.
  const oldId = "2026-09-09-1",
    oldState = {
      answers: { [oldId]: { correct: true, attempts: 2, last: 1 } },
      bookmarks: [oldId],
      history: [
        { mode: "exam", date: "2026-11-05T08:00:00Z", score: 65, total: 90 },
      ],
      days: { "2026-11-05": 1 },
      active: {
        mode: "learn",
        ids: [oldId],
        index: 0,
        answers: {},
        checked: {},
        started: 1,
        deadline: null,
      },
    };
  let legacy = setup(oldState);
  await ready();
  assert.equal(legacy.run('state.answers["2026-09-09-1"].attempts'), 2);
  assert.equal(legacy.run("state.active.ids[0]"), oldId);
  // References appear alongside revealed answers but cannot reveal answers during an exam/test.
  const legal = setup();
  await ready();
  assert.equal(legal.run("legalReady"), true);
  legal.run(
    "legalBases[Q[0].id]={status:'cited',citations:[{act:'Testowy akt prawny',provision:'art. 3 pkt 5',url:'https://eli.gov.pl/eli/DU/1994/414/ogl',evidence:'Fragment przepisu do testu wyświetlania.'}]};startQuiz('learn',[Q[0]],1)",
  );
  assert.doesNotMatch(
    legal.run("quizPage()"),
    /Testowy akt prawny|Fragment przepisu/,
  );
  legal.run(
    "quiz.answers[quiz.ids[0]]=[...byId[quiz.ids[0]].correct];onAction('check')",
  );
  assert.match(legal.run("quizPage()"), /Testowy akt prawny/);
  assert.match(legal.run("quizPage()"), /art\. 3 pkt 5/);
  legal.run("startQuiz('test',[Q[0]],1)");
  assert.doesNotMatch(
    legal.run("quizPage()"),
    /Testowy akt prawny|Fragment przepisu/,
  );
  legal.run(
    "quiz.answers[quiz.ids[0]]=[...byId[quiz.ids[0]].correct];finish()",
  );
  assert.match(legal.run("reviewPage()"), /Testowy akt prawny/);
  assert.equal(legal.run("legalURL('javascript:alert(1)')"), null);
  assert.equal(legal.run("legalURL('https://example.com/ustawa')"), null);
  legal.run("filter={search:'art. 3 pkt 5'};view='base'");
  assert.equal(legal.run("filtered().some(q=>q.id===Q[0].id)"), true);
  legal.run("filter={legal:'cited'}");
  assert.equal(
    legal.run('filtered().every(q=>legalBases[q.id]?.status===\"cited\")'),
    true,
  );
  legal.run("legalReady=false");
  assert.match(legal.run("legalBasis(Q[0])"), /Nie udało się wczytać/);
  console.log(
    "PASS: 3240 questions / 36 sessions / 2021–2026; routes; exam 65/64 threshold; immediate learning; whole-base random selection and deduplication; deferred test scoring; persistence, import, and legacy backups.",
  );
}
module.exports = { setup, ready, runLogicChecks };
if (require.main === module)
  runLogicChecks().catch((e) => {
    console.error(e);
    process.exit(1);
  });
