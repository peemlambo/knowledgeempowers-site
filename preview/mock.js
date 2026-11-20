/* PREVIEW ONLY: a pretend back office, so the new look can be tried without a real code. Any code opens. */
(function () {
  var cache = {};
  function get(f) { return cache[f] || (cache[f] = fetch('/preview/' + f).then(function (r) { return r.json(); })); }
  var T = [['whole-numbers',1,'Whole numbers and place value','Grades 4–7',1],['calculating',2,'Calculating with whole numbers','Grades 4–7',1],['factors',3,'Multiples, factors and prime numbers','Grades 4–9',1],['integers',4,'Integers','Grades 6–9',1],['fractions',14,'Fractions','Grades 4–9',2],['decimals',15,'Decimals','Grades 5–9',2],['ratio',17,'Ratio, rate and proportion','Grades 6–9',3],['probability',27,'Probability','Grades 4–9',4]];
  var api = {
    signIn: function () { return Promise.resolve({ ok: true, code: 'KE-DEMO-001', name: 'Lerato', ends: '30 Nov 2027',
      terms: { 1: 'Term 1 · January to March', 2: 'Term 2 · April to June', 3: 'Term 3 · July to September', 4: 'Term 4 · October to December', 5: 'Grades 10 to 12' },
      topics: T.map(function (a) { return { key: a[0], no: a[1], title: a[2], grades: a[3], term: a[4], ready: true, allowed: a[0] !== 'probability' }; }) }); },
    openTopic: function (code, dev, key) { if (key !== 'fractions') return Promise.resolve({ ok: false, msg: 'In this preview only Fractions opens.' });
      return get('wb.json').then(function (w) { return { ok: true, html: w.engine, data: w.fractions, name: 'Lerato', ends: '30 Nov 2027', code: 'KE-DEMO-001' }; }); },
    openPack: function () { return get('ex.json').then(function (x) { return { ok: true, html: x.pack }; }); }
  };
  function runner(ok, bad) {
    return new Proxy({}, { get: function (_, k) {
      if (k === 'withSuccessHandler') return function (f) { return runner(f, bad); };
      if (k === 'withFailureHandler') return function (f) { return runner(ok, f); };
      return function () { var a = arguments; setTimeout(function () { (api[k] ? api[k].apply(null, a) : Promise.resolve({ ok: false, msg: 'Not in the preview.' })).then(ok, bad); }, 400); };
    } });
  }
  window.google = { script: { run: runner(null, null) } };
})();
