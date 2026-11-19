/* Talks to the Google Apps Script back office from a normal web page.
   Works like google.script.run: google.script.run.withSuccessHandler(fn).someFunction(args) */
(function () {
  function call(api, name, args, ok, bad) {
    fetch(api, { method: 'POST', body: JSON.stringify({ fn: name, args: args }) })
      .then(function (r) { return r.json(); })
      .then(function (r) { if (ok) ok(r); })
      .catch(function (e) { if (bad) bad(e); });
  }
  function runner(ok, bad) {
    return new Proxy({}, { get: function (_, k) {
      if (k === 'withSuccessHandler') return function (f) { return runner(f, bad); };
      if (k === 'withFailureHandler') return function (f) { return runner(ok, f); };
      if (k === 'withUserObject') return function () { return runner(ok, bad); };
      return function () { call(window.KE_API, k, [].slice.call(arguments), ok, bad); };
    } });
  }
  window.google = { script: { run: runner(null, null) } };
})();
