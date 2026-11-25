/* Black Friday bundle banner: shows by itself from Fri 27 Nov to Mon 30 Nov 2026 (South African time),
   on the home page and the shop only. Add ?bf=1 to a page address to preview it. */
(function () {
  var now = Date.now(), from = Date.parse('2026-11-27T00:00:00+02:00'), to = Date.parse('2026-12-01T00:00:00+02:00');
  var preview = /[?&]bf=1/.test(location.search);
  if (!preview && (now < from || now >= to)) return;
  var p = location.pathname.replace(/index\.html$/, '');
  if (p !== '/' && p !== '/shop/') return;
  var msg = encodeURIComponent("Hi KnowledgeEmpowers, I'd like the Black Friday bundle (a year online + the printed My Maths Diary). My child's grade is: ");
  var css = '.bf{background:#2A1A18;color:#fff;font-family:"Public Sans",system-ui,sans-serif}' +
    '.bf .in{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:10px 28px;padding:16px clamp(20px,5vw,96px);text-align:center}' +
    '.bf .tag{font-size:.72rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#E3C48F}' +
    '.bf .txt{font-size:1rem;line-height:1.45}.bf .txt b{font-weight:700}.bf .txt s{opacity:.65}' +
    '.bf a{display:inline-flex;align-items:center;min-height:44px;padding:0 20px;border-radius:999px;background:#fff;color:#7A0000;font-weight:700;text-decoration:none;white-space:nowrap}' +
    '.bf a:hover{background:#F6E9E6}';
  css += '.launch{display:none!important}';   /* one strip at a time: the deal replaces the back-to-school line */
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var b = document.createElement('div'); b.className = 'bf'; b.setAttribute('role', 'region'); b.setAttribute('aria-label', 'Black Friday offer');
  b.innerHTML = '<div class="in"><span class="tag">Black Friday · until Monday 30 November</span>' +
    '<span class="txt"><b>A year of every topic online + the printed maths diary:</b> R299 <s>R348</s> for Grades 4–9, R349 <s>R398</s> for Grades 10–12. Online access until 31 December 2027.</span>' +
    '<a href="https://wa.me/27615818059?text=' + msg + '" target="_blank" rel="noopener">Order on WhatsApp</a></div>';
  var h = document.querySelector('header.top') || document.getElementById('kehdr');
  if (h && h.parentNode) h.parentNode.insertBefore(b, h.nextSibling); else document.body.insertBefore(b, document.body.firstChild);
})();
