#!/usr/bin/env python3
"""Generate all medeqon website pages from one shared template.
Header + footer are identical on every page; only the body changes.
Run: python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent

# ---- Navigation (main pages, in order) ----------------------------------
NAV = [
    ("index.html", "Startseite"),
    ("leistungen.html", "Leistungen"),
    ("produkte.html", "Produkte"),
    ("referenzen.html", "Referenzen"),
    ("management.html", "Management"),
    ("kontakt.html", "Kontakt"),
]

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700'
    '&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'
)
FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Crect width='100' height='100' rx='24' fill='%23004AAD'/%3E%3Ctext x='50' y='70' "
    "font-family='Arial,sans-serif' font-size='60' font-weight='700' fill='white' "
    "text-anchor='middle'%3Em%3C/text%3E%3C/svg%3E"
)

def header(active):
    def link(href, label):
        cls = ' class="active"' if label == active else ''
        return f'    <a href="{href}"{cls}>{label}</a>'
    links = "\n".join(link(href, label) for href, label in NAV)
    return f'''<header class="m-nav">
  <a class="brandlogo" href="index.html" aria-label="medeqon — Startseite">
    <span class="brandlogo-mono" aria-hidden="true">m</span>
    <span class="brandlogo-word">medeqon</span>
  </a>
  <nav class="m-nav-links" aria-label="Hauptnavigation">
{links}
  </nav>
</header>'''

FOOTER = '''<footer class="m-foot">
  <div class="m-shell m-foot-top">
    <div class="m-foot-brand">
      <a class="m-foot-logo" href="index.html" aria-label="medeqon — Startseite">
        <span class="m-foot-mono" aria-hidden="true">m</span>
        <span class="m-foot-word">medeqon</span>
      </a>
      <div class="m-foot-words">Ingenieurbüro für Medizintechnik.</div>
      <div class="m-foot-legalline">medeqon GmbH · FN 672926y · UID ATU83016237</div>
    </div>
    <div class="m-foot-links">
      <div class="m-foot-col">
        <div class="m-foot-tag">Leistungen</div>
        <a class="m-foot-svc" href="leistungen.html#planung"><svg class="m-foot-ico" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 38 L38 38 L10 12 Z"/><path d="M10 27 L21 27"/><circle cx="38" cy="38" r="2.6" class="sig-fill"/></svg><span>Planung</span></a>
        <a class="m-foot-svc" href="leistungen.html#consulting"><svg class="m-foot-ico" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 13 h26 a3 3 0 0 1 3 3 v13 a3 3 0 0 1 -3 3 H21 l-7 6 v-6 h-2 a3 3 0 0 1 -3 -3 V16 a3 3 0 0 1 3 -3 Z"/><circle cx="23" cy="22.5" r="2.4" class="sig-fill"/></svg><span>Consulting</span></a>
        <a class="m-foot-svc" href="leistungen.html#handel"><svg class="m-foot-ico" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 8 L39 16 L39 32 L24 40 L9 32 L9 16 Z"/><path d="M9 16 L24 24 L39 16"/><path d="M24 24 L24 40"/><circle cx="24" cy="24" r="2.4" class="sig-fill"/></svg><span>Handel</span></a>
        <a class="m-foot-svc" href="leistungen.html#pruefung"><svg class="m-foot-ico" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="21" cy="21" r="11"/><path d="M29 29 L39 39"/><path d="M16.5 21.5 l3.5 3.5 l6.5 -7.5" class="sig-stroke"/></svg><span>Prüfung</span></a>
      </div>
      <div class="m-foot-col">
        <div class="m-foot-tag">Kontakt</div>
        <a href="mailto:office@medeqon.com">office@medeqon.com</a>
        <a href="tel:+436705505612">+43 670 550 5612</a>
        <a href="https://www.medeqon.com">www.medeqon.com</a>
        <div class="m-foot-plain">Bergstrasse 42/5/3<br>2102 Hagenbrunn · AT</div>
      </div>
      <div class="m-foot-col">
        <div class="m-foot-tag">Rechtliches</div>
        <a href="agb.html">AGB</a>
        <a href="datenschutz.html">Datenschutz</a>
        <a href="impressum.html">Impressum</a>
      </div>
    </div>
    <div class="m-foot-badges">
      <img class="m-badge" src="assets/siegel-ingenieurbuero.png" alt="Ingenieurbüro — staatlich geprüft" loading="lazy">
      <img class="m-badge" src="assets/siegel-medizinproduktehandel.png" alt="Medizinproduktehandel — staatlich geprüft" loading="lazy">
      <img class="m-badge m-badge-wide" src="assets/siegel-ingenieurbueros-at-eu.png" alt="Ingenieurbüros Österreich · EU" loading="lazy">
    </div>
  </div>
  <div class="m-shell m-foot-base">
    <div>© 2026 medeqon GmbH</div>
    <div>MED-CI-01 · V2.0</div>
  </div>
</footer>'''

def page(filename, title, desc, active, body):
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#004AAD">
<link rel="icon" href="{FAVICON}">
{FONTS}
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip" href="#main">Zum Inhalt springen</a>

{header(active)}

<main id="main">
{body}
</main>

{FOOTER}

<script>
(function(){{
  var frames = document.querySelectorAll('.m-pl-frame');
  frames.forEach(function(f){{
    var shots = f.querySelectorAll('.m-pl-shot');
    var dots  = f.querySelectorAll('.m-pl-dots i');
    var n = shots.length;
    if (n < 2) return;
    var cur = 0;
    function show(i){{
      if (i === cur) return;
      cur = i;
      shots.forEach(function(s,k){{ s.classList.toggle('is-on', k === i); }});
      dots.forEach(function(d,k){{ d.classList.toggle('on', k === i); }});
    }}
    f.addEventListener('pointermove', function(e){{
      var r = f.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width;
      var i = Math.floor(x * n);
      if (i < 0) i = 0; if (i > n - 1) i = n - 1;
      show(i);
    }});
    f.addEventListener('pointerleave', function(){{ show(0); }});
  }});
}})();
</script>

</body>
</html>
'''

# ---- Page bodies ---------------------------------------------------------
BODY_INDEX = '''<section class="m-hero-main">
  <div class="m-shell m-hero-grid">
    <div class="m-hero-copy">
      <h1 class="m-hero-title">Ingenieurbüro für Medizintechnik<span class="end-dot">.</span></h1>
      <p class="m-hero-sub">Wir planen, liefern und betreuen medizinische Lösungen mit höchstem Qualitätsanspruch.</p>
    </div>
    <img class="m-hero-logo" src="assets/medeqon-logo-white.png" alt="medeqon" width="1618" height="335">
  </div>
</section>

<section class="m-slogan" style="background-image:url(assets/slogan-bg.jpg)">
  <div class="m-shell">
    <div class="line"></div>
    <p>Ihr Partner für den gesamten Lebenszyklus der Medizintechnik<span class="em">.</span></p>
  </div>
</section>

<section class="m-section alt">
  <div class="m-shell">
    <div class="m-secH">
      <h2 class="m-bigH">Gemeinsam gestalten wir Fortschritt<span class="end-dot">.</span></h2>
      <div class="sub">Mit unserer langjährigen Erfahrung in der Medizintechnik bieten wir ein umfassendes Leistungsspektrum, das individuell auf Ihre Anforderungen zugeschnitten ist. Ob erste Konzeptideen und Machbarkeitsstudien, die strategische Beschaffung oder die detaillierte Planung Ihrer Klinik – wir unterstützen Sie kompetent und zuverlässig in jeder Projektphase.</div>
    </div>
    <div class="m-svc2-grid">
      <a class="m-svc2" href="leistungen.html">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 38 L38 38 L10 12 Z"/><path d="M10 27 L21 27"/><circle cx="38" cy="38" r="3.6" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">01</span>
        </div>
        <h3 class="m-svc2-title">Planung<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Von der Idee bis zur Umsetzung – wir realisieren Ihre Projekte in der Medizintechnik. Mit klaren Strukturen und effizienter Projektsteuerung gewährleisten wir Termintreue, Kostensicherheit und höchste Qualität.</p>
      </a>
      <a class="m-svc2" href="leistungen.html">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 13 h26 a3 3 0 0 1 3 3 v13 a3 3 0 0 1 -3 3 H21 l-7 6 v-6 h-2 a3 3 0 0 1 -3 -3 V16 a3 3 0 0 1 3 -3 Z"/><circle cx="23" cy="22.5" r="3.4" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">02</span>
        </div>
        <h3 class="m-svc2-title">Consulting<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Strategien mit Substanz – Beratung mit langjähriger Erfahrung in der Medizintechnik. Maßgeschneiderte Lösungen, die Abläufe optimieren, Kosten senken und nachhaltige Ergebnisse liefern.</p>
      </a>
      <a class="m-svc2" href="leistungen.html">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 8 L39 16 L39 32 L24 40 L9 32 L9 16 Z"/><path d="M9 16 L24 24 L39 16"/><path d="M24 24 L24 40"/><circle cx="24" cy="24" r="3.4" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">03</span>
        </div>
        <h3 class="m-svc2-title">Handel<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Qualität, die bleibt. Lösungen, die sich rechnen. Langlebige, wartungsarme Medizinprodukte und individuell angepasste Lösungen – mit persönlicher Beratung und vertrauensvoller, partnerschaftlicher Zusammenarbeit.</p>
      </a>
      <a class="m-svc2" href="leistungen.html">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="21" cy="21" r="11"/><path d="M29 29 L39 39"/><path d="M16.5 21.5 l3.5 3.5 l6.5 -7.5" class="sig-stroke" stroke-width="3.2"/></svg></span>
          <span class="m-svc2-num">04</span>
        </div>
        <h3 class="m-svc2-title">Prüfung<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Zuverlässiger Technikservice – maximale Sicherheit. Einwandfreie Geräte, rechtssichere Prüfungen, minimale Ausfälle.</p>
      </a>
    </div>
  </div>
</section>

<section class="m-section" id="tco">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Total Cost of Ownership</span>
      <h2 class="m-bigH">Der Anschaffungspreis ist nur der Anfang<span class="end-dot">.</span></h2>
      <div class="sub">Ein Medizingerät kostet weit mehr als seinen Kaufpreis. Der größte Teil der Kosten entsteht erst über den gesamten Lebenszyklus – im Betrieb, in der Wartung und im Personal. Wir kennen diese Gesamtkosten im Detail und planen so, dass Sie langfristig sparen.</div>
    </div>

    <div class="m-tco-grid">
      <figure class="m-tco-chart">
        <div class="m-tco-chart-title">Kosteneffizienz durch frühe Planung</div>
        <svg viewBox="0 0 720 400" role="img" aria-label="Diagramm: Projektkosten über 30 Jahre – mit früher Planung deutlich niedrigere Lebenszykluskosten." xmlns="http://www.w3.org/2000/svg">
          <!-- axes -->
          <line x1="64" y1="48" x2="64" y2="320" stroke="#D5DAE0" stroke-width="1.5"/>
          <line x1="64" y1="320" x2="612" y2="320" stroke="#D5DAE0" stroke-width="1.5"/>
          <!-- savings area between the curves -->
          <polygon points="64,320 163,268 262,198 361,138 460,84 560,58 560,141 411,157 262,179 163,200 64,320" fill="#004AAD" fill-opacity="0.08"/>
          <!-- ohne Planung (steil steigend) -->
          <path d="M64,320 C120,300 150,285 163,268 C210,238 235,222 262,198 C310,168 335,158 361,138 C408,110 432,98 460,84 C505,68 535,64 560,58" fill="none" stroke="#5B9BD5" stroke-width="3.4" stroke-linecap="round"/>
          <!-- mit Planung (flacher) -->
          <path d="M64,320 C108,252 138,214 163,200 C205,184 228,182 262,179 C330,173 350,162 411,157 C480,151 520,146 560,141" fill="none" stroke="#004AAD" stroke-width="3.4" stroke-linecap="round"/>
          <!-- end points -->
          <circle cx="560" cy="58" r="5.5" fill="#5B9BD5"/>
          <circle cx="560" cy="141" r="5.5" fill="#004AAD"/>
          <!-- end labels -->
          <text x="576" y="52" font-family="Hanken Grotesk, sans-serif" font-size="14" font-weight="700" fill="#5B9BD5">Kosten ohne</text>
          <text x="576" y="70" font-family="Hanken Grotesk, sans-serif" font-size="14" font-weight="700" fill="#5B9BD5">Planung</text>
          <text x="576" y="135" font-family="Hanken Grotesk, sans-serif" font-size="14" font-weight="700" fill="#004AAD">Kosten mit</text>
          <text x="576" y="153" font-family="Hanken Grotesk, sans-serif" font-size="14" font-weight="700" fill="#004AAD">Planung</text>
          <!-- x ticks -->
          <g font-family="IBM Plex Mono, monospace" font-size="12" fill="#6B7785" text-anchor="middle">
            <text x="64" y="340">0</text><text x="155" y="340">5</text><text x="246" y="340">10</text>
            <text x="336" y="340">15</text><text x="427" y="340">20</text><text x="518" y="340">25</text><text x="560" y="340">30</text>
          </g>
          <text x="628" y="324" font-family="IBM Plex Mono, monospace" font-size="12" fill="#6B7785">Jahre</text>
          <text x="20" y="184" font-family="IBM Plex Mono, monospace" font-size="11" letter-spacing="1.5" fill="#6B7785" transform="rotate(-90 20 184)" text-anchor="middle">PROJEKTKOSTEN</text>
          <!-- phase bar -->
          <rect x="64" y="352" width="99" height="22" rx="5" fill="#E8EEF7"/>
          <rect x="167" y="352" width="445" height="22" rx="5" fill="#F1F4F8"/>
          <text x="113" y="367" font-family="IBM Plex Mono, monospace" font-size="10.5" letter-spacing="1" fill="#004AAD" text-anchor="middle">PLANUNG</text>
          <text x="389" y="367" font-family="IBM Plex Mono, monospace" font-size="10.5" letter-spacing="1" fill="#6B7785" text-anchor="middle">BETRIEB</text>
        </svg>
        <figcaption>Früh planen. Geringere Lebenszykluskosten.</figcaption>
      </figure>

      <div class="m-tco-side">
        <div class="m-tco-split">
          <div class="m-tco-split-bar">
            <span class="seg-acq" style="width:20%"><em>20&thinsp;%</em>Anschaffung</span>
            <span class="seg-op" style="width:80%"><em>80&thinsp;%</em>Betrieb über den Lebenszyklus</span>
          </div>
          <p class="m-tco-split-cap">Der Anschaffungspreis macht typischerweise nur rund ein Fünftel der Gesamtkosten aus – der Großteil entsteht im laufenden Betrieb.</p>
        </div>

        <div class="m-tco-factors">
          <div class="m-tco-factors-cap">Was den wahren Gerätepreis ausmacht</div>
          <div class="m-tco-chips">
            <span class="m-tco-chip is-acq">Anschaffung</span>
            <span class="m-tco-chip">Transport</span>
            <span class="m-tco-chip">Installation</span>
            <span class="m-tco-chip">Inbetriebnahme</span>
            <span class="m-tco-chip">Betrieb &amp; Energie</span>
            <span class="m-tco-chip">Personal</span>
            <span class="m-tco-chip">Verbrauchsmaterial</span>
            <span class="m-tco-chip">Wartung</span>
            <span class="m-tco-chip">Schulung</span>
            <span class="m-tco-chip">Entsorgung</span>
          </div>
        </div>

        <p class="m-tco-principle">Früh planen · Gesamtkosten senken · Werterhalt langfristig sichern<span class="em">.</span></p>
      </div>
    </div>
  </div>
</section>

<section class="m-cta-banner" style="background-image:url(assets/cta-banner.jpg)">
  <div class="m-shell">
    <div class="m-cta-banner-copy">
      <div class="line"></div>
      <h2>Arbeiten Sie mit uns<span class="end-dot">.</span></h2>
      <a class="m-cta-link" href="kontakt.html">Kontakt aufnehmen</a>
    </div>
  </div>
</section>'''

BODY_LEISTUNGEN = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Leistungen</span>
    <h1>Unsere Leistungen<span class="end-dot">.</span></h1>
    <p class="lede">Mit unserer langjährigen Erfahrung in der Medizintechnik bieten wir ein umfassendes Leistungsspektrum, das exakt auf Ihre Anforderungen zugeschnitten ist. Von ersten Konzeptideen und fundierten Machbarkeitsstudien über die strategische Beschaffung bis zur detaillierten Planung Ihrer Klinik unterstützen wir Sie kompetent, zuverlässig und effizient in jeder Projektphase.</p>
  </div>
</section>

<section class="m-graphic-sec" style="background-image:url(assets/slogan-bg.jpg)">
  <div class="m-shell">
    <div class="m-cross">
      <span class="m-cross-line v"></span>
      <span class="m-cross-line h"></span>

      <a class="m-cx-node n-top" href="#planung">
        <span class="m-hg-ring"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 38 L38 38 L10 12 Z"/><path d="M10 27 L21 27"/><circle cx="38" cy="38" r="4.4" class="sig-fill"/></svg></span>
        <span class="m-cx-label">Planung</span>
      </a>

      <a class="m-cx-node n-right" href="#consulting">
        <span class="m-hg-ring"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 13 h26 a3 3 0 0 1 3 3 v13 a3 3 0 0 1 -3 3 H21 l-7 6 v-6 h-2 a3 3 0 0 1 -3 -3 V16 a3 3 0 0 1 3 -3 Z"/><circle cx="23" cy="22.5" r="4.2" class="sig-fill"/></svg></span>
        <span class="m-cx-label">Consulting</span>
      </a>

      <a class="m-cx-node n-bottom" href="#handel">
        <span class="m-hg-ring"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 8 L39 16 L39 32 L24 40 L9 32 L9 16 Z"/><path d="M9 16 L24 24 L39 16"/><path d="M24 24 L24 40"/><circle cx="24" cy="24" r="4.2" class="sig-fill"/></svg></span>
        <span class="m-cx-label">Handel</span>
      </a>

      <a class="m-cx-node n-left" href="#pruefung">
        <span class="m-hg-ring"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="21" cy="21" r="11"/><path d="M29 29 L39 39"/><path d="M16.5 21.5 l3.5 3.5 l6.5 -7.5" class="sig-stroke" stroke-width="3.2"/></svg></span>
        <span class="m-cx-label">Prüfung</span>
      </a>

      <div class="m-cross-center"><img src="assets/m-logo.png" alt="medeqon" width="372" height="335"></div>
    </div>
  </div>
</section>

<section class="m-section alt">
  <div class="m-shell">
    <div class="m-svc2-grid">
      <article class="m-svc2" id="planung">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 38 L38 38 L10 12 Z"/><path d="M10 27 L21 27"/><circle cx="38" cy="38" r="3.6" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">01</span>
        </div>
        <h2 class="m-svc2-title">Planung &amp; Bauüberwachung<span class="end-dot">.</span></h2>
        <p class="m-svc2-lead">Von der Idee bis zur Umsetzung – wir realisieren Ihre Projekte.</p>
        <p class="m-svc2-desc">Im Projektgeschäft begleiten wir Sie von Anfang an auf Augenhöhe. Durch klare Strukturen und effizient gesteuerte Arbeitsabläufe sparen Sie sich Zeit und Ressourcen. Unsere präzise Projektsteuerung und hohen Qualitätsansprüche sorgen für Termintreue, Kostensicherheit und erstklassige Ergebnisse.</p>
        <ul class="m-svc2-list">
          <li>Abwicklung über LPH 1–9</li>
          <li>Planung in 3D</li>
          <li>Aktive Kostensteuerung</li>
          <li>Übersichtliche Raumbücher</li>
          <li>Projektsteuerung</li>
        </ul>
      </article>
      <article class="m-svc2" id="consulting">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 13 h26 a3 3 0 0 1 3 3 v13 a3 3 0 0 1 -3 3 H21 l-7 6 v-6 h-2 a3 3 0 0 1 -3 -3 V16 a3 3 0 0 1 3 -3 Z"/><circle cx="23" cy="22.5" r="3.4" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">02</span>
        </div>
        <h2 class="m-svc2-title">Consulting<span class="end-dot">.</span></h2>
        <p class="m-svc2-lead">Strategien mit Substanz – Beratung mit Erfahrung in der Medizintechnik.</p>
        <p class="m-svc2-desc">Wir entwickeln maßgeschneiderte Lösungen, die technisch, organisatorisch und wirtschaftlich passen. Unsere langjährige Erfahrung in der Medizintechnikberatung verbindet Fachwissen mit praxisnaher Umsetzung, optimiert Abläufe, senkt Kosten und schafft nachhaltige Ergebnisse – heute und morgen.</p>
        <ul class="m-svc2-list">
          <li>Bedarfsanalyse</li>
          <li>Zieldefinition</li>
          <li>Technische und wirtschaftliche Bewertung</li>
          <li>Strategische Konzeptentwicklung</li>
          <li>Umsetzungsbegleitung</li>
          <li>Schulung und Wissenstransfer</li>
        </ul>
      </article>
    </div>

    <div class="m-cta-mid">
      <div class="m-shell m-cta-inner">
        <div class="line"></div>
        <h2>Arbeiten Sie mit uns<span class="end-dot">.</span></h2>
        <p>Vertrauen Sie auf passgenaue Lösungen, kompetente Beratung und persönliche Betreuung – für erfolgreiche Projekte und dauerhafte Resultate.</p>
        <a class="m-cta-link" href="kontakt.html">Kontakt aufnehmen</a>
      </div>
    </div>

    <div class="m-svc2-grid">
      <article class="m-svc2" id="handel">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 8 L39 16 L39 32 L24 40 L9 32 L9 16 Z"/><path d="M9 16 L24 24 L39 16"/><path d="M24 24 L24 40"/><circle cx="24" cy="24" r="3.4" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">03</span>
        </div>
        <h2 class="m-svc2-title">Handel<span class="end-dot">.</span></h2>
        <p class="m-svc2-lead">Qualität, die bleibt. Lösungen, die sich rechnen.</p>
        <p class="m-svc2-desc">Wir bieten langlebige, wartungsarme Medizinprodukte mit niedrigen Lebenszykluskosten. Individuelle Lösungen werden exakt auf Ihren Bedarf abgestimmt – inklusive persönlicher Beratung und partnerschaftlicher Zusammenarbeit.</p>
        <ul class="m-svc2-list">
          <li>Produktsourcing</li>
          <li>Auswahlberatung</li>
          <li>Qualitätssicherung</li>
          <li>Beschaffung und Einbringung</li>
          <li>Wirtschaftlichkeitsanalyse</li>
          <li>After-Sales-Service</li>
          <li>Technische Unterstützung</li>
        </ul>
      </article>
      <article class="m-svc2" id="pruefung">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="21" cy="21" r="11"/><path d="M29 29 L39 39"/><path d="M16.5 21.5 l3.5 3.5 l6.5 -7.5" class="sig-stroke" stroke-width="2.6"/></svg></span>
          <span class="m-svc2-num">04</span>
        </div>
        <h2 class="m-svc2-title">Prüfung, Reparatur und Sicherheit<span class="end-dot">.</span></h2>
        <p class="m-svc2-lead">Zuverlässiger Technikservice für maximale Sicherheit.</p>
        <p class="m-svc2-desc">Unsere Mechatroniker*innen gewährleisten einwandfreie Medizintechnik-Geräte, rechtssichere Prüfungen und frühzeitige Empfehlungen – für minimale Ausfälle und maximale Sicherheit. So bleibt Ihre Medizintechnik jederzeit einsatzbereit und erfüllt höchste Qualitäts- und Sicherheitsstandards.</p>
        <ul class="m-svc2-list">
          <li>Wiederholungsprüfungen</li>
          <li>Prüfung und Instandsetzung nach EN 6253</li>
          <li>Sichtprüfung und Kontrolle der Funktionsfähigkeit</li>
          <li>Reparatur- und Ersatzempfehlungen</li>
          <li>Unterstützung bei der Übertragung ins Bestandsverzeichnis</li>
          <li>Nachvollziehbare Dokumentation</li>
        </ul>
      </article>
    </div>
  </div>
</section>'''

CHEV = '<svg class="m-ac-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'

# ---- Produktkarten (Medizinische Einrichtung) aus products.json generieren ----
import json, html as _html, glob as _glob
_products = json.loads((ROOT / "products.json").read_text(encoding="utf-8"))
def _gallery(p):
    imgs = sorted(_glob.glob(str(ROOT / "assets" / "produkte" / p["slug"] / "*.jpg")))
    n = len(imgs) or 1
    model = _html.escape(p["model"])
    shots = []
    for i in range(1, n + 1):
        cls = "m-pl-shot is-on" if i == 1 else "m-pl-shot"
        alt = model if i == 1 else f"{model} – Ansicht {i}"
        shots.append(
            f'                        <img class="{cls}" src="assets/produkte/{p["slug"]}/{i}.jpg" alt="{alt}" loading="lazy" draggable="false">')
    dots = ""
    if n > 1:
        d = "".join(('<i class="on"></i>' if i == 0 else '<i></i>') for i in range(n))
        dots = f'\n                        <div class="m-pl-dots">{d}</div>'
    tall = " m-pl-frame--tall" if p.get("fit") == "tall" else ""
    return (
'                    <div class="m-pl-gallery">\n'
f'                      <div class="m-pl-frame{tall}" data-count="{n}">\n'
+ "\n".join(shots) + dots + '\n'
'                      </div>\n'
'                    </div>')
def _render_liege(p):
    specs = "\n".join(
        f'                        <li><span>{_html.escape(k)}</span>{_html.escape(v)}</li>'
        for k, v in p["specs"])
    return (
'                  <article class="m-pl">\n'
+ _gallery(p) + '\n'
'                    <div class="m-pl-info">\n'
f'                      <span class="m-pl-ref">Ref. {_html.escape(p["ref"])}</span>\n'
f'                      <h4 class="m-pl-name">{_html.escape(p["model"])}</h4>\n'
f'                      <p class="m-pl-desc">{_html.escape(p["description"])}</p>\n'
'                      <ul class="m-pl-specs">\n'
f'{specs}\n'
'                      </ul>\n'
'                    </div>\n'
'                  </article>')
def _cards(cat):
    return "\n\n".join(_render_liege(p) for p in _products if p["cat"] == cat)
def _count(cat):
    return sum(1 for p in _products if p["cat"] == cat)
CARDS = {c: _cards(c) for c in ("chiro", "elektrisch", "hydraulisch", "fix", "stuehle", "sichtschutz")}

# ---- Heilbehelfe & Hilfsmittel ----
_hb = json.loads((ROOT / "heilbehelfe.json").read_text(encoding="utf-8"))
def _hb_cards(sub, group=None):
    return "\n\n".join(_render_liege(p) for p in _hb
                       if p["sub"] == sub and (group is None or p.get("group") == group))
def _hb_count(sub):
    return sum(1 for p in _hb if p["sub"] == sub)

# ---- Strahlenschutz (ROTHBAND) ----
_ss = json.loads((ROOT / "strahlenschutz.json").read_text(encoding="utf-8"))
def _ss_cards(sub):
    return "\n\n".join(_render_liege(p) for p in _ss if p["sub"] == sub)
def _ss_count(sub):
    return sum(1 for p in _ss if p["sub"] == sub)

# ---- Personalisierung & Optionen (ROTHBAND) ----
_OPTIONEN = [
    ("Personalisierung", [
        ("stickerei", "Stickerei", "Individuelle Textstickerei direkt auf der Schürze – z. B. Name, Abteilung oder Einsatzbereich."),
        ("tasche", "Aufgesetzte Tasche", "Praktische Außentasche für Dosimeter, Stift oder Kleinteile."),
        ("taschen-stickerei", "Taschen-Stickerei", "Bestickung direkt auf der Tasche – etwa mit Abteilungs- oder Klinikname."),
        ("namensschild", "Austauschbares Namensschild", "Per Klett wechselbares Namensschild – jederzeit flexibel anpassbar."),
        ("ausweistasche", "Transparente Ausweistasche", "Klarsichttasche für Dienstausweis oder Dosimeter-Karte."),
    ]),
    ("Optionale Extras", [
        ("innentasche", "Innentasche", "Verdeckte Innentasche für persönliche Kleinteile."),
        ("outlast", "Outlast®-Klimatechnologie", "Temperaturregulierendes Innenfutter für spürbar angenehmeres Tragen."),
        ("rocktasche", "Rock-Tasche", "Zusätzliche Tasche am Rockteil des Zweiteilers."),
        ("innengurt", "Innengurt", "Integrierter Stützgurt entlastet den Rücken und verbessert den Sitz."),
    ]),
]
def _optionen_html():
    out = []
    for group, items in _OPTIONEN:
        tiles = []
        for key, title, desc in items:
            tiles.append(
'                    <figure class="m-opt">\n'
f'                      <div class="m-opt-img"><img src="assets/optionen/{key}.jpg" alt="{_html.escape(title)}" loading="lazy"></div>\n'
'                      <figcaption class="m-opt-body">\n'
f'                        <h4 class="m-opt-title">{_html.escape(title)}</h4>\n'
f'                        <p class="m-opt-desc">{_html.escape(desc)}</p>\n'
'                      </figcaption>\n'
'                    </figure>')
        out.append(
'                <div class="m-opt-group">\n'
f'                  <div class="m-opt-grouptitle">{_html.escape(group)}</div>\n'
'                  <div class="m-opt-grid">\n'
+ "\n".join(tiles) + '\n'
'                  </div>\n'
'                </div>')
    return "\n".join(out)

# ---- Farboptionen (ROTHBAND) ----
_FARBEN = [
    ("Unifarben", [
        ("royalblue","Royalblau"), ("marineblue","Marineblau"), ("orange","Orange"),
        ("rose","Rosé"), ("burgundy","Bordeaux"), ("berry","Beere"), ("red","Rot"),
        ("violet","Violett"), ("grey","Grau"), ("lightgreen","Hellgrün"),
        ("forestgreen","Waldgrün"), ("khaki","Khaki"), ("black","Schwarz"), ("yellow","Gelb"),
    ]),
    ("Muster", [
        ("zebra","Zebra"), ("tartan","Karo"), ("stars","Sterne"), ("safari","Safari"),
        ("swirls","Wirbel"), ("flower-pink","Blüten Pink"), ("flower-violet","Blüten Violett"),
        ("firework","Feuerwerk"), ("flames","Flammen"), ("nursery","Kindermotiv"),
        ("paintsplash","Farbkleckse"), ("camo-pink","Camouflage Pink"),
        ("camo-grey","Camouflage Grau"), ("camo-blue","Camouflage Blau"),
    ]),
    ("Einfassung", [
        ("bind-black","Schwarz"), ("bind-red","Rot"), ("bind-blue","Blau"), ("bind-green","Grün"),
        ("bind-darkpink","Dunkelpink"), ("bind-neonpink","Neonpink"),
        ("bind-teal","Petrol"), ("bind-orange","Orange"),
    ]),
]
def _farben_html():
    out = []
    for group, items in _FARBEN:
        tiles = []
        for key, name in items:
            tiles.append(
'                    <figure class="m-sw">\n'
f'                      <div class="m-sw-img"><img src="assets/farben/{key}.jpg" alt="{_html.escape(name)}" loading="lazy"></div>\n'
f'                      <figcaption class="m-sw-name">{_html.escape(name)}</figcaption>\n'
'                    </figure>')
        out.append(
'                <div class="m-opt-group">\n'
f'                  <div class="m-opt-grouptitle">{_html.escape(group)}</div>\n'
'                  <div class="m-sw-grid">\n'
+ "\n".join(tiles) + '\n'
'                  </div>\n'
'                </div>')
    return "\n".join(out)

# ---- Montierter Strahlenschutz (KENEX) ----
_kenex = json.loads((ROOT / "kenex.json").read_text(encoding="utf-8"))
def _kenex_cards(cat, sub=None):
    return "\n\n".join(_render_liege(p) for p in _kenex
                       if p["cat"] == cat and (sub is None or p.get("sub") == sub))
def _kenex_count(cat, sub=None):
    return sum(1 for p in _kenex if p["cat"] == cat and (sub is None or p.get("sub") == sub))

# ---- Download-Bereiche (Kataloge, Datenblätter, Zertifikate) ----
_DL_ICONS = {
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15.5H6.5A2.5 2.5 0 0 0 4 21z"/><path d="M4 18.5A2.5 2.5 0 0 1 6.5 16H20"/><path d="M8 7.5h7"/></svg>',
    "doc":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M8.5 13h7"/><path d="M8.5 16.5h7"/></svg>',
    "cert": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="9.5" r="5.5"/><path d="M9.3 13.8 8 21l4-2 4 2-1.3-7.2"/><path d="M9.6 9.3l1.6 1.6 3-3.2"/></svg>',
}
_DL_DOWNLOAD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M5 20h14"/></svg>'

def _dl_card(item):
    icon = _DL_ICONS.get(item.get("icon", "doc"), _DL_ICONS["doc"])
    title = _html.escape(item["title"])
    meta = _html.escape(item.get("meta", "PDF-Dokument"))
    f = item.get("file")
    if f:
        action = f'<a class="m-dl-btn" href="{f}" download aria-label="{title} herunterladen">{_DL_DOWNLOAD}</a>'
        soon = ""
    else:
        action = '<span class="m-dl-flag">In Kürze</span>'
        soon = " is-soon"
    return (
'                    <figure class="m-dl-card' + soon + '">\n'
f'                      <span class="m-dl-ic">{icon}</span>\n'
'                      <span class="m-dl-main">\n'
f'                        <span class="m-dl-title">{title}</span>\n'
f'                        <span class="m-dl-meta">{meta}</span>\n'
'                      </span>\n'
f'                      {action}\n'
'                    </figure>')

def _downloads_category(num, cid, lead, groups):
    parts = [
'      <details class="m-ac" id="' + cid + '">\n'
'        <summary><span class="m-ac-num">' + num + '</span><span class="m-ac-title">Downloads &amp; Unterlagen</span>' + CHEV + '</summary>\n'
'        <div class="m-ac-body">\n'
'          <p class="m-ac-lead">' + lead + '</p>\n'
'          <div class="m-dl-wrap">']
    for group, items in groups:
        parts.append(
'            <div class="m-dl-group">\n'
f'              <div class="m-dl-grouptitle">{_html.escape(group)}</div>\n'
'              <div class="m-dl-grid">\n'
+ "\n".join(_dl_card(it) for it in items) + '\n'
'              </div>\n'
'            </div>')
    parts.append(
'          </div>\n'
'        </div>\n'
'      </details>')
    return "\n".join(parts)

_DL_LEAD = ("Hier stellen wir Ihnen Unterlagen zum Herunterladen bereit &ndash; "
            "Herstellerkataloge, technische Datenblätter, Produktinformationen sowie "
            "CE- und Konformitätszertifikate. Neue Dokumente ergänzen wir laufend.")

DL_STRAHLENSCHUTZ = [
    ("Herstellerkataloge", [
        {"title": "ROTHBAND – Produktkatalog", "meta": "Gesamtkatalog Strahlenschutz · PDF", "icon": "book"},
        {"title": "KENEX – Produktkatalog", "meta": "Röntgenschutz­systeme · PDF", "icon": "book"},
    ]),
    ("Datenblätter & Produktinfos", [
        {"title": "Datenblätter – Persönlicher Strahlenschutz", "meta": "Technische Daten · PDF"},
        {"title": "Datenblätter – Tisch-, Decken- & Mobilschutz (KENEX)", "meta": "Technische Daten · PDF"},
    ]),
    ("Zertifikate & Konformität", [
        {"title": "CE-Konformitätserklärung – ROTHBAND", "meta": "Zertifikat · PDF", "icon": "cert"},
        {"title": "CE-Konformitätserklärung – KENEX", "meta": "Zertifikat · PDF", "icon": "cert"},
    ]),
]

DL_MED = [
    ("Herstellerkataloge", [
        {"title": "COINFYCARE – Produktkatalog", "meta": "Medizinische Einrichtung · PDF", "icon": "book"},
    ]),
    ("Datenblätter & Produktinfos", [
        {"title": "Datenblätter – Untersuchungsliegen", "meta": "Technische Daten · PDF"},
        {"title": "Datenblätter – Medizinische Stühle", "meta": "Technische Daten · PDF"},
        {"title": "Datenblätter – Sichtschutz", "meta": "Technische Daten · PDF"},
    ]),
    ("Zertifikate & Konformität", [
        {"title": "CE-Konformitätserklärung – COINFYCARE", "meta": "Zertifikat · PDF", "icon": "cert"},
    ]),
]

DL_HB = [
    ("Herstellerkataloge", [
        {"title": "MOBIAK – Produktkatalog", "meta": "Heilbehelfe & Hilfsmittel · PDF", "icon": "book"},
    ]),
    ("Datenblätter & Produktinfos", [
        {"title": "Datenblätter – Rollstühle & Mobilität", "meta": "Technische Daten · PDF"},
        {"title": "Datenblätter – Anti-Dekubitus-Produkte", "meta": "Technische Daten · PDF"},
        {"title": "Datenblätter – Sauerstoffkonzentratoren", "meta": "Technische Daten · PDF"},
    ]),
    ("Zertifikate & Konformität", [
        {"title": "CE-Konformitätserklärung – MOBIAK", "meta": "Zertifikat · PDF", "icon": "cert"},
    ]),
]

BODY_PRODUKTE = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Produkte</span>
    <h1>Unsere Produkte<span class="end-dot">.</span></h1>
    <p class="lede">Wir vermitteln und liefern zertifizierte Medizinprodukte in mehreren Kategorien: Strahlenschutz, Medizinische Einrichtung und Heilbehelfe &amp; Hilfsmittel. Darüber hinaus beschaffen wir als herstellerunabhängiger Partner nahezu jedes Produkt und statten ganze Bereiche projektbasiert aus. Klicken Sie eine Kategorie an, um die einzelnen Bereiche zu entdecken.</p>
  </div>
</section>

<section class="m-section m-hexbg m-hexbg-l" id="strahlenschutz" style="--hexbg:url('assets/brands/ss-hero.jpg');--hexbg2:url('assets/brands/kenex-hero.jpg')">
  <div class="m-shell">
    <div class="m-cat-head has-mfr">
      <div class="m-cat-head-text">
        <h2>Strahlenschutz<span class="end-dot">.</span></h2>
        <div class="sub">Persönliche Strahlenschutz-Bekleidung „Made in UK" vom Hersteller ROTHBAND – ergänzt um passende Aufbewahrung sowie mobile, deckenmontierte und tischmontierte Röntgenschutzsysteme von KENEX. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.</div>
      </div>
      <div class="m-mfr">
        <span class="m-mfr-cap">Hersteller</span>
        <div class="m-mfr-chips">
          <a class="m-mfr-chip m-mfr-chip--rothband" href="https://www.rothband.com/de" target="_blank" rel="noopener" aria-label="Hersteller ROTHBAND – Website in neuem Tab öffnen"><img src="assets/brands/rothband.png" alt="ROTHBAND" loading="lazy"></a>
          <a class="m-mfr-chip m-mfr-chip--kenex" href="https://www.kenex.co.uk" target="_blank" rel="noopener" aria-label="Hersteller KENEX – Website in neuem Tab öffnen"><img src="assets/brands/kenex.png" alt="KENEX" loading="lazy"></a>
        </div>
      </div>
    </div>

    <div class="m-acc">
      <details class="m-ac" id="persoenlicher-strahlenschutz">
        <summary><span class="m-ac-num">01</span><span class="m-ac-title">Persönlicher Strahlenschutz</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <img class="m-ac-mfr m-ac-mfr--rothband" src="assets/brands/rothband.png" alt="ROTHBAND" loading="lazy">
          <p class="m-ac-lead">Strahlenschutzbekleidung für den direkten Personenschutz – Schürzen, Zweiteiler, Schilddrüsenschutz und ergänzendes Zubehör. Fokus auf Ergonomie, Gewichtsverteilung, Schutzleistung und Tragekomfort.</p>
          <div class="m-acc m-acc-nested">
            <details class="m-ac m-ac-sub" id="ss-front">
              <summary><span class="m-ac-title">Front-Schürzen</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_ss_count("front")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + _ss_cards("front") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="ss-tabard">
              <summary><span class="m-ac-title">Umhang-/Tabard-Schürzen</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_ss_count("tabard")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + _ss_cards("tabard") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="ss-wrap">
              <summary><span class="m-ac-title">Mantel-/Wickelschürzen</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_ss_count("wrap")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + _ss_cards("wrap") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="ss-zweiteiler">
              <summary><span class="m-ac-title">Zweiteiler – Oberteil &amp; Rock</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_ss_count("zweiteiler")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + _ss_cards("zweiteiler") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="ss-schild">
              <summary><span class="m-ac-title">Schilddrüsenschutz</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_ss_count("schild")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + _ss_cards("schild") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="ss-zubehoer">
              <summary><span class="m-ac-title">Zubehör</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_ss_count("zubehoer")) + ''' Produkte verfügbar</p>
                <div class="m-pl-list">
''' + _ss_cards("zubehoer") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="ss-brillen">
              <summary><span class="m-ac-title">Strahlenschutzbrillen</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-ac-lead">Röntgenschutzbrillen für den Schutz der Augen bei Durchleuchtung, interventioneller Bildgebung und Radiologie – in zahlreichen Rahmenformen, mit seitlichem Schutz und wahlweise mit Sehstärke. Bleigläser 0,75 mm Pb, Seitenschutz 0,50 mm Pb.</p>
                <p class="m-pl-count">''' + str(_ss_count("brillen")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + _ss_cards("brillen") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="ss-personalisierung">
              <summary><span class="m-ac-title">Personalisierung &amp; Optionen</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-ac-lead">Jede Schürze lässt sich individuell anpassen – für eine bessere Zuordnung, mehr Tragekomfort und praktische Details im Klinikalltag. Alle Optionen sind mit den Modellen aus „Persönlicher Strahlenschutz" kombinierbar.</p>
''' + _optionen_html() + '''
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="ss-farben">
              <summary><span class="m-ac-title">Farboptionen</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-ac-lead">Alle Schürzen und Zubehörteile sind in zahlreichen Farben, Mustern und Einfassungen erhältlich – für ein individuelles, gut erkennbares Erscheinungsbild. Das Stoffsortiment wird von ROTHBAND laufend erweitert.</p>
''' + _farben_html() + '''
              </div>
            </details>
          </div>
        </div>
      </details>

      <details class="m-ac" id="ss-aufbewahrung">
        <summary><span class="m-ac-num">02</span><span class="m-ac-title">Aufbewahrung</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <img class="m-ac-mfr m-ac-mfr--rothband" src="assets/brands/rothband.png" alt="ROTHBAND" loading="lazy">
          <p class="m-ac-lead">Ständer, Schwenkarme und Bügel zur sicheren, platzsparenden Aufbewahrung von Strahlenschutzschürzen.</p>
          <p class="m-pl-count">''' + str(_ss_count("aufbewahrung")) + ''' Produkte verfügbar</p>
          <div class="m-pl-list">
''' + _ss_cards("aufbewahrung") + '''
          </div>
        </div>
      </details>

      <details class="m-ac" id="mobiler-strahlenschutz">
        <summary><span class="m-ac-num">03</span><span class="m-ac-title">Mobiler Strahlenschutz</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <img class="m-ac-mfr m-ac-mfr--kenex" src="assets/brands/kenex.png" alt="KENEX" loading="lazy">
          <p class="m-ac-lead">Fahrbare, frei positionierbare Röntgenschutzsysteme für flexible Einsätze im OP und in der interventionellen Radiologie – vom Hersteller KENEX.</p>
          <p class="m-pl-count">''' + str(_kenex_count("mobil")) + ''' Modelle verfügbar</p>
          <div class="m-pl-list">
''' + _kenex_cards("mobil") + '''
          </div>
        </div>
      </details>

      <details class="m-ac" id="deckenmontierter-strahlenschutz">
        <summary><span class="m-ac-num">04</span><span class="m-ac-title">Deckenmontierter Strahlenschutz</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <img class="m-ac-mfr m-ac-mfr--kenex" src="assets/brands/kenex.png" alt="KENEX" loading="lazy">
          <p class="m-ac-lead">Aufgehängte Überkopf-Schutzschilde und komplette Aufhängungssysteme (Deckenschienen, Säulen, Arme, Monitor-Aufhängung) – zur deutlichen Reduktion der Streustrahlung im Arbeitsbereich. Vom Hersteller KENEX.</p>
          <div class="m-acc m-acc-nested">

            <details class="m-ac m-ac-sub" id="decken-ueberkopf">
              <summary><span class="m-ac-title">Überkopf-Schutzschilde</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_kenex_count("decken","ueberkopf")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + _kenex_cards("decken","ueberkopf") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="decken-aufhaengung">
              <summary><span class="m-ac-title">Aufhängungssysteme</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_kenex_count("decken","aufhaengung")) + ''' Produkte verfügbar</p>
                <div class="m-pl-list">
''' + _kenex_cards("decken","aufhaengung") + '''
                </div>
              </div>
            </details>

          </div>
        </div>
      </details>

      <details class="m-ac" id="tischmontierter-strahlenschutz">
        <summary><span class="m-ac-num">05</span><span class="m-ac-title">Tischmontierter Strahlenschutz</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <img class="m-ac-mfr m-ac-mfr--kenex" src="assets/brands/kenex.png" alt="KENEX" loading="lazy">
          <p class="m-ac-lead">Am Untersuchungstisch montierte Schutzschilde für die interventionelle Radiologie – Unterkörper-, Kopfende- und Aufsatz-Schilde sowie passende Aufbewahrung. Vom Hersteller KENEX.</p>
          <div class="m-acc m-acc-nested">

            <details class="m-ac m-ac-sub" id="tisch-unterkoerper">
              <summary><span class="m-ac-title">Unterkörper-Tischschilde</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_kenex_count("tisch","unterkoerper")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + _kenex_cards("tisch","unterkoerper") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="tisch-kopfende">
              <summary><span class="m-ac-title">Kopfende-Tischschilde</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_kenex_count("tisch","kopfende")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + _kenex_cards("tisch","kopfende") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="tisch-top">
              <summary><span class="m-ac-title">Aufsatz- &amp; Fußende-Schilde</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_kenex_count("tisch","top")) + ''' Produkte verfügbar</p>
                <div class="m-pl-list">
''' + _kenex_cards("tisch","top") + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="tisch-aufbewahrung">
              <summary><span class="m-ac-title">Aufbewahrung &amp; Zubehör</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_kenex_count("tisch","aufbewahrung")) + ''' Produkte verfügbar</p>
                <div class="m-pl-list">
''' + _kenex_cards("tisch","aufbewahrung") + '''
                </div>
              </div>
            </details>

          </div>
        </div>
      </details>
''' + _downloads_category("06", "downloads-strahlenschutz", _DL_LEAD, DL_STRAHLENSCHUTZ) + '''
    </div>
  </div>
</section>

<section class="m-section alt m-hexbg m-hexbg--photo" id="medizinische-einrichtung" style="--hexbg:url('assets/brands/med-hero.jpg')">
  <div class="m-shell">
    <div class="m-cat-head has-mfr">
      <div class="m-cat-head-text">
        <h2>Medizinische Einrichtung<span class="end-dot">.</span></h2>
        <div class="sub">Ausstattung und Einrichtung für klinische Bereiche – vom Untersuchungsplatz bis zum Sichtschutz. Geliefert vom Hersteller COINFYCARE. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.</div>
      </div>
      <a class="m-mfr m-mfr--coinfy" href="https://www.coinfycare.com/en" target="_blank" rel="noopener" aria-label="Hersteller COINFYCARE – Website in neuem Tab öffnen">
        <span class="m-mfr-cap">Hersteller</span>
        <span class="m-mfr-chip"><img src="assets/brands/coinfycare.png" alt="COINFYCARE" loading="lazy"></span>
      </a>
    </div>

    <div class="m-acc">
      <details class="m-ac" id="untersuchungsliegen">
        <summary><span class="m-ac-num">01</span><span class="m-ac-title">Untersuchungsliegen</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-ac-lead">Untersuchungs- und Behandlungsliegen für Praxis und Klinik – nach Bauart gegliedert.</p>
          <div class="m-acc m-acc-nested">

            <details class="m-ac m-ac-sub" id="liegen-fix">
              <summary><span class="m-ac-title">Fix</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_count("fix")) + ''' Modell verfügbar</p>
                <div class="m-pl-list">
''' + CARDS["fix"] + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="liegen-hydraulisch">
              <summary><span class="m-ac-title">Hydraulisch</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_count("hydraulisch")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + CARDS["hydraulisch"] + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="liegen-elektrisch">
              <summary><span class="m-ac-title">Elektrisch</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_count("elektrisch")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + CARDS["elektrisch"] + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="liegen-chiropraktisch">
              <summary><span class="m-ac-title">Chiropraktische Liegen</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(_count("chiro")) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + CARDS["chiro"] + '''
                </div>
              </div>
            </details>

          </div>
        </div>
      </details>

      <details class="m-ac" id="medizinische-stuehle">
        <summary><span class="m-ac-num">02</span><span class="m-ac-title">Medizinische Stühle</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-ac-lead">Behandlungs-, Blutabnahme- und Arbeitsstühle sowie Hocker für den medizinischen Einsatz.</p>
          <p class="m-pl-count">''' + str(_count("stuehle")) + ''' Modelle verfügbar</p>
          <div class="m-pl-list">
''' + CARDS["stuehle"] + '''
          </div>
        </div>
      </details>

      <details class="m-ac" id="sichtschutz">
        <summary><span class="m-ac-num">03</span><span class="m-ac-title">Sichtschutz</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-ac-lead">Sicht- und Trennwandsysteme für diskrete, flexibel teilbare Raumbereiche.</p>
          <div class="m-pl-list">
''' + CARDS["sichtschutz"] + '''
          </div>
        </div>
      </details>
''' + _downloads_category("04", "downloads-medizinische-einrichtung", _DL_LEAD, DL_MED) + '''
    </div>
  </div>
</section>

<section class="m-section m-hexbg m-hexbg--photo" id="heilbehelfe" style="--hexbg:url('assets/brands/hb-hero.jpg')">
  <div class="m-shell">
    <div class="m-cat-head has-mfr">
      <div class="m-cat-head-text">
        <h2>Heilbehelfe &amp; Hilfsmittel<span class="end-dot">.</span></h2>
        <div class="sub">Mobilität, Pflege und Alltagshilfen – von Rollstühlen und Elektromobilen über Gehhilfen bis zu Anti-Dekubitus-Systemen und Sauerstoffversorgung. Geliefert vom Hersteller MOBIAK. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.</div>
      </div>
      <a class="m-mfr m-mfr--mobiak" href="https://www.mobiak.com/en/" target="_blank" rel="noopener" aria-label="Hersteller MOBIAK – Website in neuem Tab öffnen">
        <span class="m-mfr-cap">Hersteller</span>
        <span class="m-mfr-chip"><img src="assets/brands/mobiak.png" alt="MOBIAK"></span>
      </a>
    </div>

    <div class="m-acc">
      <details class="m-ac" id="hb-rollstuehle">
        <summary><span class="m-ac-num">01</span><span class="m-ac-title">Rollstühle</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-pl-count">''' + str(_hb_count("rollstuehle")) + ''' Modelle verfügbar</p>
          <div class="m-pl-list">
''' + _hb_cards("rollstuehle") + '''
          </div>
        </div>
      </details>

      <details class="m-ac" id="hb-erollstuehle">
        <summary><span class="m-ac-num">02</span><span class="m-ac-title">Elektrische Rollstühle &amp; Scooter</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-pl-count">''' + str(_hb_count("erollstuehle")) + ''' Modelle verfügbar</p>
          <div class="m-pl-list">
''' + _hb_cards("erollstuehle") + '''
          </div>
        </div>
      </details>

      <details class="m-ac" id="hb-gehhilfen">
        <summary><span class="m-ac-num">03</span><span class="m-ac-title">Gehhilfen</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <div class="m-pl-group">
            <h5 class="m-pl-grouphead">Rollatoren</h5>
            <div class="m-pl-list">
''' + _hb_cards("gehhilfen", "rollatoren") + '''
            </div>
          </div>
          <div class="m-pl-group">
            <h5 class="m-pl-grouphead">Gehböcke / Walker</h5>
            <div class="m-pl-list">
''' + _hb_cards("gehhilfen", "walker") + '''
            </div>
          </div>
        </div>
      </details>

      <details class="m-ac" id="hb-antidekubitus">
        <summary><span class="m-ac-num">04</span><span class="m-ac-title">Anti-Dekubitus-Produkte</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-pl-count">''' + str(_hb_count("antidekubitus")) + ''' Modelle verfügbar</p>
          <div class="m-pl-list">
''' + _hb_cards("antidekubitus") + '''
          </div>
        </div>
      </details>

      <details class="m-ac" id="hb-oxygen">
        <summary><span class="m-ac-num">05</span><span class="m-ac-title">Sauerstoffkonzentratoren</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <div class="m-pl-list">
''' + _hb_cards("oxygen") + '''
          </div>
        </div>
      </details>
''' + _downloads_category("06", "downloads-heilbehelfe", _DL_LEAD, DL_HB) + '''
    </div>
  </div>
</section>

<section class="m-section alt m-hexbg m-hexbg--photo" id="beschaffung" style="--hexbg:url('assets/brands/sourcing-hero.jpg')">
  <div class="m-shell">
    <div class="m-cat-head">
      <div class="m-cat-head-text">
        <h2>Beschaffung &amp; Projektausstattung<span class="end-dot">.</span></h2>
        <div class="sub">Nicht jedes Objekt steht in einem Katalog – doch nahezu jedes lässt sich beschaffen. Als herstellerunabhängiger Partner sourcen wir für Sie jedes medizinische, technische oder infrastrukturelle Produkt: einzeln und kurzfristig oder als Teil eines umfassenden Projekts. Vom einzelnen Spezialgerät bis zur kompletten Ausstattung eines Funktionsbereichs übernehmen wir Recherche, Auswahl, Einkauf und Lieferung – und richten auf Wunsch ganze Bereiche schlüsselfertig ein.</div>
      </div>
    </div>

    <div class="m-svc2-grid">
      <div class="m-svc2">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="24" cy="24" r="15"/><path d="M9 24 h30"/><path d="M24 9 a19 19 0 0 1 0 30 a19 19 0 0 1 0 -30"/><circle cx="24" cy="24" r="3.8" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">01</span>
        </div>
        <h3 class="m-svc2-title">Alles beschaffbar<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Ob Standardartikel, Spezialgerät oder schwer erhältliches Ersatzteil – wir identifizieren die passende Bezugsquelle und liefern zuverlässig. Kein Sortiment setzt uns Grenzen: Sie nennen den Bedarf, wir finden die Lösung.</p>
      </div>
      <div class="m-svc2">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="11" width="30" height="27" rx="2.5"/><path d="M24 11 v27"/><path d="M9 25 h30"/><circle cx="16.5" cy="18" r="3.6" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">02</span>
        </div>
        <h3 class="m-svc2-title">Komplette Bereichsausstattung<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Von der Praxis bis zur Klinikabteilung statten wir ganze Bereiche aus – abgestimmt auf Arbeitsabläufe, Hygieneanforderungen und Budget. Grundausstattung, Mobiliar und High-End-Technik aus einer Hand.</p>
      </div>
      <div class="m-svc2">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="13" r="3"/><circle cx="37" cy="13" r="3"/><circle cx="11" cy="35" r="3"/><circle cx="37" cy="35" r="3"/><path d="M20.4 20.6 L13.2 15.2 M27.6 20.6 L34.8 15.2 M20.4 27.4 L13.2 32.8 M27.6 27.4 L34.8 32.8"/><circle cx="24" cy="24" r="4.6" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">03</span>
        </div>
        <h3 class="m-svc2-title">Herstellerunabhängig<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Wir sind an keine Marke gebunden. So wählen wir stets das Produkt, das technisch, wirtschaftlich und qualitativ am besten zu Ihrer Anforderung passt – objektiv und in Ihrem Interesse.</p>
      </div>
      <div class="m-svc2">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 8 L39 16 L39 32 L24 40 L9 32 L9 16 Z"/><path d="M9 16 L24 24 L39 16"/><path d="M24 24 L24 40"/><circle cx="24" cy="24" r="3.8" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">04</span>
        </div>
        <h3 class="m-svc2-title">Projekt- &amp; Komplettservice<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Ein Ansprechpartner für den gesamten Beschaffungsprozess: Bedarfsanalyse, Angebot, Einkauf, Logistik und Lieferung – auf Wunsch inklusive Installation und Einschulung. Termintreu, transparent und aus einer Hand.</p>
      </div>
    </div>

    <div class="m-src-cta">
      <p>Sie haben einen konkreten Bedarf oder planen ein Projekt? Beschreiben Sie uns Ihr Vorhaben – wir erstellen Ihnen ein individuelles, unverbindliches Angebot.</p>
      <a class="m-btn" href="kontakt.html">Projekt anfragen</a>
    </div>
  </div>
</section>'''

BODY_MANAGEMENT = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Management</span>
    <h1>Medizintechnik mit Verantwortung, Qualität und Zukunft<span class="end-dot">.</span></h1>
    <p class="lede">Unsere Geschäftsführung verfügt über mehr als 15 Jahre Erfahrung in der Medizintechnik, die unser Unternehmen prägt. Qualität, Zuverlässigkeit und ständige Erreichbarkeit stehen für uns an erster Stelle. Wir setzen auf partnerschaftliche Zusammenarbeit, persönliche Betreuung und schnelle, lösungsorientierte Reaktionen. Durch den Einsatz modernster Technologien gewährleisten wir zukunftssichere und hochwertige Lösungen für unsere Kunden.</p>
  </div>
</section>

<section class="m-section">
  <div class="m-shell">
    <div class="m-solo">
      <img class="m-solo-photo" src="assets/portrait-scherzer.jpg" alt="Georg Scherzer" loading="lazy">
      <div class="m-solo-body">
        <div class="m-member-name">Georg Scherzer</div>
        <div class="m-member-role">Gründer · Medizintechniker</div>
        <div class="m-member-contact"><span class="k">Kontakt</span><a href="mailto:g.scherzer@medeqon.com">g.scherzer@medeqon.com</a><span class="sep">·</span><a href="tel:+436705505612">+43 670 5505612</a></div>
        <div class="m-member-langs"><span class="k">Sprachen</span>Deutsch (Muttersprache), Englisch, Französisch</div>
        <div class="m-member-quals">
          <span class="k">Erfahrung &amp; Qualifikationen</span>
          <ul class="ring-list">
            <li>Mehr als 15 Jahre Erfahrung in der Medizintechnik</li>
            <li>Ehemaliger Abteilungsleiter Medizintechnik am AKH Wien und am Universitätsklinikum Krems</li>
            <li>Internationale Projekterfahrung in Krisengebieten für das Rote Kreuz</li>
            <li>Beratungstätigkeiten für die WHO</li>
            <li>Allgemein beeideter und gerichtlich zertifizierter Sachverständiger (in Ausbildung)</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>'''

BODY_KONTAKT = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Kontakt</span>
    <h1>Wir sind gerne für Sie da<span class="end-dot">.</span></h1>
    <p class="lede">Ob Projektanfrage, Service, Beratung oder die Beschaffung von Medizinprodukten — kontaktieren Sie uns. Wir finden das passende Produkt und liefern zuverlässig. Unser Team meldet sich schnell und persönlich bei Ihnen.</p>
  </div>
</section>

<section class="m-section">
  <div class="m-shell">
    <div class="m-contactgrid">
      <div>
        <div class="m-secH" style="margin-bottom:28px">
          <span class="m-tag">Anfrage</span>
          <h2>Schreiben Sie uns<span class="end-dot">.</span></h2>
          <div class="sub">Felder mit * sind Pflichtfelder. Ihre Anfrage geht direkt an unser Team.</div>
        </div>
        <form class="m-form" id="kontaktForm" novalidate>
          <div class="m-field">
            <label for="k-name">Name *</label>
            <input class="m-input" id="k-name" name="Name" type="text" autocomplete="name" required>
          </div>
          <div class="m-form-row">
            <div class="m-field">
              <label for="k-mail">E-Mail *</label>
              <input class="m-input" id="k-mail" name="E-Mail" type="email" autocomplete="email" required>
            </div>
            <div class="m-field">
              <label for="k-tel">Telefon</label>
              <input class="m-input" id="k-tel" name="Telefon" type="tel" autocomplete="tel">
            </div>
          </div>
          <div class="m-field">
            <label for="k-org">Unternehmen</label>
            <input class="m-input" id="k-org" name="Unternehmen" type="text" autocomplete="organization">
          </div>
          <div class="m-field">
            <label for="k-topic">Anliegen</label>
            <select class="m-input" id="k-topic" name="Anliegen">
              <option>Projektanfrage</option>
              <option>Beratung / Consulting</option>
              <option>Beschaffung von Medizinprodukten</option>
              <option>Service / Prüfung</option>
              <option>Sonstiges</option>
            </select>
          </div>
          <div class="m-field">
            <label for="k-msg">Nachricht *</label>
            <textarea class="m-input" id="k-msg" name="Nachricht" required></textarea>
          </div>
          <label class="m-check">
            <input type="checkbox" name="Datenschutz akzeptiert" value="Ja" required>
            <span>Ich habe die <a href="datenschutz.html">Datenschutzerklärung</a> gelesen und bin mit der Verarbeitung meiner Angaben zur Bearbeitung meiner Anfrage einverstanden.</span>
          </label>
          <input type="text" name="_honey" class="m-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <input type="hidden" name="_subject" value="Neue Anfrage über medeqon.com">
          <input type="hidden" name="_template" value="table">
          <button class="m-btn" type="submit" id="k-submit">Anfrage senden</button>
          <div class="m-form-status" id="formStatus" role="status" aria-live="polite"></div>
          <noscript><p class="sub">Bitte aktivieren Sie JavaScript oder schreiben Sie uns direkt an office@medeqon.com.</p></noscript>
        </form>
      </div>

      <aside class="m-caside">
        <div>
          <span class="k">Direkt</span>
          <a href="mailto:office@medeqon.com">office@medeqon.com</a>
          <a href="tel:+436705505612">+43 670 550 5612</a>
        </div>
        <div>
          <span class="k">Büro</span>
          <p>Bergstraße 42/5/3<br>2102 Hagenbrunn · Österreich<br>Mo – Fr · nach Vereinbarung</p>
        </div>
      </aside>
    </div>
  </div>
</section>

<script>
(function(){
  var f=document.getElementById("kontaktForm");
  if(!f) return;
  var s=document.getElementById("formStatus");
  var btn=document.getElementById("k-submit");
  var ENDPOINT="https://formsubmit.co/ajax/office@medeqon.com";
  f.addEventListener("submit", function(e){
    e.preventDefault();
    if(f._honey.value){ return; }
    if(!f.checkValidity()){ f.reportValidity(); return; }
    btn.disabled=true;
    s.className="m-form-status is-sending"; s.textContent="Anfrage wird gesendet …";
    fetch(ENDPOINT,{method:"POST",headers:{"Accept":"application/json"},body:new FormData(f)})
      .then(function(r){ return r.json().catch(function(){return {};}); })
      .then(function(){
        s.className="m-form-status is-ok";
        s.textContent="Vielen Dank! Ihre Anfrage wurde gesendet – wir melden uns zeitnah bei Ihnen.";
        f.reset();
      })
      .catch(function(){
        s.className="m-form-status is-err";
        s.innerHTML="Beim Senden ist ein Fehler aufgetreten. Bitte schreiben Sie uns direkt an <a href=\"mailto:office@medeqon.com\">office@medeqon.com</a>.";
      })
      .then(function(){ btn.disabled=false; });
  });
})();
</script>'''

# ================= Referenzen (persönliche Referenzen G. Scherzer) =================
import re as _re
_ref_data = json.loads((ROOT / "referenzen.json").read_text(encoding="utf-8"))
_PIN = ('<svg class="m-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/>'
        '<circle cx="12" cy="10" r="2.4"/></svg>')

def _ref_eurnum(s):
    d = _re.sub(r'[^\d]', '', s or '')
    return int(d) if d else 0

def _ref_vol(n):
    if n >= 1_000_000:
        mio = n / 1_000_000
        if abs(mio - round(mio)) < 1e-9:
            return f"€ {int(round(mio))} Mio."
        return "€ " + f"{mio:.1f}".replace('.', ',') + " Mio."
    if n >= 1000:
        return f"€ {n//1000}.000"
    return f"€ {n}"

_ref_all = []
for _g in _ref_data["groups"]:
    for _p in _g["projects"]:
        _ref_all.append({**_p, "_client": _g["client"], "_num": _ref_eurnum(_p.get("kosten", ""))})
_ref_flags = sorted(_ref_all, key=lambda p: p["_num"], reverse=True)[:6]

def _ref_flag_card(p):
    return (
'        <figure class="m-ref-flag">\n'
f'          <div class="m-ref-flag-vol">{_ref_vol(p["_num"])}</div>\n'
f'          <div class="m-ref-flag-client">{_html.escape(p["_client"])}</div>\n'
f'          <h3 class="m-ref-flag-name">{_html.escape(p["name"])}</h3>\n'
f'          <p class="m-ref-flag-meta">{_html.escape(p.get("lph",""))} &middot; {_html.escape(p.get("dauer",""))}</p>\n'
'        </figure>')

def _ref_item(p):
    n = _ref_eurnum(p.get("kosten", ""))
    chips = []
    if p.get("lph"):   chips.append(f'<span class="m-ref-chip">{_html.escape(p["lph"])}</span>')
    if p.get("dauer"): chips.append(f'<span class="m-ref-chip">{_html.escape(p["dauer"])}</span>')
    chips.append(f'<span class="m-ref-vol">{_ref_vol(n)}</span>')
    return (
'            <div class="m-ref-item">\n'
'              <div class="m-ref-item-main">\n'
f'                <div class="m-ref-item-name">{_html.escape(p["name"])}</div>\n'
f'                <p class="m-ref-item-desc">{_html.escape(p.get("umfang",""))}</p>\n'
'              </div>\n'
f'              <div class="m-ref-item-meta">{"".join(chips)}</div>\n'
'            </div>')

def _ref_group(g, num):
    title = _html.escape(g["client"]) + " &middot; " + _html.escape(g["subtitle"])
    vol = _ref_vol(sum(_ref_eurnum(p.get("kosten", "")) for p in g["projects"]))
    items = "\n".join(_ref_item(p) for p in g["projects"])
    return (
f'      <details class="m-ac" id="ref-{g["id"]}">\n'
f'        <summary><span class="m-ac-num">{num}</span><span class="m-ac-title">{title}</span>' + CHEV + '</summary>\n'
'        <div class="m-ac-body">\n'
f'          <p class="m-pl-count">{len(g["projects"])} Projekte &middot; Beschaffungsvolumen {vol}</p>\n'
'          <div class="m-ref-list">\n'
+ items + '\n'
'          </div>\n'
'        </div>\n'
'      </details>')

_ref_groups_html = "\n".join(_ref_group(g, f"{i+1:02d}") for i, g in enumerate(_ref_data["groups"]))
_ref_flags_html = "\n".join(_ref_flag_card(p) for p in _ref_flags)

BODY_REFERENZEN = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Referenzen</span>
    <h1>Referenzen aus über 15 Jahren Medizintechnik<span class="end-dot">.</span></h1>
    <p class="lede">Eine Auswahl erfolgreich abgeschlossener Projekte aus der beruflichen Laufbahn unseres Gründers Georg Scherzer – von der Planung hochkomplexer klinischer Infrastruktur bis zur Beschaffung modernster Medizintechnik an führenden Häusern in Österreich und der Schweiz.</p>
  </div>
</section>

<section class="m-section">
  <div class="m-shell">
    <div class="m-ref-note">
      <span class="m-ref-note-cap">Wichtiger Hinweis</span>
      <p>Die nachfolgend gezeigten Projekte sind <strong>persönliche Referenzen von Georg Scherzer</strong> aus seiner bisherigen beruflichen Tätigkeit – erbracht in leitender Funktion am Allgemeinen Krankenhaus der Stadt Wien (AKH&nbsp;Wien) sowie bei der VAMED. Sie wurden nicht im Namen der medeqon&nbsp;GmbH realisiert. Als junges Unternehmen legen wir Wert auf diese Klarstellung – zugleich fließt genau diese über Jahre gewachsene Erfahrung in jedes medeqon-Projekt ein.</p>
    </div>

    <div class="m-ref-stats">
      <div class="m-ref-stat"><span class="m-ref-stat-num">55+</span><span class="m-ref-stat-label">Realisierte Projekte</span></div>
      <div class="m-ref-stat"><span class="m-ref-stat-num">€&nbsp;92&nbsp;Mio.</span><span class="m-ref-stat-label">Beschaffungsvolumen Medizintechnik</span></div>
      <div class="m-ref-stat"><span class="m-ref-stat-num">15+</span><span class="m-ref-stat-label">Jahre Erfahrung</span></div>
      <div class="m-ref-stat"><span class="m-ref-stat-num">3 Regionen</span><span class="m-ref-stat-label">Österreich, Schweiz &amp; Naher Osten</span></div>
    </div>
  </div>
</section>

<section class="m-section alt">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Auswahl</span>
      <h2 class="m-bigH">Leuchtturmprojekte<span class="end-dot">.</span></h2>
      <div class="sub">Eine Auswahl der umfangreichsten realisierten Projekte – gemessen am Beschaffungsvolumen der Medizintechnik.</div>
    </div>
    <div class="m-ref-flags">
''' + _ref_flags_html + '''
    </div>
  </div>
</section>

<section class="m-section">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Projektreferenzen</span>
      <h2 class="m-bigH">Vollständige Referenzliste<span class="end-dot">.</span></h2>
      <div class="sub">Gegliedert nach Auftraggeber und Verantwortungsbereich. Klicken Sie eine Gruppe an, um alle Projekte mit Details einzusehen.</div>
    </div>
    <div class="m-acc">
''' + _ref_groups_html + '''
    </div>
  </div>
</section>

<section class="m-section alt" id="nahost">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Internationale Einsätze</span>
      <h2 class="m-bigH">Projekte im Nahen Osten<span class="end-dot">.</span></h2>
      <div class="sub">Im Rahmen humanitärer und internationaler Einsätze war Georg Scherzer über rund zweieinhalb Jahre vor Ort im Nahen Osten tätig – in Regionen, die von Krisen und bewaffneten Konflikten geprägt sind. Der Schwerpunkt lag auf der bedarfsgerechten Ausstattung medizinischer Einrichtungen unter schwierigsten Rahmenbedingungen.</div>
    </div>

    <div class="m-nahost-stats">
      <div class="m-ref-stat"><span class="m-ref-stat-num">6</span><span class="m-ref-stat-label">Projekte vor Ort</span></div>
      <div class="m-ref-stat"><span class="m-ref-stat-num">2,5&nbsp;Jahre</span><span class="m-ref-stat-label">Tätigkeit in der Region</span></div>
      <div class="m-ref-stat"><span class="m-ref-stat-num">€&nbsp;8&nbsp;Mio.</span><span class="m-ref-stat-label">Beschaffungsvolumen</span></div>
    </div>

    <div class="m-nahost-grid">
      <div class="m-nahost-block">
        <div class="m-nahost-cap">6 Standorte</div>
        <div class="m-nahost-cities">
          <span class="m-nahost-city">''' + _PIN + '''Damaskus<em>Syrien</em></span>
          <span class="m-nahost-city">''' + _PIN + '''Homs<em>Syrien</em></span>
          <span class="m-nahost-city">''' + _PIN + '''Aleppo<em>Syrien</em></span>
          <span class="m-nahost-city">''' + _PIN + '''Latakia<em>Syrien</em></span>
          <span class="m-nahost-city">''' + _PIN + '''Amman<em>Jordanien</em></span>
          <span class="m-nahost-city">''' + _PIN + '''Beirut<em>Libanon</em></span>
        </div>
      </div>
      <div class="m-nahost-block">
        <div class="m-nahost-cap">Fachliche Schwerpunkte</div>
        <ul class="m-nahost-focus">
          <li>Bedarfsanalysen</li>
          <li>Gerätebewertungen</li>
          <li>Beschaffung</li>
          <li>Logistik</li>
          <li>Qualitätsüberprüfung von lokalen Händlern</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="m-section">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Akademisches &amp; Beratung</span>
      <h2 class="m-bigH">Wissenschaft &amp; internationale Beratung<span class="end-dot">.</span></h2>
      <div class="sub">Neben der praktischen Projektarbeit ist Georg Scherzer wissenschaftlich und beratend tätig – unter anderem für die Weltgesundheitsorganisation.</div>
    </div>
    <div class="m-ref-acad">
      <figure class="m-ref-acadcard">
        <span class="m-ref-acadcap">Internationale Beratung</span>
        <h3>World Health Organization (WHO)</h3>
        <p>Beratung zum „Compendium on innovative medical technologies" sowie Plenarbeitrag beim 3rd WHO Global Forum on Medical Devices zu Medizintechnik in Konfliktsituationen.</p>
      </figure>
      <figure class="m-ref-acadcard">
        <span class="m-ref-acadcap">Promotion</span>
        <h3>Doktorarbeit (PhD)</h3>
        <p>„Leading health care facilities in times of armed conflict: what are the constraints for medical equipment management?" – Dissertation zur Medizintechnik-Beschaffung unter Extrembedingungen.</p>
      </figure>
      <figure class="m-ref-acadcard">
        <span class="m-ref-acadcap">Publikationen</span>
        <h3>Peer-reviewed Fachartikel &amp; Fachbuch</h3>
        <p>Mehrere begutachtete Publikationen in internationalen Fachzeitschriften zu Medizintechnik, öffentlicher Gesundheit und Sicherheit sowie ein Fachbuch zu MRT-Sicherheit für Einsatzkräfte.</p>
      </figure>
      <figure class="m-ref-acadcard">
        <span class="m-ref-acadcap">Lehre &amp; Konferenzen</span>
        <h3>Vorträge &amp; akademische Betreuung</h3>
        <p>Beiträge auf internationalen Konferenzen (u.&nbsp;a. EuHEA, European Public Health Conference) sowie Betreuung einer Masterarbeit an der University of Copenhagen.</p>
      </figure>
    </div>
  </div>
</section>

<section class="m-cta-banner" style="background-image:url(assets/cta-banner.jpg)">
  <div class="m-shell">
    <div class="m-cta-banner-copy">
      <div class="line"></div>
      <h2>Ihr Projekt in erfahrenen Händen<span class="end-dot">.</span></h2>
      <a class="m-cta-link" href="kontakt.html">Projekt besprechen</a>
    </div>
  </div>
</section>'''

def legal_body(tag, title):
    return f'''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">{tag}</span>
    <h1>{title}<span class="end-dot">.</span></h1>
    <p class="lede">Der Inhalt dieser Seite wird demnächst ergänzt.</p>
  </div>
</section>

<section class="m-section">
  <div class="m-shell">
    <div class="m-soon">
      <span class="k">In Arbeit</span>
      <p>Sobald du mir den Text für „{title}“ zusendest (z. B. als Word-Dokument), füge ich ihn hier markengetreu ein.</p>
    </div>
  </div>
</section>'''

def load_content(name):
    return (ROOT/"content"/f"{name}.html").read_text(encoding="utf-8")

BODY_AGB = load_content("agb")
BODY_DATENSCHUTZ = load_content("datenschutz")
BODY_IMPRESSUM = load_content("impressum")

PAGES = [
    ("index.html", "medeqon · Ingenieurbüro für Medizintechnik",
     "medeqon GmbH — Wiener Ingenieurbüro für Medizintechnik. Planung, Beratung, Vermittlung und sicherheitstechnische Prüfung klinischer Infrastruktur in DACH und Polen.",
     "Startseite", BODY_INDEX),
    ("leistungen.html", "Leistungen · medeqon",
     "Leistungen von medeqon: Planung klinischer Infrastruktur, unabhängige Beratung und Vermittlung sowie sicherheitstechnische Prüfung und Abnahme.",
     "Leistungen", BODY_LEISTUNGEN),
    ("produkte.html", "Produkte · medeqon",
     "Produkte von medeqon — zertifizierte Medizintechnik. Inhalte folgen.",
     "Produkte", BODY_PRODUKTE),
    ("referenzen.html", "Referenzen · medeqon",
     "Persönliche Projektreferenzen von Georg Scherzer: über 50 realisierte Projekte am AKH Wien und bei VAMED mit rund € 84 Mio. Beschaffungsvolumen Medizintechnik.",
     "Referenzen", BODY_REFERENZEN),
    ("management.html", "Management · medeqon",
     "Das Management von medeqon: zwei erfahrene Medizintechniker:innen mit über 25 Jahren Erfahrung in klinischer Infrastruktur.",
     "Management", BODY_MANAGEMENT),
    ("kontakt.html", "Kontakt · medeqon",
     "Kontakt zu medeqon GmbH: office@medeqon.com, +43 670 550 5612, Bergstrasse 42/5/3, 2102 Hagenbrunn.",
     "Kontakt", BODY_KONTAKT),
    ("agb.html", "AGB · medeqon",
     "Allgemeine Geschäftsbedingungen der medeqon GmbH.",
     None, BODY_AGB),
    ("datenschutz.html", "Datenschutz · medeqon",
     "Datenschutzerklärung der medeqon GmbH.",
     None, BODY_DATENSCHUTZ),
    ("impressum.html", "Impressum · medeqon",
     "Impressum der medeqon GmbH.",
     None, BODY_IMPRESSUM),
]

for filename, title, desc, active, body in PAGES:
    html = page(filename, title, desc, active, body)
    (ROOT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename)
print("done")
