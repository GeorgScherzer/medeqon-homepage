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

BODY_PRODUKTE = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Produkte</span>
    <h1>Unsere Produkte<span class="end-dot">.</span></h1>
    <p class="lede">Wir vermitteln und liefern zertifizierte Medizinprodukte in mehreren Kategorien: Strahlenschutz, Medizinische Einrichtung und Heilbehelfe &amp; Hilfsmittel. Klicken Sie eine Kategorie an, um die einzelnen Bereiche aufzuklappen.</p>
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
