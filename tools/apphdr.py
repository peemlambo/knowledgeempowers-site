# Puts the same site header (logo, Home and the full menu) on the app pages that are not built by build.py.
import re, sys
sys.path.insert(0, 'tools')
NAV = [('/', 'Home'), ('/baseline-assessment/', 'Free maths check'), ('/free-classroom-practice/', 'Free practice'), ('/workbooks/', 'Workbooks'),
       ('/exam-packs/', 'Exam packs'), ('/shop/', 'Shop'), ('/tutoring/', 'Tutoring'), ('/about/', 'About')]
CSS = '''<style id="kehdr-css">
html{padding-top:72px!important}
#kehdr{position:fixed;top:0;left:0;right:0;z-index:9999;height:72px;background:rgba(251,248,244,.97);backdrop-filter:blur(6px);border-bottom:1px solid #E6DCD6;font-family:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
#kehdr *{box-sizing:border-box}
#kehdr .kh-w{max-width:1240px;height:100%;margin:0 auto;padding:0 max(20px,env(safe-area-inset-left,0px));display:flex;align-items:center;justify-content:space-between;gap:24px;position:relative}
#kehdr .kh-logo img{height:40px;width:auto;display:block}
#kehdr nav{display:flex;align-items:center;gap:26px;font-size:13.5px;font-weight:600;letter-spacing:.12em;text-transform:uppercase}
#kehdr nav a{color:#1E1414;text-decoration:none;padding:6px 0;border-bottom:1px solid transparent;white-space:nowrap;line-height:1.4}
#kehdr nav a:hover,#kehdr nav a[aria-current]{color:#7A0000;border-color:#7A0000}
#kehdr nav .kh-login{background:#7A0000;color:#fff;padding:10px 18px;border:0}
#kehdr nav .kh-login:hover{background:#5C0000;color:#fff}
#kehdr .kh-menu{width:auto;min-height:0;margin:0;display:none;align-items:center;gap:10px;background:#7A0000;color:#fff;border:0;border-radius:2px;padding:11px 16px;font:600 13px "Public Sans",sans-serif;letter-spacing:.14em;text-transform:uppercase;cursor:pointer}
#kehdr .kh-menu::before{content:"";width:16px;height:10px;border-top:2px solid #fff;border-bottom:2px solid #fff;background:linear-gradient(#fff,#fff) center/100% 2px no-repeat}
@media (max-width:1180px){
 html{padding-top:64px!important}
 #kehdr{height:64px}
 #kehdr .kh-logo img{height:34px}
 #kehdr .kh-menu{display:inline-flex}
 #kehdr nav{display:none;position:absolute;left:0;right:0;top:100%;background:#FBF8F4;border-bottom:1px solid #E6DCD6;flex-direction:column;align-items:stretch;gap:0;padding:6px max(20px,env(safe-area-inset-left,0px)) 18px;box-shadow:0 20px 30px -20px rgba(0,0,0,.2);font-size:15px}
 #kehdr nav.open{display:flex}
 #kehdr nav a{padding:14px 0;border-bottom:1px solid #E6DCD6}
 #kehdr nav .kh-login{margin-top:14px;text-align:center}
}
@media print{#kehdr{display:none}html{padding-top:0!important}}
%EXTRA%
</style>'''
def header(cur):
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == cur else '', t) for h, t in NAV)
    return ('<div id="kehdr"><div class="kh-w"><a class="kh-logo" href="/" aria-label="KnowledgeEmpowers home"><img src="/assets/img/logo.png" alt="KnowledgeEmpowers"></a>'
            '<button class="kh-menu" type="button" aria-expanded="false">Menu</button>'
            '<nav aria-label="Main">%s<a class="kh-login" href="/workbooks/digital-math-workbooks/">Log in</a></nav></div></div>'
            '<script>(function(){var b=document.querySelector("#kehdr .kh-menu"),n=document.querySelector("#kehdr nav");b.addEventListener("click",function(){var o=n.classList.toggle("open");b.setAttribute("aria-expanded",o)})})();</script>') % nav

PAGES = {
 'baseline-assessment/index.html': ('/baseline-assessment/', 'div.top{display:none!important}body>.wrap,#app{padding-top:40px}h1{font-size:clamp(1.8rem,3.2vw,2.5rem)!important;line-height:1.2!important}@media (min-width:1181px){body:not(.rep) .wrap{max-width:820px!important}}'),
 'free-classroom-practice/index.html': ('/free-classroom-practice/', 'h1{font-size:clamp(1.8rem,3.2vw,2.5rem)!important;line-height:1.2!important}'),
 'shop/index.html': ('/shop/', ''),
 'workbooks/digital-math-workbooks/index.html': ('', ''),
 'exam-packs/exam-preparation-packs/index.html': ('', 'body{min-height:calc(100vh - 72px)!important}@media (max-width:1180px){body{min-height:calc(100vh - 64px)!important}}'),
 'digital-empowerment/visual-times-table-explorer/index.html': ('', ''),
 'digital-empowerment/interactive-ratio-and-proportion/index.html': ('', ''),
 'digital-empowerment/interactive-fraction-decimal-and-percentage-builder/index.html': ('', ''),
}
for f, (cur, extra) in PAGES.items():
    s = open(f).read()
    s = re.sub(r'<div id="kehome".*?</span></div>', '', s, count=1, flags=re.S)       # old slim bar
    s = re.sub(r'<style id="kehdr-css">.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<div id="kehdr">.*?</script>', '', s, count=1, flags=re.S)
    css = CSS.replace("%EXTRA%", extra)
    hd = header(cur) if '</head>' in s else css + header(cur)
    s = s.replace('</head>', css + '</head>', 1)
    m = re.search(r'<body[^>]*>', s, flags=re.I)
    if m: s = s[:m.end()] + hd + s[m.end():]
    else: s = s.replace('<div id="app">', hd + '<div id="app">', 1)
    if f.startswith('shop'):
        s = s.replace('<header>\n    <a class="b"', '<header style="display:none">\n    <a class="b"', 1)
    if f.startswith('free-classroom'):
        s = s.replace("function header(){\n  if(EMBED)return '';", "function header(){\n  return '';", 1)
    open(f, 'w').write(s)
    print(f, s.count('id="kehdr"'), s.count('kehome'), '</head>' in s)
