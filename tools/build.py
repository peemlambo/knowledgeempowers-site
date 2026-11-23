# Builds the simple content pages of the KnowledgeEmpowers website from one shared header and footer.
# Run: python3 tools/build.py   (from the repository folder)
import os, re, html
from urllib.parse import quote

GA = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-YHMHQ9V039"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-YHMHQ9V039');</script>'''
WA = 'https://wa.me/27615818059'
def wa(text): return WA + '?text=' + quote(text)
LOGIN = '/workbooks/digital-math-workbooks/'
NAV = [('/', 'Home'), ('/baseline-assessment/', 'Free maths check'), ('/free-classroom-practice/', 'Free practice'), ('/workbooks/', 'Workbooks'),
       ('/exam-packs/', 'Exam packs'), ('/shop/', 'Shop'), ('/tutoring/', 'Tutoring'), ('/about/', 'About')]


import re as _re
# A picture for the top of each inner page that has none of its own
PICS = {
 '/tutoring/mathematics-tutoring-grades-5-10/': '<figure><div class="win"><img src="/assets/preview/practice-check.jpg" alt="A worked answer, step by step"></div></figure>',
 '/digital-empowerment/': '<figure><div class="win"><img src="/assets/preview/tools.jpg" alt="The free Times Table Explorer"></div></figure>',
 '/motivation-faith/': '<figure class="pic"><img src="/assets/img/seedling.jpg" alt="A young plant growing from the soil"></figure>',
 '/mathematics/': '<figure class="pic"><img src="/assets/img/shelf.jpg" alt="Workbooks for Whole numbers, Integers, Fractions and Algebraic expressions"></figure>',
 '/about/': '<figure class="pic"><img src="/assets/img/workbook.jpg" alt="An open Fractions workbook"></figure>',
}
def _div_end(s, start):
    depth, i = 0, start
    for m in _re.finditer(r'<(/?)div\b', s[start:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start + m.start() + s[start + m.start():].find('>') + 1
    return len(s)
def _accent(html):
    # "First part, second part" -> "First part, <em>second part</em>" (the gold italic accent used on the home page)
    def f(m):
        t = m.group(1)
        if '<' in t or ',' not in t: return m.group(0)
        i = t.rfind(', ')
        return '<h1>%s, <em>%s</em></h1>' % (t[:i], t[i+2:]) if i > 0 else m.group(0)
    return _re.sub(r'<h1>(.*?)</h1>', f, html, count=1, flags=_re.S)
def brand_head(path, body):
    return _accent(_brand_head(path, body)) if path != '/' else body
def _brand_head(path, body):
    if path == '/' or 'class="phead"' in body: return body
    b = body.lstrip()
    if b.startswith('<div class="wrap hero">'):
        e = _div_end(b, 0)
        return '<section class="phead">' + b[:e] + '</section>' + b[e:]
    m = _re.match(r'<div class="wrap page([^"]*)">\s*<div class="eb">(.*?)</div>\s*<h1>(.*?)</h1>\s*(<p class="lead">.*?</p>)?', b, _re.S)
    if m:
        pic = PICS.get(path, '')
        head = '<section class="phead"><div class="wrap hero%s"><div class="txt"><div class="eb">%s</div><h1>%s</h1><hr class="rule">%s</div>%s</div></section>' % (
            '' if pic else ' solo', m.group(2), m.group(3), m.group(4) or '', pic)
        return head + '<div class="wrap page after%s">' % m.group(1) + b[m.end():]
    return body

SITE_URL = 'https://www.knowledgeempowers.online'
import json as _json
def ld_json(path):
    org = {"@type": "EducationalOrganization", "@id": SITE_URL + "/#org", "name": "KnowledgeEmpowers",
           "alternateName": "GROW", "legalName": "Pelocus Org (Pty) Ltd", "url": SITE_URL + "/",
           "logo": SITE_URL + "/assets/img/logo.png", "image": SITE_URL + "/assets/img/share.jpg",
           "description": "Maths workbooks, exam packs, free practice and tutoring for Grades 4 to 12. One topic, in depth. Works alongside any curriculum.",
           "email": "knowledgeempowers08@gmail.com", "telephone": "+27615818059",
           "address": {"@type": "PostalAddress", "streetAddress": "25 Frederick Rd, Broadacres", "addressLocality": "Johannesburg", "postalCode": "2191", "addressCountry": "ZA"},
           "areaServed": "ZA"}
    graph = [org]
    if path == '/':
        graph.append({"@type": "WebSite", "@id": SITE_URL + "/#site", "url": SITE_URL + "/", "name": "KnowledgeEmpowers", "publisher": {"@id": SITE_URL + "/#org"}, "inLanguage": "en-ZA"})
    return _json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace('</', '<\\/')

def page(path, title, desc, body, current=None):
    body = brand_head(path, body)
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if current == h else '', t) for h, t in NAV)
    out = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s · KnowledgeEmpowers</title>
<meta name="description" content="%(desc)s">
<meta property="og:title" content="%(title)s · KnowledgeEmpowers">
<meta property="og:description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="KnowledgeEmpowers">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="https://www.knowledgeempowers.online/assets/img/share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/logo.png">
<script type="application/ld+json">%(ld)s</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:ital,wght@0,500;0,600;0,700;1,500&family=Public+Sans:wght@400;600;700&display=swap">
<link rel="stylesheet" href="/assets/classic.css">
%(ga)s
</head>
<body%(bc)s>
<div class="launch">2027 back to school: start with the free maths check.<a href="/baseline-assessment/">Find the gaps</a></div>
<header class="top"><div class="wrap">
  <a href="/" aria-label="KnowledgeEmpowers home"><img src="/assets/img/logo.svg" alt="KnowledgeEmpowers"></a>
  <button class="menu" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav">%(nav)s<a class="login" href="%(login)s">Log in</a></nav>
</div></header>
<main>
%(body)s
</main>
<footer><div class="wrap">
  <div class="cols">
    <div style="display:grid;gap:14px;align-content:start"><img src="/assets/img/logo-white.svg" alt="KnowledgeEmpowers"><p>One topic, in depth. Works alongside any curriculum.</p><p style="opacity:.75">Don't give up! Grow through what you go through.</p></div>
    <div><h4>Learn</h4><a href="/baseline-assessment/">Free maths check</a><a href="/free-classroom-practice/">Free practice</a><a href="/workbooks/">Workbooks</a><a href="/exam-packs/">Exam packs</a><a href="/digital-empowerment/">Free maths tools</a></div>
    <div><h4>More</h4><a href="/shop/">Shop</a><a href="/tutoring/">Tutoring</a><a href="/grow-at-home/">Grow at home</a><a href="/mathematics/">Mathematics</a><a href="/about/">About</a></div>
    <div><h4>Contact</h4><a href="%(wa)s">WhatsApp 061 581 8059</a><a href="mailto:knowledgeempowers08@gmail.com">Email us</a><a href="/about/contact/">Contact</a><a href="/about/privacy-policy/">Privacy</a><a href="/about/terms-and-conditions/">Terms</a></div>
  </div>
  <small>© KnowledgeEmpowers. Licensed to the subscriber for use with their own learners. Not for resale.</small>
</div></footer>
<script>document.querySelector('.menu').addEventListener('click',function(){var n=document.getElementById('nav'),o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)});</script>
<a class="wa-float" href="https://wa.me/27615818059" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/></svg><span>WhatsApp us</span></a>
</body>
</html>
''' % dict(title=html.escape(title), desc=html.escape(desc), ga=GA, nav=nav, login=LOGIN, body=body, wa=WA, url=SITE_URL + path, ld=ld_json(path), bc=' class="home"' if path == '/' else '')
    d = path.strip('/')
    if d: os.makedirs(d, exist_ok=True)
    open((d + '/' if d else '') + 'index.html', 'w').write(out)

def prices(rows): return '<div class="prices">' + ''.join('<div><span>%s</span><b>%s</b></div>' % r for r in rows) + '</div>'
def ul(items): return '<ul>' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'
def btns(*b): return '<div class="btns">' + ''.join('<a class="btn%s" href="%s">%s</a>' % (' ghost' if i else '', h, t) for i, (h, t) in enumerate(b)) + '</div>'
MORE = '<p><a href="/grow-at-home/">More to grow at home →</a></p>'

# ---------------- Home
HOME = '''<div class="wrap hero">
  <div class="eb">Maths for Grades 4 to 12</div>
  <h1>One topic, in depth.</h1>
  <p class="lead">Workbooks, exam packs and free practice for learners in South African public, IEB and Cambridge schools. Every answer shown step by step. Works alongside any curriculum.</p>
  %s
</div>
<section class="soft"><div class="wrap">
  <h2>How it works</h2>
  <div class="steps">
    <div><h3>Take the free maths check</h3><p class="mut">See which topics are secure and which need work.</p></div>
    <div><h3>Choose what fits</h3><p class="mut">A workbook or exam pack for the gaps the check found.</p></div>
    <div><h3>Start the same day</h3><p class="mut">Get your access code on WhatsApp, or a printed book delivered.</p></div>
  </div>
</div></section>
<section><div class="wrap">
  <h2>How we can help</h2>
  <div class="tiles">
    <a class="tile" href="/free-classroom-practice/"><h3>Free classroom and practice</h3><p class="mut">Show a lesson on the classroom screen, or practise at home. No sign-up.</p><span class="go">Start practising →</span></a>
    <a class="tile" href="/workbooks/"><h3>Online workbooks</h3><p class="mut">Every topic for a year: R149 for Grades 4–9, R199 for Grades 10–12.</p><span class="go">See workbooks →</span></a>
    <a class="tile" href="/shop/"><h3>Printed books and diaries</h3><p class="mut">Topic workbooks in full colour, and a maths diary for every age.</p><span class="go">See the shop →</span></a>
    <a class="tile" href="/exam-packs/"><h3>Exam packs</h3><p class="mut">End-of-year exam preparation for your child's grade, in print and online.</p><span class="go">See exam packs →</span></a>
    <a class="tile" href="/tutoring/"><h3>Tutoring</h3><p class="mut">One-to-one online maths and English lessons, Grades 4 to 10.</p><span class="go">Find out more →</span></a>
    <a class="tile" href="/grow-at-home/"><h3>Grow at home</h3><p class="mut">Quiet Progress books, free maths tools and motivation.</p><span class="go">Explore →</span></a>
  </div>
</div></section>''' % btns(('/baseline-assessment/', "Find my child's gaps (free)"), ('/shop/', 'Shop'))
page('/', 'Maths for Grades 4 to 12', 'Maths workbooks, exam packs and free practice for Grades 4 to 12. One topic, in depth. Works alongside any curriculum.', HOME)

# ---------------- Workbooks
page('/workbooks/', 'Workbooks', 'One maths topic at a time, Grades 4 to 12, online and printed.', '''<div class="wrap page wide">
<div class="split"><div style="display:grid;gap:22px">
  <div class="eb">Workbooks</div><h1>One topic at a time, Grades 4 to 12</h1>
  <p class="lead">Each workbook takes one maths topic in depth, and works alongside any curriculum. Online, a wrong answer brings a hint first, then the full steps, so learners can work alone.</p>
</div><img src="/assets/img/workbook.jpg" alt="A KnowledgeEmpowers topic workbook"></div>
<h2>All topics online</h2>%s
<h2>Printed workbook</h2>%s
<p class="mut">Delivery of printed workbooks is charged separately.</p>
<div class="note"><b>How to order:</b> message us on WhatsApp with your child's grade. Pay using the details we send you, then receive your personal code. Each code is for one learner, lasts 12 months from the day you pay, and works on up to 2 devices.</div>
%s
</div>''' % (prices([('Grades 4–9', 'R149 a year'), ('Grades 10–12', 'R199 a year')]),
             prices([('One topic', 'R199 (members R169)'), ('Part 1 or Part 2', 'R109 (members R99)')]),
             btns((wa("Hi, I'd like to order a workbook. Topic and grade: "), 'Order on WhatsApp'), (LOGIN, 'I already have a code'), ('/baseline-assessment/', 'Not sure? Take the free maths check'))), '/workbooks/')

# ---------------- Exam packs
page('/exam-packs/', 'Exam packs', 'End-of-year maths exam preparation, Grades 4 to 12.', '''<div class="wrap page wide">
<div class="split"><div style="display:grid;gap:22px">
  <div class="eb">Exam packs</div><h1>End-of-year maths exam preparation, Grades 4 to 12</h1>
  <p class="lead">One pack for your child's grade, for South African (public and IEB) and Cambridge learners.</p>
  <p>Inside: revision for every topic with worked examples, mock exam papers with full memos, a formula sheet and a progress tracker.</p>
</div><img src="/assets/img/parts.jpg" alt="KnowledgeEmpowers printed books"></div>
<h2>Grades 4 to 9</h2>%s
<h2>Grades 10 to 12</h2>%s
<p class="mut">Delivery of printed packs is charged separately.</p>
<div class="note"><b>How to order:</b> message us on WhatsApp with your child's grade and the pack you want. Pay using the details we send you. Then receive your pack and personal code. Each code is for one learner and works for one school term on up to 2 devices.</div>
%s
</div>''' % (prices([('Online', 'R149'), ('PDF', 'R100'), ('Printed', 'R199')]), prices([('Online', 'R199'), ('PDF', 'R149'), ('Printed', 'R250')]),
             btns((wa("Hi, I'd like to order an Exam Pack. Grade: "), 'Order on WhatsApp'), ('/exam-packs/exam-preparation-packs/', 'I already have a code'))), '/exam-packs/')

# ---------------- Tutoring
page('/tutoring/', 'Tutoring', 'One-to-one online maths and English lessons for Grades 4 to 10.', '''<div class="wrap page wide">
<div class="eb">Tutoring</div><h1>One-to-one online lessons, Grades 4 to 10</h1>
<p class="lead">We start where your child is, and stay with a topic until it makes sense. Each lesson is tailored to the learner's needs, schoolwork and goals, with clear explanations and guided practice.</p>
%s
<p>Message us on WhatsApp to discuss your child's grade, learning goals and available lesson times.</p>
%s
<div class="cards">
 <div class="card"><h3>Mathematics tutoring</h3><p class="mut">Clear explanations, step-by-step guidance and personal support.</p>%s<a href="/tutoring/mathematics-tutoring-grades-5-10/">Learn more →</a></div>
 <div class="card"><h3>English HL/FAL tutoring</h3><p class="mut">Reading, writing, grammar, comprehension and exam performance.</p>%s<a href="/tutoring/english-hl-or-fal-tutoring-grades-4-10/">Learn more →</a></div>
</div></div>''' % (prices([('Single 60-minute lesson', 'R250'), ('4 online lessons', 'R900')]), btns(('https://wa.me/message/XAFTSZAMNG6IO1', 'Enquire about online lessons')),
                   ul(['One-on-one online lessons', 'Group classes available', 'Exam preparation and revision', 'Homework support', 'Problem-solving and confidence']),
                   ul(['Group classes', 'Essay and creative writing support', 'Comprehension strategies', 'Speaking and listening skills'])), '/tutoring/')
page('/tutoring/mathematics-tutoring-grades-5-10/', 'Mathematics tutoring', 'Online mathematics tutoring, Grades 4 to 10.', '''<div class="wrap page">
<div class="eb">Tutoring</div><h1>Mathematics tutoring</h1>
<p class="lead">Online mathematics tutoring designed to help learners strengthen understanding, improve problem-solving skills, and build academic confidence. Lessons are personalised to each learner's pace, learning style and needs. The focus is on understanding concepts clearly rather than relying only on memorisation.</p>
<h2>Common challenges learners face</h2>%s
<h2>Topics covered</h2>%s
<h2>Teaching approach</h2><p>Lessons are conducted in a calm and supportive environment where learners are encouraged to ask questions, think independently, and strengthen foundational understanding step by step. The goal is to help learners improve confidence, clarity and academic growth over time.</p>
<h2>Online lesson information</h2>%s
%s</div>''' % (ul(['Difficulty understanding mathematical concepts', 'Fear of making mistakes', 'Weak foundational knowledge', 'Struggles with algebra and problem-solving', 'Exam anxiety and lack of confidence', 'Difficulty applying formulas correctly']),
               ul(['Number operations', 'Fractions and decimals', 'Percentages', 'Algebra', 'Geometry', 'Trigonometry', 'Statistics and probability', 'Functions and graphs', 'Measurement and finance', 'Data handling and patterns']),
               ul(['One-on-one online tutoring', 'Lessons via Google Meet', 'Flexible scheduling', 'Homework and revision support', 'Exam preparation assistance']),
               btns(('https://wa.me/message/XAFTSZAMNG6IO1', 'Enquire on WhatsApp'))), '/tutoring/')
page('/tutoring/english-hl-or-fal-tutoring-grades-4-10/', 'English HL/FAL tutoring', 'Online English tutoring, Grades 4 to 10.', '''<div class="wrap page">
<div class="eb">Tutoring</div><h1>English HL/FAL tutoring</h1>
<p class="lead">English language tutoring focused on improving communication, comprehension, writing, grammar and confidence in using English effectively. Lessons support learners at different levels by strengthening both foundational language skills and academic performance.</p>
<h2>Areas of support</h2>%s
<h2>Common challenges learners face</h2>%s
<h2>Online lesson information</h2>%s
%s</div>''' % (ul(['Grammar and sentence structure', 'Reading comprehension', 'Vocabulary development', 'Essay and paragraph writing', 'Pronunciation and speaking confidence', 'English for academic purposes']),
               ul(['Difficulty expressing ideas clearly', 'Limited vocabulary', 'Lack of confidence when speaking English', 'Grammar mistakes in writing', 'Difficulty understanding comprehension passages', 'Fear of participating in class discussions']),
               ul(['Online lessons via Google Meet', 'One-on-one support', 'Flexible lesson scheduling', 'Homework and assignment assistance', 'Academic writing support']),
               btns(('https://wa.me/message/XAFTSZAMNG6IO1', 'Enquire on WhatsApp'))), '/tutoring/')

# ---------------- Grow at home
page('/grow-at-home/', 'Grow at home', 'Books for learners and parents, free maths tools and guides on faith.', '''<div class="wrap page wide">
<div class="eb">Beyond the classroom</div><h1>Calm habits, strong minds, real skills.</h1>
<p class="lead">Books for learners and parents, plus free maths tools and guides on faith. Small steps at home that help your child grow.</p>
<div class="tiles" style="margin-top:0">
 <a class="tile" href="/free-classroom-practice/"><h3>Free practice</h3><p class="mut">Practise any topic, with every answer shown step by step.</p><span class="go">Start →</span></a>
 <a class="tile" href="/digital-empowerment/"><h3>Free maths tools</h3><p class="mut">Interactive tools that help your child see the maths.</p><span class="go">Open →</span></a>
 <a class="tile" href="/motivation-faith/"><h3>Motivation &amp; Faith</h3><p class="mut">Prepare yourself, because life won't wait.</p><span class="go">Read →</span></a>
 <a class="tile" href="/the-power-of-quiet-progress/"><h3>The Power of Quiet Progress</h3><p class="mut">Learner Edition · from R149</p><span class="go">See the book →</span></a>
 <a class="tile" href="/the-quiet-progress-method/"><h3>The Quiet Progress Method</h3><p class="mut">Family Edition · from R199</p><span class="go">See the book →</span></a>
 <a class="tile" href="/shop/"><h3>My Maths Diary</h3><p class="mut">A full-year diary for Grades 4–7, 8–9 and 10–12.</p><span class="go">See the shop →</span></a>
</div>
<p class="mut">Empowering minds. Uplifting hearts. Transforming lives.</p>
</div>''')

# ---------------- Free maths tools
page('/digital-empowerment/', 'Free maths tools', 'Three free tools that help your child see the maths, not just memorise it.', '''<div class="wrap page">
<div class="eb">Free maths tools</div><h1>See the maths, not just memorise it</h1>
<p class="lead">Three free tools for Grades 4 to 9.</p>
<div class="cards">
 <div class="card"><h3>Fraction, Decimal and Percentage Builder</h3><p class="mut">Shade a shape and watch the fraction, decimal and percentage change together. Grades 4 to 7.</p><a href="interactive-fraction-decimal-and-percentage-builder/">Open tool →</a></div>
 <div class="card"><h3>Ratio Mixer</h3><p class="mut">Mix parts and see how ratio and proportion scale up and down. Grades 6 to 9.</p><a href="interactive-ratio-and-proportion/">Open tool →</a></div>
 <div class="card"><h3>Times Table Explorer</h3><p class="mut">See each times table as rows and columns, then test yourself with short quizzes. Grades 4 to 6.</p><a href="visual-times-table-explorer/">Open tool →</a></div>
 <div class="card"><h3>Want the whole topic?</h3><p class="mut">Every topic, step by step, in the online workbooks.</p><a href="/workbooks/">See workbooks →</a></div>
</div>%s</div>''' % MORE)

# ---------------- Motivation & Faith
MF = [("Know yourself before you chase success", "Before you chase degrees, jobs or relationships, ask: who am I becoming? Your values, your faith and your emotional clarity are your compass. Build your identity on truth, not trends.", "Journal your strengths, fears and goals. Speak affirmations daily. Your voice matters."),
      ("Master the basics. They're your foundation.", "Learn how to budget, cook, clean and manage your time. These aren't chores or checkboxes. They're tools for freedom, confidence and long-term success. Education is your launchpad, not just a requirement. Small steps build strong habits.", "Create a weekly routine. Learn one new life skill each month. Stay curious: read, ask questions, and seek tutoring when needed."),
      ("Build emotional resilience", "You'll face rejection, confusion and pressure. That's normal. What matters is how you respond. Practise self-awareness. Learn to pause before reacting. Forgive yourself quickly.", "When overwhelmed, breathe, pray and reflect. Growth often hides in discomfort."),
      ("Invest in relationships that build you", "Choose friends who challenge you to grow, not just chill. Seek mentors. Be teachable. Your circle shapes your mindset, so choose wisely.", "Ask: “Does this relationship help me rise?” If not, reset your boundaries."),
      ("Pursue purpose, not just paychecks", "Your career matters, but your calling matters more. Align your work with your gifts. It's okay to pivot. It's okay to start small. Just don't settle for a life that doesn't speak to your soul.", "Volunteer, shadow professionals, or start a side project. Explore before you commit."),
      ("Stay rooted in faith and focus", "Life will test your focus. Distractions will come. Stay anchored in what's eternal. Faith isn't weakness, it's your fuel. Focus isn't pressure, it's your power.", "Declaration: “I am growing through what I go through. I am equipped, empowered, and evolving.”")]
page('/motivation-faith/', 'Motivation & Faith', "Prepare yourself, because life won't wait.", '''<div class="wrap page">
<div class="eb">Motivation &amp; Faith</div><h1>Prepare yourself, because life won't wait</h1>
<p class="lead">Don't give up, grow through what you go through. Life doesn't come with a manual, but it does come with moments. Moments that shape you, stretch you, and call you to rise. If you're a young adult standing at the edge of independence, here's how you could prepare yourself, not just to survive but to thrive.</p>
%s
<h2>You're not behind, you're becoming</h2><p>You don't need to have it all figured out. You just need to start. Prepare yourself with intention, and life will meet you with opportunity. You are not alone. You are not late. You are not lost. You are learning. You are rising. You are ready.</p>
%s</div>''' % (''.join('<h2>%s</h2><p>%s</p><p class="note"><b>Tip:</b> %s</p>' % (h, p, t) if not t.startswith('Declaration') else '<h2>%s</h2><p>%s</p><p class="note">%s</p>' % (h, p, t) for h, p, t in MF), MORE))

# ---------------- Quiet Progress books
def book(path, title, eb, h, lead, img, ed, edtxt, pdf, printed, printword, who_intro, who, inside, extra, other, othertxt):
    page(path, title, lead, '''<section class="phead"><div class="wrap hero"><div class="txt">
  <div class="eb">%s</div><h1>%s</h1><hr class="rule"><p class="lead">%s</p>
  <h2 style="color:#fff;font-size:1.5rem">%s</h2><p class="lead" style="font-size:1rem">%s</p>
  <p><b>PDF download: R%d · %s: R%d plus delivery</b></p>
  %s
</div><figure class="pic cover"><img src="/assets/img/%s" alt="%s cover"></figure></div></section>
<div class="wrap page wide after">
<div class="cards">
 <div class="card"><h3>Who it is for</h3><p class="mut">%s</p>%s</div>
 <div class="card"><h3>What is inside</h3>%s%s</div>
</div>
<div class="note"><b>How to order:</b> message us on WhatsApp and we'll send you payment details. Once paid, we send the PDF straight away, or print and deliver your copy. Delivery is charged separately.</div>
<h2>Better together</h2><p>%s Get both books for R299 as PDFs, or R499 printed.</p>
%s
%s</div>''' % (eb, h, lead, ed, edtxt, pdf, printword, printed,
               btns((wa("Hi, I'd like to order %s as a PDF, R%d." % (title, pdf)), 'Order the PDF'), (wa("Hi, I'd like to order a printed copy of %s, R%d plus delivery." % (title, printed)), 'Order a printed copy')),
               img, title, who_intro, ul(who), ul(inside), extra, othertxt,
               btns((wa("Hi, I'd like to order both Quiet Progress books as PDFs, R299."), 'Order both as PDFs, R299'), (wa("Hi, I'd like to order printed copies of both Quiet Progress books, R499 plus delivery."), 'Order both printed, R499')), MORE))
book('/the-power-of-quiet-progress/', 'The Power of Quiet Progress (Learner Edition)', 'The Power of Quiet Progress', 'Not every learner improves loudly.',
     'Some learners improve quietly: step by step, mistake by mistake, until one day it starts making sense.', 'learner-edition.jpg', 'Learner Edition',
     'A practical guide for learners who work hard but feel behind, rushed or discouraged. It shows how to learn from mistakes, build study habits that fit a real school week, and notice the progress that marks do not always show.',
     149, 249, 'Printed copy', 'Learners in upper primary and high school who:',
     ['feel behind or slower than their classmates', 'work hard but do not see it in their marks', 'are not sure how to study on their own', 'lose heart after mistakes or feedback'],
     ['10 short chapters, each with a relatable school story', 'Practical steps for Maths and English in every chapter', 'Reflection pages to plan, try and check what works', 'A 14-day Quiet Progress plan', 'A study-tool quick reference and a guide on when to ask for help'], '',
     '/the-quiet-progress-method/', 'Pair it with <a href="/the-quiet-progress-method/">The Quiet Progress Method</a>, our family edition that helps parents support homework calmly at home.')
book('/the-quiet-progress-method/', 'The Quiet Progress Method (Family Edition)', 'The Quiet Progress Method', 'Calmer homework, together.',
     'You do not need to know every answer to help your child learn. A calm start, a few good questions and a plan you can keep make a real difference.', 'family-edition.jpg', 'Family Edition',
     "A hands-on homework workbook for parents and children. Twelve short lessons help you turn tense homework evenings into calm, steady progress, using your child's real homework.",
     199, 329, 'Printed, spiral-bound copy', 'Parents and caregivers who:',
     ['dread the daily homework battle', 'are not sure how to help without doing the work for their child', 'want homework to start with less resistance', 'want simple tools for Maths, reading and writing at home'],
     ['12 lessons, each with a parent guide and words to try', '12 activities to do together, using real homework', '12 printable tools and weekly check-ins', 'Conversation scripts and a reset plan for hard evenings', 'Reusable maths models, reading cards and writing prompts'],
     '<p class="mut">The printed copy is spiral-bound so it lies flat for writing. With the PDF, print the pages as often as you need for your own household.</p>',
     '/the-power-of-quiet-progress/', 'Pair it with <a href="/the-power-of-quiet-progress/">The Power of Quiet Progress</a>, the learner edition your child can work through on their own.')

# ---------------- Mathematics (topic overview)
TOP = [('Number operations', 'Master the basics that power all of mathematics.', ['Addition strategies (mental maths, regrouping)', 'Subtraction techniques (borrowing, inverse operations)', 'Multiplication (tables, long multiplication, area models)', 'Division (short division, long division, remainders)', 'Order of operations (BODMAS)', 'Word problems and real-life applications']),
       ('Fractions', 'From parts to wholes: understand the language of sharing.', ['Proper, improper and mixed fractions', 'Equivalent fractions', 'Comparing and ordering fractions', 'Adding and subtracting fractions', 'Multiplying and dividing fractions', 'Converting between fractions and decimals']),
       ('Decimals', 'Precision and place value made simple.', ['Place value and rounding', 'Adding, subtracting, multiplying, dividing decimals', 'Converting between decimals and fractions', 'Comparing and ordering decimals', 'Real-world applications (money, measurements)']),
       ('Percentages', 'Unlock the power of proportions.', ['Understanding percentages', 'Converting between fractions, decimals and percentages', 'Percentage of a quantity', 'Percentage increase and decrease', 'Discounts, interest and profit calculations']),
       ('Time', 'Master the rhythm of life, one tick at a time.', ['Reading analogue and digital clocks', 'Converting between units (seconds, minutes, hours, days)', 'Calculating elapsed time and duration', 'Time zones and calendars', 'Real-life applications: schedules, travel, planning']),
       ('Measurement', 'Measure your world with confidence.', ['Units of length, mass, volume and time', 'Metric and imperial conversions', 'Perimeter, area and volume', 'Temperature and time calculations', 'Estimation and accuracy']),
       ('Finance', 'Smart money skills for everyday life.', ['Budgeting and saving', 'Income and expenses', 'Simple and compound interest', 'Currency conversions', 'Financial decision-making']),
       ('Data handling', 'Make sense of numbers and trends.', ['Collecting and organising data', 'Bar graphs, pie charts, line graphs', 'Mean, median, mode and range', 'Interpreting tables and diagrams', 'Surveys and data analysis']),
       ('Patterns and sequences', 'Spot the rhythm in numbers.', ['Number patterns and rules', 'Arithmetic and geometric sequences', 'Function machines', 'Predicting terms in a sequence']),
       ('Geometry', 'Shapes, space and structure.', ['Types of angles and their properties', 'Triangles, quadrilaterals, polygons', 'Symmetry, transformations and tessellations', '2D vs 3D shapes', 'Nets and surface area']),
       ('Algebra', 'From unknowns to understanding.', ['Expressions and equations', 'Solving for variables', 'Simplifying and expanding', 'Linear equations and inequalities', 'Substitution and formulae']),
       ('Trigonometry', 'From angles to action.', ['Understanding sine, cosine and tangent', 'Right-angled triangle ratios', 'Using SOH-CAH-TOA to solve problems', 'Angle of elevation and depression', 'Real-world applications: architecture, navigation, physics']),
       ('Statistics', 'Turn data into decisions.', ['Types of data (categorical, numerical)', 'Frequency tables and histograms', 'Measures of central tendency', 'Interpreting statistical results', 'Real-world data analysis']),
       ('Probability', 'Predict the possible.', ['Likelihood and chance', 'Experimental vs theoretical probability', 'Probability scales', 'Tree diagrams and outcomes', 'Real-life applications (games, risk)'])]
page('/mathematics/', 'Mathematics', 'Maths for learners from Grade 4 to Grade 12, and adults revisiting the basics.', '''<div class="wrap page wide">
<div class="eb">Mathematics</div><h1>The building blocks of confidence</h1>
<p class="lead">Whether you're a learner struggling with the basics or someone sharpening your skills, these topics unlock the core of mathematics. They aren't just operations: they're the building blocks of confidence, logic and lifelong learning.</p>
<div class="cards">
 <div class="card"><h3>Who is it for?</h3>%s</div>
 <div class="card"><h3>Why learn with us?</h3>%s</div>
</div>
<h2>Browse the topics</h2>
<div class="topics">%s</div>
%s</div>''' % (ul(['Learners from Grade 4 to Grade 12', 'Adults revisiting foundational maths', 'Anyone who wants to turn fear into fluency']),
               ul(['Tutoring that meets you where you are', 'Faith-rooted motivation to uplift your mindset as you learn', 'Creative methods that make maths feel natural, not stressful', 'Live support from a tutor who believes in your growth']),
               ''.join('<div><h3>%s</h3><p class="mut">%s</p>%s</div>' % (t, d, ul(i)) for t, d, i in TOP),
               btns(('/workbooks/', 'See the workbooks'), ('/tutoring/', 'Tutoring'))))

# ---------------- About
page('/about/', 'About', 'KnowledgeEmpowers is home to GROW: maths workbooks and tutoring for real understanding.', '''<div class="wrap page">
<div class="eb">About</div><h1>Who we are</h1>
<p class="lead">KnowledgeEmpowers is home to GROW. Our maths workbooks and tutoring help learners catch up, keep up and get ahead with real understanding, not just a completed page. One topic, in depth. Works alongside any curriculum.</p>
<h2>Who's behind GROW</h2>
<p>GROW is run by Pelocus Org (Pty) Ltd, a registered South African company, not a one-person side project. That matters for a few concrete reasons:</p>
%s
<h2>What we do</h2>%s
<h2>Our values</h2>%s
<h2>Find us</h2><p>You can also find KnowledgeEmpowers on Google: <a href="https://share.google/AsMWbROCykluLpB91">our business listing</a>.</p>
<p class="note">Our mission is to help every learner understand maths, one topic at a time, and to grow through what they go through.</p>
</div>''' % (ul(['<b>Every tutor is vetted before they work with a child.</b> Our vetting includes police clearance checks and reference checks: the same standard we\'d want for our own children.',
                 '<b>One team, one standard.</b> The workbooks, the tutoring and the support you get when you email us all come from the same small team, so nothing falls through the cracks.',
                 '<b>Your purchase is handled properly.</b> When you buy through KnowledgeEmpowers, you\'re buying directly from Pelocus Org (Pty) Ltd (Reg. No. 2020/864381/07), trading as GROW: an accountable company, not an anonymous storefront.']),
             ul(['<b>Tutoring and academic support:</b> personal help in English and Mathematics', '<b>Workbooks and exam packs:</b> maths for Grades 4 to 12, one topic at a time', '<b>Faith and motivation:</b> daily declarations and encouragement to keep you focused and resilient', '<b>Free maths tools:</b> <a href="/digital-empowerment/">interactive tools that help your child see the maths</a>']),
             ul(['<b>Integrity:</b> every word and resource is crafted with honesty and originality.', '<b>Clarity:</b> we simplify complexity so you can focus on what matters.', '<b>Faith:</b> we believe transformation begins when you refuse to give up.', '<b>Empowerment:</b> every service is designed to strengthen your mind, heart and spirit.'])), '/about/')
page('/about/contact/', 'Contact', "Questions about workbooks, exam packs or tutoring? We'd love to hear from you.", '''<div class="wrap page">
<div class="eb">Contact</div><h1>We'd love to hear from you</h1>
<p class="lead">Whether you have questions about workbooks, exam packs, tutoring, motivational resources or collaborations, we're here to connect. Reach out today and let's grow through what we go through.</p>
%s
<p><b>Email:</b> <a href="mailto:knowledgeempowers08@gmail.com">knowledgeempowers08@gmail.com</a><br><b>WhatsApp:</b> <a href="%s">+27 61 581 8059</a></p>
<p><b>TikTok:</b> <a href="https://www.tiktok.com/@knowledgeempowers2">@knowledgeempowers2</a> (spoken word and motivational content)<br><b>Facebook:</b> KnowledgeEmpowers (updates and inspiration)</p>
<div class="note"><b>Response time:</b> we aim to reply within 2–4 hours. For urgent questions, WhatsApp is the fastest way to reach us. All communication is handled with respect, integrity and confidentiality.</div>
</div>''' % (btns((WA, 'Chat on WhatsApp'), ('mailto:knowledgeempowers08@gmail.com', 'Send an email')), WA), '/about/')
page('/about/privacy-policy/', 'Privacy Policy', 'How KnowledgeEmpowers collects, uses and protects your personal information.', '''<div class="wrap page">
<div class="eb">About</div><h1>Privacy Policy</h1>
<p class="lead">At KnowledgeEmpowers, we value your privacy. This policy explains how we collect, use and protect your personal information when you visit our site, purchase digital products, or interact with affiliate links.</p>
<h2>1. Child safety</h2>
<p>Every tutor in the KnowledgeEmpowers network completes a Police Clearance Certificate and signs a child safeguarding declaration before they are ever matched with a learner. You're not just choosing a tutor: you're choosing someone who will spend time with your child, and we treat that responsibility accordingly. If you ever have a question or concern about a tutor's conduct, you're welcome to reach out to us directly at any time.</p>
<p>Every tutor is police-cleared before working with learners. Every tutor signs a child safeguarding declaration. Your information is handled securely and confidentially, in line with South Africa's POPIA.</p>
<h2>2. Information we collect</h2><p>We may collect:</p>%s
<h2>3. How we use your information</h2><p>We use your data to:</p>%s
<h2>4. Affiliate disclosure</h2><p>Some links on this site are affiliate links. If you purchase through them, we may earn a small commission, at no extra cost to you. We only promote tools and platforms we believe in.</p>
<h2>5. Data protection</h2><p>We take reasonable steps to protect your data:</p>%s
<h2>6. Your rights</h2><p>You can:</p>%s
<h2>7. Cookies</h2><p>We use cookies to enhance your experience. You can disable cookies in your browser settings.</p>
<h2>8. Changes to this policy</h2><p>We may update this policy. Changes will be posted on this page with a revised date.</p>
<h2>9. Contact us</h2><p>If you have questions, email us at <a href="mailto:knowledgeempowers08@gmail.com">knowledgeempowers08@gmail.com</a>.</p>
</div>''' % (ul(['Name and email address (when you contact us or make a purchase)', 'Payment details (processed securely via third-party platforms)', 'Usage data (via cookies and analytics tools)']),
             ul(['Process orders and deliver downloads', 'Respond to inquiries and provide support', 'Improve site performance and user experience', 'Share relevant affiliate offers (only those we trust)']),
             ul(['Secure payment gateways', 'No selling or renting of personal information', 'Limited access to user data']),
             ul(['Request access to your data', 'Ask for corrections or deletion', 'Opt out of marketing communications'])), '/about/')
page('/about/terms-and-conditions/', 'Terms and conditions', 'The terms for using KnowledgeEmpowers.online and buying our products.', '''<div class="wrap page">
<div class="eb">About</div><h1>Terms and conditions</h1>
<p class="lead">By accessing and using KnowledgeEmpowers.online, you agree to comply with these Terms and Conditions. If you do not agree, please discontinue use of the site.</p>
<h2>1. Use of content</h2>%s
<h2>2. User responsibilities</h2>%s
<h2>3. Purchases and downloads</h2>%s
<h2>4. Affiliate disclosure</h2><p>Some links may be affiliate links. If you purchase through them, KnowledgeEmpowers may earn a small commission, at no extra cost to you. We only promote tools and platforms we trust.</p>
<h2>5. Limitation of liability</h2>%s
<h2>6. Privacy and data protection</h2><p>Your privacy is important. Please review our <a href="/about/privacy-policy/">Privacy Policy</a> for details on how we collect and protect your information.</p>
<h2>7. Changes to terms</h2><p>We may update these Terms and Conditions at any time. Changes will be posted on this page with a revised date.</p>
<h2>8. Contact us</h2><p>Email <a href="mailto:knowledgeempowers08@gmail.com">knowledgeempowers08@gmail.com</a> or WhatsApp <a href="%s">+27 61 581 8059</a>.</p>
</div>''' % (ul(['All content on this site, including text, graphics and resources, is original and protected.', 'You may not copy, reproduce or distribute materials without prior written consent.', 'Content is provided for educational, motivational and informational purposes only.']),
             ul(['Visitors must use the site lawfully and respectfully.', 'You agree not to misuse the site for harmful, illegal or disruptive activities.', 'Any comments, submissions or interactions must remain constructive and free of offensive language.']),
             ul(['Orders are placed on WhatsApp. We send payment details when you order.', 'Digital packs and personal codes are sent once payment is received.', 'Printed packs are delivered for a separate fee.', 'Each code is for one learner and works on up to 2 devices. Workbook codes last 12 months from the day you pay. Exam pack codes work for one school term.', 'Refunds are handled on a case-by-case basis, depending on the nature of the product.', 'Free resources are offered for personal use only and may not be resold.']),
             ul(["We strive for accuracy, but we cannot guarantee that all content is error-free.", 'KnowledgeEmpowers is not liable for damages arising from the use or misuse of site content.', 'Users are responsible for applying information appropriately in their own contexts.']), WA), '/about/')
print('built')

# =====================================================================
# Classic design with previews of the real content (these replace the
# simpler versions above). Photos of printed books come later.
# =====================================================================
def F(a, b): return '<span class="f"><span>%s</span><span>%s</span></span>' % (a, b)
def win(src, alt, cap=''):
    return '<figure><div class="win"><img src="/assets/preview/%s" alt="%s" loading="lazy"></div>%s</figure>' % (src, alt, '<figcaption>%s</figcaption>' % cap if cap else '')
def stack(a, b, cap=''):
    return '<figure><div class="pages"><img src="/assets/preview/%s" alt="" loading="lazy"><img src="/assets/preview/%s" alt="" loading="lazy"></div>%s</figure>' % (a, b, '<figcaption>%s</figcaption>' % cap if cap else '')
def row(fig, eb, h, p, price, link, text, flip=False):
    return '<div class="row%s">%s<div class="txt"><div class="eb">%s</div><h2>%s</h2><p class="mut">%s</p>%s<a class="link" href="%s">%s</a></div></div>' % (
        ' flip' if flip else '', fig, eb, h, p, '<p class="price">%s</p>' % price if price else '', link, text)

TRY = '''<section class="band"><div class="wrap">
  <div class="sec-head"><div class="eb">Try it now</div><h2>See how a question works</h2><p class="mut">Get it wrong on purpose. You'll see a hint first, then every step, the way it works in our workbooks.</p></div>
  <div class="try" id="try">
    <div class="eb" style="color:var(--m)">Fractions · Grades 5–6</div>
    <div class="q">Simplify %s fully.</div>
    <form id="tryF"><input id="tryA" inputmode="text" autocomplete="off" placeholder="Your answer, e.g. 3/4" aria-label="Your answer"><button class="btn" type="submit">Check</button></form>
    <div class="fb" id="tryFb"></div>
    <div class="steps-sol" id="trySteps"><b>Step by step</b><ol>
      <li><span class="r">Rule:</span> divide the top and the bottom by the same number, the highest common factor (HCF).</li>
      <li>Factors of 12: 1, 2, 3, 4, 6, 12. Factors of 18: 1, 2, 3, 6, 9, 18. The HCF is 6.</li>
      <li>%s = %s</li>
      <li>2 and 3 have no common factor except 1, so %s is in simplest form.</li></ol></div>
    <p class="mut" style="font-size:.9rem">Want more? <a href="/free-classroom-practice/?t=fractions&amp;m=practice">Practise 15 fraction questions free →</a></p>
  </div>
</div></section>
<script>
(function(){var f=document.getElementById('tryF'),a=document.getElementById('tryA'),fb=document.getElementById('tryFb'),st=document.getElementById('trySteps'),tries=0;
function val(t){t=t.replace(/\\s+/g,'');var m=t.match(/^(-?\\d+)\\/(\\d+)$/);if(m)return [+m[1],+m[2]];if(/^-?\\d+(\\.\\d+)?$/.test(t))return [parseFloat(t),1];return null}
f.addEventListener('submit',function(e){e.preventDefault();var v=val(a.value);if(!v){fb.className='fb hint show';fb.innerHTML='Type a fraction, like 3/4.';return}
 if(v[0]===2&&v[1]===3){fb.className='fb ok show';fb.innerHTML='<b>Correct.</b> 12 ÷ 6 = 2 and 18 ÷ 6 = 3.';st.classList.add('show');return}
 tries++;var same=Math.abs(v[0]/v[1]-2/3)<1e-9;
 if(same){fb.className='fb hint show';fb.innerHTML='<b>Right value.</b> Now simplify your fraction fully.';return}
 if(tries===1){fb.className='fb hint show';fb.innerHTML='<b>Not quite. Here is a hint:</b> divide the top and the bottom by the same number. Which number divides into both 12 and 18?'}
 else{fb.className='fb hint show';fb.innerHTML='<b>Not yet.</b> Follow the steps below.';st.classList.add('show')}});})();
</script>''' % (F(12, 18), F('12 ÷ 6', '18 ÷ 6'), F(2, 3), F(2, 3))

HOME = '''<div class="wrap hero">
  <div class="txt">
    <div class="eb">Maths for Grades 4 to 12</div>
    <h1>One topic, in depth.</h1>
    <hr class="rule">
    <p class="lead">Workbooks, exam packs and free practice for learners in South African public, IEB and Cambridge schools. Every answer shown step by step.</p>
    %s
  </div>
  <figure class="duo"><div class="win"><img src="/assets/preview/classroom.jpg" alt="A worked solution on the classroom screen"></div><div class="phone"><img src="/assets/preview/practice-phone.jpg" alt="A practice question on a phone"></div></figure>
</div>
<section class="band"><div class="wrap">
  <div class="sec-head"><div class="eb">How it works</div><h2>Start where your child really is</h2></div>
  <div class="steps">
    <div><span class="n">i</span><h3>Take the free maths check</h3><p class="mut">Short questions that show which topics are secure and which need work.</p></div>
    <div><span class="n">ii</span><h3>Choose what fits</h3><p class="mut">A workbook or exam pack for exactly the gaps the check found.</p></div>
    <div><span class="n">iii</span><h3>Start the same day</h3><p class="mut">Your access code arrives on WhatsApp, or a printed book is delivered.</p></div>
  </div>
</div></section>
<section><div class="wrap">
  %s
  %s
  %s
  %s
</div></section>
%s
<section class="quote"><img src="/assets/img/seedling.jpg" alt=""><div class="wrap">
  <div class="eb">Our promise</div><h2>“Don't give up. Grow through what you go through.”</h2>
</div></section>
<section><div class="wrap">
  <div class="sec-head"><div class="eb">Free for everyone</div><h2>Start today, no sign-up</h2></div>
  <div class="cards3">
    <a class="pcard" href="/baseline-assessment/"><div class="win"><img src="/assets/preview/check-phone.jpg" alt="" style="aspect-ratio:1/1.05;object-fit:cover;object-position:top"></div><h3>Free maths check</h3><p class="mut">Find the gaps in 10 to 30 minutes, with a report straight away.</p><span class="go">Start the check →</span></a>
    <a class="pcard" href="/free-classroom-practice/"><div class="win"><img src="/assets/preview/topics.jpg" alt="" style="aspect-ratio:1/1.05;object-fit:cover;object-position:left top"></div><h3>Free classroom and practice</h3><p class="mut">Show a lesson on the classroom screen, or practise at home.</p><span class="go">Start practising →</span></a>
    <a class="pcard" href="/digital-empowerment/"><div class="win"><img src="/assets/preview/book-adding.jpg" alt="" style="aspect-ratio:1/1.05;object-fit:cover;object-position:top"></div><h3>Free maths tools</h3><p class="mut">Interactive tools that help your child see the maths.</p><span class="go">Open the tools →</span></a>
  </div>
</div></section>''' % (btns(('/baseline-assessment/', "Find my child's gaps, free"), ('/shop/', 'Visit the shop')),
   row(win('practice-hint.jpg', 'A practice question showing a hint', 'A wrong answer brings a hint first, then the full steps.'), 'Online workbooks', 'Every topic, from the rule to the answer',
       'One maths topic in depth. Learners can work on their own: a hint after one wrong try, then the full worked solution, rule first.', 'R149 a year for Grades 4–9 · R199 for Grades 10–12', '/workbooks/', 'See the workbooks'),
   row(stack('book-cover.jpg', 'book-teach.jpg', 'Inside the Fractions workbook: teach, worked example, watch out.'), 'Printed workbooks', 'One book, from the first concept to the last',
       'About 100 pages in full colour for each topic, from Diagnose to Master. Also in two parts: Building blocks and Taking it further.', 'R199 · members R169', '/shop/', 'See the shop', True),
   row(win('classroom.jpg', 'A worked solution on the classroom screen'), 'Exam packs', 'Ready for the end-of-year exam',
       "Revision for every topic with worked examples, mock exam papers with full memos, a formula sheet and a progress tracker for your child's grade.", 'From R100', '/exam-packs/', 'See the exam packs'),
   row(stack('diary-summary.jpg', 'diary-reference.jpg', 'Inside My Maths Diary: the weekly summary, and formulas with the reasoning behind them.'), 'My Maths Diary', 'Small steps, written down, every week',
       'A full-year diary for Grades 4–7, 8–9 and 10–12: weekly summaries, a mistake bank, a marks tracker and a maths reference.', 'From R79', '/shop/', 'See the diaries', True),
   TRY)
page('/', 'Maths for Grades 4 to 12', 'Maths workbooks, exam packs and free practice for Grades 4 to 12. One topic, in depth. Works alongside any curriculum.', HOME)

# ---------------- Workbooks (visual)
STEPS9 = ['Diagnose', 'Build', 'Teach', 'Guide', 'Practise', 'Apply', 'Assess', 'Remediate', 'Master']
page('/workbooks/', 'Maths workbooks, Grades 4 to 12 · online and printed', 'Grade 4 to 12 maths workbooks, online and printed. One topic in depth, every answer worked step by step. For public school, IEB and Cambridge learners.', '''<div class="wrap hero">
  <div class="txt"><div class="eb">Workbooks</div><h1>One topic at a time, Grades 4 to 12</h1><hr class="rule">
  <p class="lead">Each workbook takes one maths topic in depth, and works alongside any curriculum.</p>%s</div>
  %s
</div>
<section style="padding-top:0"><div class="wrap page" style="padding-block:0;margin:0 auto">
  <p>Looking for a Grade 4, 5, 6, 7, 8 or 9 maths workbook that actually explains the work? Each KnowledgeEmpowers workbook takes one topic, such as fractions, integers or algebra, from the first idea to exam level, with every answer worked step by step. For Grades 10 to 12, the senior series covers functions, trigonometry, algebra and more. They work alongside any curriculum: public schools, IEB and Cambridge.</p>
</div></section>
<section class="band"><div class="wrap">
  <div class="sec-head"><div class="eb">How every topic is built</div><h2>Nine steps, from Diagnose to Master</h2><p class="mut">Learners start where they really are, not where their grade says.</p></div>
  <div class="steps" style="grid-template-columns:repeat(3,minmax(0,1fr))">%s</div>
</div></section>
<section><div class="wrap">
  %s
  %s
</div></section>
<section class="band"><div class="wrap page" style="padding-block:0;margin:0 auto">
  <h2>Prices</h2>
  <h3>All topics online</h3>%s
  <h3>Printed workbook</h3>%s
  <p class="mut">Delivery of printed workbooks is charged separately.</p>
  <div class="note"><b>How to order:</b> message us on WhatsApp with your child's grade. Pay using the details we send you, then receive your personal code. Each code is for one learner, lasts 12 months from the day you pay, and works on up to 2 devices.</div>
  %s
</div></section>''' % (btns((wa("Hi, I'd like to order a workbook. Topic and grade: "), 'Order on WhatsApp'), (LOGIN, 'I already have a code')),
   stack('book-cover.jpg', 'book-teach.jpg'),
   ''.join('<div><span class="n">%d</span><h3>%s</h3></div>' % (i + 1, t) for i, t in enumerate(STEPS9)),
   row(win('practice-hint.jpg', 'A hint after a wrong answer'), 'Online', 'A hint first, then every step', 'A wrong answer brings a hint first. A second try shows the full worked solution, starting with the rule, so learners can work on their own and parents do not need to know every answer.', '', '/free-classroom-practice/?t=fractions&m=practice', 'Try a free practice set'),
   row(stack('book-teach.jpg', 'book-adding.jpg'), 'Printed', 'Teach, worked example, watch out', 'Every concept explains the rule, works an example step by step, and warns about the mistake learners usually make. In full colour and bound.', '', '/shop/', 'See printed workbooks', True),
   prices([('Grades 4–9', 'R149 a year'), ('Grades 10–12', 'R199 a year')]), prices([('One topic', 'R199 (members R169)'), ('Part 1 or Part 2', 'R109 (members R99)')]),
   btns((wa("Hi, I'd like to order a workbook. Topic and grade: "), 'Order on WhatsApp'), ('/baseline-assessment/', 'Not sure? Take the free maths check'))), '/workbooks/')

# ---------------- Exam packs (visual)
page('/exam-packs/', 'Maths exam revision packs with memos, Grades 4 to 12', 'End-of-year maths exam revision for Grades 4 to 12: every topic, mock papers with full memos, a formula sheet and a progress tracker. Online, PDF or printed.', '''<div class="wrap hero">
  <div class="txt"><div class="eb">Exam packs</div><h1>Ready for the end-of-year exam</h1><hr class="rule">
  <p class="lead">One pack for your child's grade, Grades 4 to 12, for South African (public and IEB) and Cambridge learners.</p>
  <p>Inside: revision for every topic with worked examples, mock exam papers with full memos, a formula sheet and a progress tracker.</p>%s</div>
  %s
</div>
<section style="padding-top:0"><div class="wrap page" style="padding-block:0;margin:0 auto">
  <p>Preparing for the end-of-year maths exam? Each exam pack has revision for every topic in your child's grade, mock exam papers with full memos, a formula sheet and a progress tracker. Use it online or print it. It suits public school, IEB and Cambridge learners in Grades 4 to 12.</p>
</div></section>
<section class="band"><div class="wrap page" style="padding-block:0;margin:0 auto">
  <h2>Prices</h2>
  <h3>Grades 4 to 9</h3>%s
  <h3>Grades 10 to 12</h3>%s
  <p class="mut">Delivery of printed packs is charged separately.</p>
  <div class="note"><b>How to order:</b> message us on WhatsApp with your child's grade and the pack you want. Pay using the details we send you. Then receive your pack and personal code. Each code is for one learner and works for one school term on up to 2 devices.</div>
  %s
</div></section>''' % (btns((wa("Hi, I'd like to order an Exam Pack. Grade: "), 'Order on WhatsApp'), ('/exam-packs/exam-preparation-packs/', 'I already have a code')),
   '<figure class="pic"><img src="/assets/img/printed-in-hand.jpg" alt="A printed, comb-bound Grade 7 exam pack and My Maths Diary" style="border-radius:6px"></figure>',
   prices([('Online', 'R149'), ('PDF', 'R100'), ('Printed', 'R199')]), prices([('Online', 'R199'), ('PDF', 'R149'), ('Printed', 'R250')]),
   btns((wa("Hi, I'd like to order an Exam Pack. Grade: "), 'Order on WhatsApp'))), '/exam-packs/')

# ---------------- Grow at home (visual)
page('/grow-at-home/', 'Grow at home', 'Books for learners and parents, free maths tools and guides on faith.', '''<div class="wrap hero">
  <div class="txt"><div class="eb">Beyond the classroom</div><h1>Calm habits, strong minds, real skills.</h1><hr class="rule">
  <p class="lead">Books for learners and parents, plus free maths tools and guides on faith. Small steps at home that help your child grow.</p></div>
  <figure><img src="/assets/img/seedling.jpg" alt="A young plant growing" style="width:100%%;aspect-ratio:4/3.2;object-fit:cover"></figure>
</div>
<section style="padding-top:0"><div class="wrap">
  <div class="cards3">
    <a class="pcard" href="/the-power-of-quiet-progress/"><img src="/assets/img/learner-edition.jpg" alt="" style="object-position:top"><h3>The Power of Quiet Progress</h3><p class="mut">Learner Edition · from R149</p><span class="go">See the book →</span></a>
    <a class="pcard" href="/the-quiet-progress-method/"><img src="/assets/img/family-edition.jpg" alt="" style="object-position:top"><h3>The Quiet Progress Method</h3><p class="mut">Family Edition · from R199</p><span class="go">See the book →</span></a>
    <a class="pcard" href="/shop/"><img src="/assets/preview/diary-covers.jpg" alt=""><h3>My Maths Diary</h3><p class="mut">A full-year diary for Grades 4–7, 8–9 and 10–12.</p><span class="go">See the shop →</span></a>
    <a class="pcard" href="/free-classroom-practice/"><img src="/assets/preview/classroom.svg" alt=""><h3>Free practice</h3><p class="mut">Every answer shown step by step.</p><span class="go">Start →</span></a>
    <a class="pcard" href="/digital-empowerment/"><div class="win"><img src="/assets/preview/book-adding.jpg" alt="" style="aspect-ratio:1/1.05;object-fit:cover;object-position:top"></div><h3>Free maths tools</h3><p class="mut">Interactive tools that help your child see the maths.</p><span class="go">Open →</span></a>
    <a class="pcard" href="/motivation-faith/"><img src="/assets/img/seedling.jpg" alt=""><h3>Motivation &amp; Faith</h3><p class="mut">Prepare yourself, because life won't wait.</p><span class="go">Read →</span></a>
  </div>
</div></section>''')

# ---------------- Tutoring (visual hero)
page('/tutoring/', 'Tutoring', 'One-to-one online maths and English lessons for Grades 4 to 10.', '''<div class="wrap hero">
  <div class="txt"><div class="eb">Tutoring</div><h1>One-to-one online lessons, Grades 4 to 10</h1><hr class="rule">
  <p class="lead">We start where your child is, and stay with a topic until it makes sense. Each lesson is tailored to the learner's needs, schoolwork and goals, with clear explanations and guided practice.</p>%s</div>
  %s
</div>
<section class="band"><div class="wrap page" style="padding-block:0;margin:0 auto">
  <h2>Lesson prices</h2>%s
  <p>Message us on WhatsApp to discuss your child's grade, learning goals and available lesson times.</p>
  <div class="cards">
   <div class="card"><h3>Mathematics tutoring</h3><p class="mut">Clear explanations, step-by-step guidance and personal support.</p>%s<a class="link" href="/tutoring/mathematics-tutoring-grades-5-10/">Learn more</a></div>
   <div class="card"><h3>English HL/FAL tutoring</h3><p class="mut">Reading, writing, grammar, comprehension and exam performance.</p>%s<a class="link" href="/tutoring/english-hl-or-fal-tutoring-grades-4-10/">Learn more</a></div>
  </div>
</div></section>''' % (btns(('https://wa.me/message/XAFTSZAMNG6IO1', 'Enquire about lessons')), win('classroom.jpg', 'A step-by-step solution on screen', 'Lessons on Google Meet, working through each step together.'),
   prices([('Single 60-minute lesson', 'R250'), ('4 online lessons', 'R900')]),
   ul(['One-on-one online lessons', 'Group classes available', 'Exam preparation and revision', 'Homework support', 'Problem-solving and confidence']),
   ul(['Group classes', 'Essay and creative writing support', 'Comprehension strategies', 'Speaking and listening skills'])), '/tutoring/')
print('visual pages built')

# ---------------- Home (brand hero, orderly grid) — final version
_h = TRY.index('<div class="sec-head">'); _e = TRY.index('</div>', TRY.index('<p class="mut">Get it wrong')) + len('</div>')
TRY2 = TRY[:_h] + '''<div class="try-split"><div style="display:grid;gap:18px"><div class="eb">Try it now</div><h2>See how a question works</h2><hr class="rule">
<p class="mut">Get it wrong on purpose. You'll see a hint first, then every step, starting with the rule. That's how every question in our workbooks works, so learners can keep going on their own.</p></div>''' + TRY[_e:]
TRY2 = TRY2.replace('\n</div></section>\n<script>', '\n</div></div></section>\n<script>', 1)

def offer(href, img, pos, title, text, price, go):
    return '<a href="%s"><div class="pic"><img src="/assets/preview/%s" alt="" loading="lazy" style="object-position:%s"></div><div class="body"><h3>%s</h3><p class="mut">%s</p><p class="price">%s</p><span class="go">%s →</span></div></a>' % (href, img, pos, title, text, price, go)

GOOGLE = 'https://share.google/AsMWbROCykluLpB91'
FAQ = [
 ("How does my child get access?", "Message us on WhatsApp and we send the payment details. Once you have paid, your child's personal code arrives on WhatsApp, usually the same day."),
 ("How long does access last?", "Online workbooks: 12 months from the day you pay, for every topic in the series. Exam packs: one school term."),
 ("Which grade should I buy?", "Workbooks are made by topic, not by grade, so one book takes a learner from the first idea to the last. Not sure where to start? The free maths check shows which topics to work on first."),
 ("Does it work with my child's school?", "Yes. It works alongside any curriculum: public schools, IEB and Cambridge."),
 ("Which devices does it work on?", "Any phone, tablet or computer with a browser. Each code works on up to two devices."),
 ("Do you have prices for more than one child?", "A second child in the same family pays half price. Tutors and schools pay R79 per learner for 10 learners or more."),
 ("How are printed books delivered?", "We print in full colour, bind them and post them to you. Delivery is charged separately."),
]

# Real Google reviews (add more here as they come in: quote, name, what it was about)
QUOTES = [
 ("The tutor was professional, supportive, and always willing to help. She provided quality service and created a welcoming environment.", "Oluhle S.", "Tutoring"),
 ("Very excellent service! The tutor is very friendly, knowledgeable, and very helpful. I had a great experience with her and I would really recommend her service to others.", "Asanda N.", "Tutoring"),
]
def quotes():
    return ('<section class="says"><div class="wrap"><div class="sec-head"><div class="eb">What people say</div><h2>Rated 5.0 on Google</h2>'
            '<p class="mut"><span class="stars" aria-label="5 out of 5 stars">★★★★★</span> From every review so far. <a href="%s" target="_blank" rel="noopener">Read them on Google</a></p></div>'
            '<div class="says-grid">%s</div></div></section>') % (GOOGLE, ''.join(
            '<figure><span class="stars" aria-hidden="true">★★★★★</span><blockquote>“%s”</blockquote><figcaption><b>%s</b> · Google review · %s</figcaption></figure>' % q for q in QUOTES))
def faq(items=FAQ):
    return '<div class="faq">' + ''.join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in items) + '</div>'
def path(eb, h, p, items, b1, b2):
    return '<div class="path-card"><div class="eb">%s</div><h3>%s</h3><p class="mut">%s</p>%s%s</div>' % (eb, h, p, '<ol>' + ''.join('<li>%s</li>' % i for i in items) + '</ol>', btns(b1, b2))
GRADES = ''.join('<option value="%d"%s>Grade %d</option>' % (g, ' selected' if g == 7 else '', g) for g in range(4, 13))
SAMPLES = [('KnowledgeEmpowers-Fractions-sample.pdf', 'Fractions workbook', 'Grades 4 to 9 · 7 pages', 'The cover, how the book works, the Diagnose page and one full concept from Teach to Master.'),
           ('KnowledgeEmpowers-Functions-and-graphs-sample.pdf', 'Functions and graphs', 'Grades 10 to 12 · 6 pages', 'The Diagnose page and the first full concept, with a worked example.'),
           ('KnowledgeEmpowers-Maths-Diary-sample.pdf', 'My Maths Diary', 'Grades 8 and 9 · 5 pages', 'One full week, how the diary works, and a reference page that shows the reasoning behind each formula.')]
def sample(fn, t, meta, d):
    return '<a class="sample" href="/assets/samples/%s" download><span class="pdf">PDF</span><span><b>%s</b><small>%s</small><span class="mut">%s</span></span><span class="go">Download</span></a>' % (fn, t, meta, d)

HOME = """<section class="brand-hero two" style="padding:0"><div class="wrap">
  <div class="txt">
    <div class="eb">KnowledgeEmpowers · Maths for Grades 4 to 12</div>
    <h1>One topic, <em>in depth.</em></h1>
    <hr class="rule">
    <p class="lead">Workbooks, exam packs and free practice that take each maths topic from the rule to the answer. Works alongside any curriculum: public, IEB and Cambridge.</p>
    <p class="hero-links"><a href="/workbooks/">See the workbooks</a><a href="/shop/">Visit the shop</a></p>
  </div>
  <aside class="start" aria-label="Start here">
    <div class="start-eb">Start here · free</div>
    <h2>Find your child’s gaps</h2>
    <form class="picker v" action="/baseline-assessment/" method="get">
      <label for="pk">My child is in</label>
      <select id="pk" name="grade">%(grades)s</select>
      <button type="submit">Start the free maths check</button>
    </form>
    <p class="start-note">10 to 30 minutes, with a report straight away.</p>
    <a class="start-today" href="/free-classroom-practice/"><span class="badge">Today’s question</span><b>A new free maths question every day</b><span class="go">Try today’s question →</span></a>
  </aside>
</div></section>
<div class="trust"><div class="wrap">
  <div><span class="i">1</span><span><b>Every answer step by step</b>Rule first, no steps skipped</span></div>
  <div><span class="i">2</span><span><b>Hint first, then the steps</b>Learners can work on their own</span></div>
  <div><span class="i">3</span><span><b>Online or printed</b>Phone, tablet, computer or paper</span></div>
  <div><span class="i">4</span><span><b>Free maths check</b>Start where your child really is</span></div>
</div></div>
<section><div class="wrap">
  <div class="sec-head"><div class="eb">Who it is for</div><h2>Two ways to start</h2></div>
  <div class="paths">%(p1)s%(p2)s</div>
</div></section>
<section class="band"><div class="wrap">
  <div class="sec-head"><div class="eb">What we offer</div><h2>Everything for one topic, in one place</h2></div>
  <div class="offer">%(o1)s%(o2)s%(o3)s</div>
</div></section>
<section class="value"><div class="wrap">
  <div class="v-txt"><div class="eb">Fair price</div><h2>R149 a year. About R12 a month.</h2><p>Every maths topic online for a full year costs less than one hour with a tutor. One payment, no monthly debit order.</p></div>
  <div class="v-cmp">
    <div class="v-row"><span>KnowledgeEmpowers online workbooks</span><b>R149 a year</b></div>
    <div class="v-row mut"><span>One tutoring lesson</span><b>R250 an hour</b></div>
    <div class="v-row mut"><span>Monthly learning apps</span><b>R149 a month</b></div>
    %(vb)s
  </div>
</div></section>
%(try2)s
<section><div class="wrap">
  <div class="sec-head"><div class="eb">Free for everyone</div><h2>Start today, no sign-up</h2></div>
  <div class="offer">%(f1)s%(f2)s%(f3)s</div>
  <div class="samples-wrap"><h3>Free sample pages</h3><p class="mut">See exactly what your child gets before you buy. Print them, try them, keep them.</p>
  <div class="samples">%(s)s</div></div>
</div></section>
%(says)s
<section class="band"><div class="wrap who">
  <div><div class="eb">Who is behind it</div><h2>A registered South African company</h2><hr class="rule" style="margin-top:18px">
  <blockquote class="founder">“I started KnowledgeEmpowers after seeing too many learners fall behind in maths, not because they couldn't do it, but because one small gap was never filled. So every workbook starts where the learner really is, and shows every step.”<cite>Founder, KnowledgeEmpowers</cite></blockquote>
  <p class="mut" style="margin-top:18px">KnowledgeEmpowers and GROW are run by Pelocus Org (Pty) Ltd (Reg. No. 2020/864381/07). One small team writes the workbooks, the exam packs and the free practice, and teaches the tutoring lessons. When you message us, you speak to the people who made it.</p></div>
  <div class="who-facts">
    <div><b>Real people on WhatsApp</b><span class="mut">We usually reply within 2 to 4 hours. <a href="https://wa.me/27615818059">061 581 8059</a></span></div>
    <div><b>Reviewed on Google</b><span class="mut">Read what parents say on our Google business profile. <a href="%(google)s" target="_blank" rel="noopener">See our reviews</a></span></div>
    <div><b>Tutors are checked</b><span class="mut">Every tutor is vetted, with police clearance and reference checks, before they work with a child.</span></div>
  </div>
</div></section>
<section><div class="wrap">
  <div class="sec-head"><div class="eb">Questions</div><h2>Common questions</h2></div>
  %(faq)s
  <p class="mut" style="text-align:center;margin-top:28px">Something else? <a href="https://wa.me/27615818059">Ask us on WhatsApp</a>.</p>
</div></section>
<section class="quote"><img src="/assets/img/seedling.jpg" alt=""><div class="wrap">
  <div class="eb">Our promise</div><h2>“Don't give up. Grow through what you go through.”</h2>
  %(qb)s
</div></section>""" % dict(
    grades=GRADES,
    p1=path('For parents', 'Find the gaps, then fix them at home', 'Start where your child really is, not where their grade says.',
            ['Take the free maths check: a report straight away.', 'Get the workbook for each topic it shows, online or printed.', 'Keep track every week with My Maths Diary.'],
            ('/baseline-assessment/', 'Start the free check'), ('/shop/', 'Visit the shop')),
    p2=path('For teachers and tutors', 'Teach one topic on the big screen', 'Show a lesson in class, then let learners practise on their own.',
            ['Open Classroom mode, free and with no sign-up.', 'Give each learner a code: R79 per learner for 10 or more.', 'Order printed sets for your class or centre.'],
            ('/free-classroom-practice/', 'Open Classroom mode'), (wa("Hi KnowledgeEmpowers, I'm a teacher/tutor and I'd like prices for my learners."), 'Ask about group prices')),
    o1=offer('/workbooks/', 'practice-hint.jpg', 'left top', 'Online workbooks', 'Every topic for a year, with a hint after one wrong try, then the full worked solution.', 'From R149 a year', 'See the workbooks'),
    o2=offer('/shop/', 'book-cover.jpg', 'center top', 'Printed workbooks', 'About 100 pages in full colour for each topic: teach, worked example, watch out.', 'From R169', 'Visit the shop'),
    o3=offer('/exam-packs/', 'exam-menu.jpg', 'left top', 'Exam packs', 'Revision, mock papers with full memos, a formula sheet and a progress tracker.', 'From R100', 'See the exam packs'),
    vb=btns(('/shop/', 'Get the online workbooks')),
    try2=TRY2,
    f1=offer('/baseline-assessment/', 'maths-check.svg', 'center', 'Free maths check', 'Find the gaps in 10 to 30 minutes, with a report straight away.', 'Free · Grades 4–12', 'Start the check'),
    f2=offer('/free-classroom-practice/', 'classroom.svg', 'center', 'Free classroom and practice', 'Show a lesson on the classroom screen, or practise at home.', 'Free · no sign-up', 'Start practising'),
    f3=offer('/shop/', 'diary-covers.jpg', 'center', 'My Maths Diary', 'A full-year diary: weekly summaries, a mistake bank and a marks tracker.', 'From R79', 'See the diaries'),
    s=''.join(sample(*x) for x in SAMPLES), google=GOOGLE, faq=faq(), says=quotes(),
    qb=btns(('/baseline-assessment/', 'Take the free maths check')).replace('class="btn"', 'class="btn" style="background:#fff;color:var(--m);border-color:#fff;margin-top:10px"'))
page('/', 'Maths for Grades 4 to 12', 'Maths workbooks, exam packs and free practice for Grades 4 to 12. One topic, in depth. Works alongside any curriculum.', HOME)
print('home v4 built')

# Not-found page (Cloudflare serves 404.html for addresses that don't exist)
import shutil as _sh
page('/not-found/', 'Page not found', 'This page could not be found.', """<section class="phead"><div class="wrap hero solo"><div class="txt"><div class="eb">Page not found</div><h1>We couldn't find that page.</h1><hr class="rule"><p class="lead">It may have moved when we updated the website.</p>%s</div></div></section>
<div class="wrap page after"><p>Try one of these:</p><ul><li><a href="/">Home</a></li><li><a href="/baseline-assessment/">Free maths check</a></li><li><a href="/workbooks/">Workbooks</a></li><li><a href="/shop/">Shop</a></li></ul></div>""" % btns(('/', 'Go to the home page'), ('https://wa.me/27615818059', 'Ask us on WhatsApp')))
_t = open('not-found/index.html').read()
_t = _re.sub(r'<link rel="canonical"[^>]*>\n?', '', _t).replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)
open('404.html', 'w').write(_t); _sh.rmtree('not-found')
print('404 built')
