# Tidies the shop: full-width maroon top, centred section heads, one even row of printed products, site footer.
import re
f = 'shop/index.html'; s = open(f).read()
CSS = r'''
:root{--bg:#FBF8F4;--card:#FFFFFF;--ink:#1E1414;--mut:#5E5150;--line:#E6DCD6;--soft:#F4EDE6;--m:#7A0000;--m-ink:#FFFFFF;--gold:#B08D57;--ok:#2E6B3F;
  --f-head:"Bitter",Georgia,serif;--f-body:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif}
*{box-sizing:border-box}
html{font-size:18px}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f-body);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--m)}
.in{max-width:1180px;margin:0 auto;padding:0 max(20px,env(safe-area-inset-left,0px))}
/* maroon top */
.band{background:var(--m);color:#fff;position:relative;overflow:hidden}
.band::after{content:"";position:absolute;right:-180px;top:-180px;width:560px;height:560px;border-radius:50%;border:1px solid rgba(233,211,166,.25)}
.band .in{padding-block:72px 80px;display:grid;gap:18px;position:relative;z-index:1}
.eyebrow{font-size:.72rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--gold)}
.band .eyebrow{color:#E9D3A6}
h1{font-family:var(--f-head);font-weight:600;font-size:clamp(2.3rem,5vw,3.8rem);line-height:1.1;margin:0;color:#fff;max-width:16ch;text-wrap:balance}
.rule{width:56px;height:1px;background:#E9D3A6;border:0;margin:6px 0}
.lead{margin:0;color:rgba(255,255,255,.88);max-width:52ch;font-size:1.1rem}
.promises{display:flex;flex-wrap:wrap;gap:10px 28px;margin:8px 0 0;padding:0;list-style:none;font-size:.9rem;color:rgba(255,255,255,.88)}
.promises li::before{content:"✓";color:#E9D3A6;font-weight:700;margin-right:8px}
/* sections */
.wrap{display:flex;flex-direction:column;gap:0}
.sec{padding-block:72px 0;display:flex;flex-direction:column;gap:28px}
.sec-head{display:grid;gap:10px;justify-items:center;text-align:center}
.sec-head p{margin:0;color:var(--mut);max-width:56ch}
h2{font-family:var(--f-head);font-weight:600;font-size:clamp(1.6rem,3vw,2.2rem);margin:0;line-height:1.15}
/* featured online card */
.feat{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);background:var(--card);border:1px solid var(--line);border-radius:4px;overflow:hidden;box-shadow:0 30px 60px -40px rgba(60,20,10,.35)}
.tile{background:var(--m);color:#fff;padding:36px;display:flex;flex-direction:column;justify-content:space-between;gap:24px;min-height:280px}
.tile .t{font-family:var(--f-head);font-weight:600;font-size:2rem;line-height:1.1}
.tile .shot{border:5px solid #fff;border-radius:3px;box-shadow:0 24px 40px -24px rgba(0,0,0,.6);width:100%}
.path{display:flex;align-items:center}
.path i{width:14px;height:14px;border-radius:50%;border:2px solid #fff;flex:none}
.path i.on{background:#fff}
.path b{flex:1;height:2px;background:#fff;opacity:.5}
.tile small{opacity:.85;font-size:.8rem}
.body{padding:32px 36px;display:flex;flex-direction:column;gap:14px;min-width:0}
.seg{display:inline-flex;align-self:flex-start;border:1px solid var(--line);border-radius:3px;padding:3px;gap:3px;flex-wrap:wrap;background:var(--card)}
.seg button{font:inherit;font-size:.84rem;border:0;background:transparent;color:var(--ink);padding:7px 12px;border-radius:2px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--m);color:#fff}
.price{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.price b{font-family:var(--f-head);font-weight:700;font-size:2.4rem;line-height:1;font-variant-numeric:tabular-nums}
.price span{color:var(--mut);font-size:.88rem}
ul.inc{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:6px;font-size:.93rem}
ul.inc li::before{content:"✓";color:var(--ok);font-weight:700;margin-right:8px}
.actions{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin-top:4px}
.buy{display:inline-flex;align-items:center;justify-content:center;background:var(--m);color:#fff;text-decoration:none;font-weight:600;letter-spacing:.03em;border-radius:2px;padding:13px 26px;font-size:.92rem;min-height:48px}
.buy:hover{background:#5C0000}
.ask{font-size:.88rem;color:var(--m);font-weight:600;text-decoration:none;border-bottom:1px solid var(--gold)}
.note{font-size:.8rem;color:var(--mut);margin:0}
/* product grids */
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;align-items:stretch}
.grid.two{grid-template-columns:repeat(2,minmax(0,1fr));max-width:860px;width:100%;margin:0 auto}
.card{background:var(--card);border:1px solid var(--line);border-radius:4px;overflow:hidden;display:flex;flex-direction:column}
.pic{background:var(--soft);display:flex;align-items:center;justify-content:center;padding:28px;height:300px}
.pic img{height:100%;width:auto;max-width:100%;object-fit:contain;box-shadow:0 14px 28px -12px rgba(60,20,10,.35);border-radius:2px}
.card .body{padding:24px 26px 28px;gap:12px;flex:1}
.card h3{font-family:var(--f-head);font-weight:600;font-size:1.25rem;margin:0}
.card p{margin:0;color:var(--mut);font-size:.92rem}
.card .price b{font-size:1.9rem!important}
.card .actions{margin-top:auto;padding-top:8px}
.card.best{border:1.5px solid var(--m)}
.draft{display:inline-block;font-family:var(--f-body);font-size:.68rem;font-weight:700;letter-spacing:.06em;color:var(--gold);border:1px solid var(--gold);border-radius:999px;padding:1px 8px;margin-left:6px;vertical-align:middle}
/* help strip */
.help{margin-top:80px;background:var(--soft);border-top:1px solid var(--line)}
.help .in{padding-block:48px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px}
.help div{display:flex;flex-direction:column;gap:6px;min-width:0}
.help b{font-family:var(--f-head);font-weight:600;font-size:1.05rem}
.help span{color:var(--mut);font-size:.9rem}
a:focus-visible,button:focus-visible{outline:2px solid var(--m);outline-offset:2px}
/* site footer */
.sfoot{background:#1E1414;color:#E9E1DC;padding-block:64px 36px;font-size:.88rem}
.sfoot .in{display:grid;gap:28px}
.sfoot .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:32px}
.sfoot h4{font:700 .72rem var(--f-body);letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin:0 0 12px}
.sfoot a{color:#E9E1DC;text-decoration:none;display:block;padding:3px 0}
.sfoot a:hover{color:#fff}
.sfoot img{height:38px}
.sfoot p{margin:0}
.sfoot small{opacity:.6;border-top:1px solid rgba(255,255,255,.12);padding-top:22px}
@media (min-width:1181px){html{font-size:19px}.band .in{padding-block:96px 104px}.sec{padding-block:96px 0}}
@media (max-width:1000px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:720px){html{font-size:17px}.feat{grid-template-columns:1fr}.tile{min-height:0;padding:28px}.body{padding:24px}.grid,.grid.two{grid-template-columns:1fr}.help .in{grid-template-columns:1fr;gap:20px}.sfoot .cols{grid-template-columns:1fr 1fr}.band .in{padding-block:52px 60px}.sec{padding-block:56px 0}.pic{height:260px}}
'''
# 1. styles
s = re.sub(r'<style>\n@media \(max-width:720px\)\{\.qp.*?</style>', '<style>' + CSS + '</style>', s, count=1, flags=re.S)
# 2. hero out of the narrow column into a full-width band
hero = re.search(r'\n  <section class="hero">(.*?)</section>\n', s, re.S)
inner = hero.group(1).replace('<h1>', '<h1>').replace('</h1>', '</h1><hr class="rule">')
s = s.replace(hero.group(0), '\n')
s = s.replace('<div class="wrap">\n  <header style="display:none">', '<section class="band"><div class="in">' + inner + '</div></section>\n<div class="wrap in">\n  <header style="display:none">', 1)
# 3. section heads
s = s.replace('<h2 id="h-online">Online workbooks</h2>', '<div class="sec-head"><div class="eyebrow">Online</div><h2 id="h-online">Every topic, for a full year</h2></div>')
s = s.replace('<h2 id="h-print">Printed and to keep</h2>', '<div class="sec-head"><div class="eyebrow">Printed</div><h2 id="h-print">Books to keep and write in</h2></div>')
s = s.replace('<h2 id="h-packs">Build a maths shelf</h2>\n    <p>Printed books last from the first concept to the last, so you buy each one once.</p>\n    <div class="seg" role="group" aria-label="Choose a series" style="align-self:flex-start">',
              '<div class="sec-head"><div class="eyebrow">Save on sets</div><h2 id="h-packs">Build a maths shelf</h2><p>Printed books last from the first concept to the last, so you buy each one once.</p></div>\n    <div class="seg" role="group" aria-label="Choose a series" style="align-self:center">')
# 4. online tile: real screenshot instead of empty space
s = s.replace('<div><div class="t">All maths topics.<br>One price.</div></div>',
              '<div class="t">All maths topics.<br>One price.</div><img class="shot" src="/assets/preview/practice-hint.jpg" alt="A workbook question with a hint after a wrong try">')
s = s.replace('href="https://www.knowledgeempowers.online" target="_blank" rel="noopener">Try the free maths check first', 'href="/baseline-assessment/">Try the free maths check first')
# 5. printed workbook: real cover instead of the drawn one
s = re.sub(r'<div class="pic"><div class="mini">.*?</div></div></div>', '<div class="pic"><img src="/assets/preview/book-cover.jpg" alt="Fractions workbook cover"></div>', s, count=1, flags=re.S)
# 6. Quiet Progress: same card shape as the others
qp = re.search(r'<article class="card" style="grid-column:1/-1">\s*<div style="display:grid;grid-template-columns:minmax\(0,\.8fr\) minmax\(0,1\.2fr\)" class="qp">\s*<div class="pic" style="height:auto;min-height:260px">(<img [^>]*?) style="height:250px">(</div>.*?</div>)\s*</div>\s*</article>', s, re.S)
s = s.replace(qp.group(0), '<article class="card">\n          <div class="pic">' + qp.group(1) + '>' + qp.group(2) + '\n      </article>')
# 7. shelf cards
s = s.replace('<div class="grid">\n      <article class="card" style="border:1.5px solid var(--m)">', '<div class="grid two">\n      <article class="card best">')
# 8. help strip full width, then the site footer
help_ = re.search(r'\n  <section class="help" aria-label="Help">(.*?)</section>\n', s, re.S)
s = s.replace(help_.group(0), '\n')
FOOT = '''<footer class="sfoot"><div class="in">
  <div class="cols">
    <div style="display:grid;gap:14px;align-content:start"><img src="/assets/img/logo-white.svg" alt="KnowledgeEmpowers"><p>One topic, in depth. Works alongside any curriculum.</p><p style="opacity:.75">Don't give up! Grow through what you go through.</p></div>
    <div><h4>Learn</h4><a href="/baseline-assessment/">Free maths check</a><a href="/free-classroom-practice/">Free practice</a><a href="/workbooks/">Workbooks</a><a href="/exam-packs/">Exam packs</a><a href="/digital-empowerment/">Free maths tools</a></div>
    <div><h4>More</h4><a href="/shop/">Shop</a><a href="/tutoring/">Tutoring</a><a href="/grow-at-home/">Grow at home</a><a href="/mathematics/">Mathematics</a><a href="/about/">About</a></div>
    <div><h4>Contact</h4><a href="https://wa.me/27615818059">WhatsApp 061 581 8059</a><a href="mailto:knowledgeempowers08@gmail.com">Email us</a><a href="/about/contact/">Contact</a><a href="/about/privacy-policy/">Privacy</a><a href="/about/terms-and-conditions/">Terms</a></div>
  </div>
  <small>© KnowledgeEmpowers. Licensed to the subscriber for use with their own learners. Not for resale.</small>
</div></footer>'''
s = re.sub(r'\n  <footer>.*?</footer>\n</div>\n', '\n</div>\n<section class="help" aria-label="Help"><div class="in">' + help_.group(1) + '</div></section>\n' + FOOT + '\n', s, count=1, flags=re.S)
open(f, 'w').write(s)
print('ok')
