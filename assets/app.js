/* KnowledgeEmpowers apps (online workbooks and exam packs)
   KEApp.bar(...)      one slim top bar: logo, title, a few buttons, the learner's name and Sign out
   KEApp.stepper(...)  shows the questions on a page one at a time, with Previous and Next
   KEApp.pack()        sets both up inside an exam pack */
(function () {
  if (window.KEApp) return;
  var d = document;
  var I = {
    topics: '<path d="M4 6h16M4 12h16M4 18h10"/>',
    write: '<path d="M4 20h4L19 9l-4-4L4 16v4z"/><path d="M13.5 6.5l4 4"/>',
    full: '<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>',
    unfull: '<path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5"/>',
    text: '<path d="M4 18l5-12 5 12M5.8 14h6.4M16 18l2.5-6 2.5 6M16.8 16h3.4"/>',
    save: '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
    report: '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
    formula: '<path d="M18 5H7l6 7-6 7h11"/>',
    progress: '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    home: '<path d="M4 11l8-7 8 7v9h-5v-6H9v6H4z"/>',
    more: '<circle cx="5" cy="12" r="1.3"/><circle cx="12" cy="12" r="1.3"/><circle cx="19" cy="12" r="1.3"/>'
  };
  function svg(k) { return '<svg viewBox="0 0 24 24" aria-hidden="true">' + (I[k] || '') + '</svg>'; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ---------- full screen ---------- */
  function isFull() { return !!(d.fullscreenElement || d.webkitFullscreenElement); }
  var canFull = !!(d.documentElement.requestFullscreen || d.documentElement.webkitRequestFullscreen) && d.fullscreenEnabled !== false;
  function toggleFull() {
    try { if (isFull()) (d.exitFullscreen || d.webkitExitFullscreen).call(d);
          else { var r = d.documentElement; (r.requestFullscreen || r.webkitRequestFullscreen).call(r); } } catch (e) {}
  }

  /* ---------- the top bar ---------- */
  var bar = null, menu = null, cfg = null;
  function setBar(o) {
    cfg = o;
    d.documentElement.classList.add('kb-html'); d.body.classList.add('kb-on');
    if (!bar) { bar = d.createElement('header'); bar.id = 'kbar'; }
    if (!menu) { menu = d.createElement('div'); menu.className = 'kb-menu'; menu.hidden = true; }
    if (!bar.isConnected) d.body.insertBefore(bar, d.body.firstChild);
    if (!menu.isConnected) d.body.appendChild(menu);
    var items = (o.items || []).slice();
    if (o.write !== false) items.push({ k: 'write', label: 'Write', icon: 'write', act: function () { if (window.__ink) window.__ink.open(); } });
    if (canFull) items.push({ k: 'full', label: 'Full screen', icon: 'full', minor: true, act: toggleFull });
    var h = '<a class="kb-logo" href="/" aria-label="KnowledgeEmpowers home"><img src="/assets/img/logo.svg" alt="KnowledgeEmpowers"></a><span class="kb-sep"></span>' +
      '<button class="kb-title" type="button">' + esc(o.title) + (o.sub ? '<small>' + esc(o.sub) + '</small>' : '') + '</button><nav class="kb-acts" aria-label="Workbook tools">';
    items.forEach(function (it, i) {
      h += '<button type="button" class="kb-b' + (it.minor ? ' minor' : '') + '" data-i="' + i + '" title="' + esc(it.label) + '">' + svg(it.icon) + '<span>' + esc(it.label) + '</span></button>';
    });
    h += '<button type="button" class="kb-b kb-more" aria-label="More" aria-expanded="false">' + svg('more') + '</button></nav>';
    if (o.user) h += '<div class="kb-user">' + (o.user.name ? '<b>' + esc(o.user.name) + '</b>' : '') + '<button type="button" class="kb-out">Sign out</button></div>';
    bar.innerHTML = h;
    var mh = (o.user && o.user.name ? '<div class="kb-who">Signed in as <b>' + esc(o.user.name) + '</b></div>' : '');
    items.forEach(function (it, i) { if (it.minor) mh += '<button type="button" data-i="' + i + '">' + svg(it.icon) + esc(it.label) + '</button>'; });
    if (o.user) mh += '<button type="button" class="kb-out">Sign out</button>';
    menu.innerHTML = mh; menu.hidden = true;
    function run(b) { var it = items[+b.getAttribute('data-i')]; menu.hidden = true; if (it && it.act) it.act(); }
    bar.onclick = function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.classList.contains('kb-title')) { if (o.onTitle) o.onTitle(); return; }
      if (b.classList.contains('kb-more')) { menu.hidden = !menu.hidden; b.setAttribute('aria-expanded', !menu.hidden); return; }
      if (b.classList.contains('kb-out')) { if (o.user && o.user.out) o.user.out(); return; }
      run(b);
    };
    menu.onclick = function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.classList.contains('kb-out')) { menu.hidden = true; if (o.user && o.user.out) o.user.out(); return; }
      run(b);
    };
    paintFull();
  }
  function paintFull() {
    if (!bar) return;
    var f = isFull();
    Array.prototype.forEach.call(d.querySelectorAll('#kbar [title="Full screen"],#kbar [title="Leave full screen"]'), function (b) {
      b.title = f ? 'Leave full screen' : 'Full screen'; b.innerHTML = svg(f ? 'unfull' : 'full') + '<span>' + b.title + '</span>'; });
  }
  d.addEventListener('fullscreenchange', paintFull); d.addEventListener('webkitfullscreenchange', paintFull);
  d.addEventListener('click', function (e) { if (menu && !menu.hidden && !e.target.closest('.kb-menu,.kb-more')) menu.hidden = true; });
  function hideBar() {
    if (bar) bar.remove(); if (menu) menu.remove();
    d.documentElement.classList.remove('kb-html'); d.body.classList.remove('kb-on');
  }

  /* ---------- one question at a time ----------
     o.root()    the element the app redraws pages into
     o.cards     selector for one question
     o.key()     the name of the page now showing (each page remembers its question)
     o.on()      false to show the whole page (for example a timed test)
     o.lead(r)   optional: something to read before question 1 (shown as its own step)
     o.status(c) 'ok', 'rev' or '' for the little numbered circles
     o.work      true: on big screens a working-out space sits beside the question */
  function stepper(o) {
    var mem = {}, root = o.root(), mo;
    function cardsIn(r) { return Array.prototype.filter.call(r.querySelectorAll(o.cards), function (c) { return !c.closest('.kq-skip'); }); }
    function clean(r) {
      Array.prototype.forEach.call(r.querySelectorAll('.kq-head,.kq-nav'), function (x) { x.remove(); });
      Array.prototype.forEach.call(r.querySelectorAll('.kq-hide,.kq-cur'), function (x) { x.classList.remove('kq-hide', 'kq-cur', 'kq-work'); });
    }
    function apply(scroll) {
      var r = o.root(); if (!r) return;
      if (mo) mo.disconnect();
      try {
        clean(r);
        if (o.on && !o.on()) return;
        var cards = cardsIn(r); if (cards.length < 2) return;
        var lead = o.lead ? o.lead(r) : null, steps = lead ? [lead].concat(cards) : cards;
        var k = o.key(), i = Math.max(0, Math.min(mem[k] || 0, steps.length - 1)), last = steps.length - 1;
        steps.forEach(function (c, j) { c.classList.toggle('kq-hide', j !== i); });
        var cur = steps[i]; cur.classList.add('kq-cur'); if (o.work && !(lead && i === 0)) cur.classList.add('kq-work');
        // what follows the last question (review box, page buttons) shows with the last question
        for (var n = steps[last].nextElementSibling; n; n = n.nextElementSibling) if (!n.classList.contains('kq-nav')) n.classList.toggle('kq-hide', i !== last);
        // a heading between two steps shows only with the step that follows it
        for (var m = steps[0].nextElementSibling; m && m !== steps[last]; m = m.nextElementSibling) {
          if (steps.indexOf(m) >= 0) continue;
          var nx = m.nextElementSibling; while (nx && steps.indexOf(nx) < 0) nx = nx.nextElementSibling;
          m.classList.toggle('kq-hide', nx !== cur);
        }
        var qi = lead ? i - 1 : i, done = 0;
        var head = d.createElement('div'); head.className = 'kq-head noprint';
        var dots = steps.map(function (c, j) {
          var st = (lead && j === 0) ? '' : (o.status ? o.status(c) : ''); if (st) done++;
          return '<button type="button" class="kq-dot ' + st + (j === i ? ' on' : '') + '" data-j="' + j + '" aria-label="' + (lead && j === 0 ? 'Read first' : 'Question ' + (lead ? j : j + 1)) + '">' + (lead && j === 0 ? 'i' : (lead ? j : j + 1)) + '</button>';
        }).join('');
        head.innerHTML = '<div class="kq-lab">' + (lead && i === 0 ? 'Read first <span>· then ' + cards.length + ' questions</span>' : 'Question ' + (qi + 1) + ' <span>of ' + cards.length + '</span>') + '</div>' +
          (steps.length <= 24 ? '<div class="kq-dots">' + dots + '</div>' : '') +
          '<div class="kq-bar"><i style="width:' + Math.round(100 * done / cards.length) + '%"></i></div>';
        steps[0].parentNode.insertBefore(head, steps[0]);
        var nav = d.createElement('div'); nav.className = 'kq-nav noprint';
        nav.innerHTML = (i > 0 ? '<button type="button" class="kq-prev">← Previous</button>' : '') +
          (i < last ? '<button type="button" class="kq-next">' + (lead && i === 0 ? 'Start the questions →' : 'Next question →') + '</button>' : '');
        if (nav.innerHTML) cur.parentNode.insertBefore(nav, cur.nextSibling);
        head.onclick = function (e) { var b = e.target.closest('[data-j]'); if (b) to(k, +b.getAttribute('data-j')); };
        nav.onclick = function (e) { if (e.target.closest('.kq-prev')) to(k, i - 1); else if (e.target.closest('.kq-next')) to(k, i + 1); };
        if (scroll) { var y = head.getBoundingClientRect().top + window.pageYOffset - 84; window.scrollTo(0, Math.max(0, y)); }
      } finally { if (mo) { mo.observe(r, { childList: true }); mo.takeRecords(); } }
    }
    function to(k, j) { mem[k] = j; apply(true); var f = d.querySelector('.kq-cur input:not([disabled]),.kq-cur .inp:not([disabled])'); if (f && window.matchMedia('(pointer:fine)').matches) try { f.focus({ preventScroll: true }); } catch (e) {} }
    mo = new MutationObserver(function () { apply(false); });
    if (root) mo.observe(root, { childList: true });
    apply(false);
    return { apply: apply };
  }

  /* ---------- exam pack ---------- */
  function pack() {
    d.body.classList.add('kx');
    var tt = d.querySelector('.top .tt'), title = tt && tt.firstChild ? String(tt.firstChild.textContent).trim() : 'Exam pack';
    var side = d.querySelector('nav.side');
    function toggleTopics() {
      if (window.matchMedia('(max-width:900px)').matches) d.body.classList.toggle('menu');
      else { var b = d.querySelector('.sidebtn'); if (b) b.click(); else d.body.classList.toggle('noside'); }
    }
    setBar({
      title: title.replace(/Mathematics/, 'maths'), sub: 'Exam pack',
      onTitle: function () { location.hash = '#home'; },
      items: [
        { label: 'Topics', icon: 'topics', act: toggleTopics },
        { label: 'Formula sheet', icon: 'formula', minor: true, act: function () { location.hash = '#formula'; } },
        { label: 'My progress', icon: 'progress', minor: true, act: function () { location.hash = '#progress'; } }
      ],
      user: { name: '', out: function () { try { localStorage.removeItem('ke-exam-code'); localStorage.removeItem('ke-pack'); } catch (e) {} location.reload(); } }
    });
    var view = d.getElementById('view');
    function partsOf(c) { return Array.prototype.slice.call(c.querySelectorAll('.part')); }
    var st = stepper({
      root: function () { return view; },
      cards: ':scope > section.card.q',
      key: function () { return location.hash || '#home'; },
      on: function () { return !/^#m\//.test(location.hash); },
      lead: function (r) { var l = /^#t\//.test(location.hash) ? r.querySelector(':scope > section.card:not(.q)') : null; return l && l.querySelector('li,.we,td') ? l : null; },
      status: function (c) {
        var p = partsOf(c), ok = c.querySelectorAll('.state.ok').length, any = c.querySelectorAll('.state').length;
        return p.length && ok === p.length ? 'ok' : any ? 'rev' : '';
      },
      work: true
    });
    // after Check, only the answer part is redrawn: bring the circles up to date
    view.addEventListener('click', function () { setTimeout(function () { st.apply(false); }, 0); });
    view.addEventListener('keydown', function (e) { if (e.key === 'Enter') setTimeout(function () { st.apply(false); }, 0); });
    // "Continue" on the home page
    function remember() { if (/^#t\/|^#x\//.test(location.hash)) try { localStorage.setItem('ke-exam-last-' + title, location.hash); } catch (e) {} }
    function cont() {
      if ((location.hash || '#home') !== '#home' || view.querySelector('.kx-cont')) return;
      var h = null; try { h = localStorage.getItem('ke-exam-last-' + title); } catch (e) {}
      var a = h && side && side.querySelector('a[href="' + h + '"]'); if (!a) return;
      var name = a.querySelector('.mini span') ? a.querySelector('.mini span').textContent : a.textContent, cnt = a.querySelector('.mini i');
      var box = d.createElement('div'); box.className = 'kx-cont';
      box.innerHTML = '<div><small>Continue</small><b>' + esc(name) + '</b><span>' + (cnt ? esc(cnt.textContent) + ' parts right' : '') + '</span></div><a href="' + esc(h) + '">Continue →</a>';
      view.insertBefore(box, view.firstChild);
    }
    addEventListener('hashchange', function () { remember(); setTimeout(cont, 0); });
    remember(); setTimeout(cont, 0);
  }

  window.KEApp = { bar: setBar, hideBar: hideBar, stepper: stepper, pack: pack, esc: esc };
})();
