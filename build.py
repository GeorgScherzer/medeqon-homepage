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
    <p>Früher planen. Smarter bauen<span class="em">.</span></p>
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

# ---- Untersuchungsliegen (Elektrisch) — Karten aus Datenliste generieren ----
import json, html as _html
_liegen = json.loads((ROOT / "liegen_data.json").read_text(encoding="utf-8"))
def _render_liege(p):
    specs = "\n".join(
        f'                        <li><span>{_html.escape(k)}</span>{_html.escape(v)}</li>'
        for k, v in p["specs"])
    return (
'                  <article class="m-pl">\n'
'                    <div class="m-pl-gallery">\n'
f'                      <img class="m-pl-main" src="assets/produkte/{p["slug"]}/1.jpg" alt="{_html.escape(p["model"])}" loading="lazy">\n'
'                    </div>\n'
'                    <div class="m-pl-info">\n'
f'                      <span class="m-pl-ref">Ref. {_html.escape(p["ref"])}</span>\n'
f'                      <h4 class="m-pl-name">{_html.escape(p["model"])}</h4>\n'
f'                      <p class="m-pl-desc">{_html.escape(p["description"])}</p>\n'
'                      <ul class="m-pl-specs">\n'
f'{specs}\n'
'                      </ul>\n'
'                    </div>\n'
'                  </article>')
LIEGEN_CARDS = "\n\n".join(_render_liege(p) for p in _liegen)
_stuehle = json.loads((ROOT / "stuehle_data.json").read_text(encoding="utf-8"))
_sichtschutz = json.loads((ROOT / "sichtschutz_data.json").read_text(encoding="utf-8"))
STUEHLE_CARDS = "\n\n".join(_render_liege(p) for p in _stuehle)
SICHTSCHUTZ_CARDS = "\n\n".join(_render_liege(p) for p in _sichtschutz)

BODY_PRODUKTE = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Produkte</span>
    <h1>Unsere Produkte<span class="end-dot">.</span></h1>
    <p class="lede">Wir vermitteln und liefern zertifizierte Medizinprodukte in zwei Hauptkategorien: Strahlenschutz und Medizinische Einrichtung. Klicken Sie eine Kategorie an, um die einzelnen Bereiche aufzuklappen.</p>
  </div>
</section>

<section class="m-section" id="strahlenschutz">
  <div class="m-shell">
    <div class="m-cat-head">
      <h2>Strahlenschutz<span class="end-dot">.</span></h2>
      <div class="sub">Ein komplettes Sortiment an persönlichem Strahlenschutz sowie mobilen, deckenmontierten und tischmontierten Röntgenschutzsystemen – von spezialisierten Herstellern, vertrieben durch medeqon.</div>
    </div>

    <div class="m-acc">
      <details class="m-ac" id="persoenlicher-strahlenschutz" open>
        <summary><span class="m-ac-num">01</span><span class="m-ac-title">Persönlicher Strahlenschutz</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-ac-lead">Strahlenschutzbekleidung und Zubehör für den direkten Personenschutz – Bleischürzen, bleifreie Schürzen, Brillen, Handschuhe und ergänzender Schutz. Fokus auf Ergonomie, Gewichtsverteilung, Schutzleistung und Tragekomfort.</p>
          <span class="m-ac-src">Hersteller: OLEY Medical · vertrieben durch medeqon</span>
          <div class="m-cert">
            <span class="k">Qualität &amp; Konformität</span>
            <p>CE-zertifiziert · ISO-dokumentiert · PSA-Verordnung 2016/425 · Materialbewertung nach IEC 61331-1 · Schürzenkriterien nach IEC 61331-3.</p>
          </div>
          <div class="m-prod-grid">
            <div class="m-prod"><h4>Bleischürzen</h4><div class="spec">0,25 / 0,35 / 0,50 mm Pb · Dental- und Medizineinsatz · Antibakterielles Gewebe</div></div>
            <div class="m-prod"><h4>Edge-Bilayer-Schürzen</h4><div class="spec">0,25 / 0,35 / 0,50 mm Pb · Schweißabweisende Rückseite · Hydrophobes Gewebe</div></div>
            <div class="m-prod"><h4>Bleifreie Antimon-Schürze</h4><div class="spec">0,25 / 0,35 / 0,50 mm Pb · Bleifreies Antimon-Material · Antibakteriell</div></div>
            <div class="m-prod"><h4>Dental-Schutzschürze</h4><div class="spec">0,25 / 0,35 / 0,50 mm Pb · Leichtes Blei, bleifrei oder Bilayer-Edge</div></div>
            <div class="m-prod"><h4>Periapikale Schutzschürze</h4><div class="spec">0,25 / 0,35 / 0,50 mm Pb · Integrierter Schilddrüsenkragen 0,50 mm Pb</div></div>
            <div class="m-prod"><h4>Panorama-Schutzschürze</h4><div class="spec">0,25 / 0,35 / 0,50 mm Pb · Front- und Wirbelsäulenschutz</div></div>
            <div class="m-prod"><h4>Schutz-Lymphpad</h4><div class="spec">0,25 / 0,50 mm Pb · Blei- und bleifreie Optionen · Hals- und Achselschutz</div></div>
            <div class="m-prod"><h4>Strahlenschutzbrillen</h4><div class="desc">Bleibrillen, auch mit Korrektions-, Bifokal- oder Gleitsichtgläsern.</div></div>
            <div class="m-prod"><h4>Gonadenschutz</h4><div class="desc">Für Frauen, Männer, Neugeborene und Kinder – planbar mit Halbschürzengrößen.</div></div>
            <div class="m-prod"><h4>Strahlenschutzhandschuhe</h4><div class="desc">Sterile, puderfreie, latexfreie Handschuhe, Fäustlinge und Gummihandschuhe.</div></div>
            <div class="m-prod"><h4>Ergänzender Personenschutz</h4><div class="desc">Kopf-, Brust-, Schwangerschafts- und Gesichts-Bleischutz nach Bedarf.</div></div>
            <div class="m-prod"><h4>Kinder-Schutzschürzen</h4><div class="desc">Front-, Doppel- und Panorama-Schürzen in Kindergrößen.</div></div>
          </div>
        </div>
      </details>

      <details class="m-ac" id="mobiler-strahlenschutz">
        <summary><span class="m-ac-num">02</span><span class="m-ac-title">Mobiler Strahlenschutz</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-ac-lead">Fahrbare, frei positionierbare Röntgenschutzsysteme für flexible Einsätze im OP und in der interventionellen Radiologie – schützen Kopf, Augen, Schilddrüse und Körper vor Streustrahlung.</p>
          <span class="m-ac-src">Hersteller: KENEX (Electro-Medical) Ltd · vertrieben durch medeqon</span>
          <div class="m-cert">
            <span class="k">Qualität &amp; Konformität</span>
            <p>ISO 13485 · CE · EU 2017/745 (MDR) · EU 2016/425 (PSA) · IEC 60601 · ISO 14971 · Prüfung nach IEC EN 61331.</p>
          </div>
          <div class="m-prod-grid">
            <div class="m-prod"><h4>Mobiler Röntgenschutz</h4><div class="desc">Mobile, fahrbare Röntgenschutzsysteme für flexible Einsätze.</div></div>
          </div>
        </div>
      </details>

      <details class="m-ac" id="deckenmontierter-strahlenschutz">
        <summary><span class="m-ac-num">03</span><span class="m-ac-title">Deckenmontierter Strahlenschutz</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-ac-lead">Aufgehängte Überkopf-Schutzschilde, die von der Decke montiert werden und die Streustrahlung im Arbeitsbereich deutlich reduzieren.</p>
          <span class="m-ac-src">Hersteller: KENEX (Electro-Medical) Ltd · vertrieben durch medeqon</span>
          <div class="m-prod-grid">
            <div class="m-prod"><h4>Überkopf-Schutzschilde</h4><div class="desc">Aufgehängte Überkopf-Schutzschilde zur Reduktion von Streustrahlung.</div></div>
          </div>
        </div>
      </details>

      <details class="m-ac" id="tischmontierter-strahlenschutz">
        <summary><span class="m-ac-num">04</span><span class="m-ac-title">Tischmontierter Strahlenschutz</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-ac-lead">Am Untersuchungstisch montierte Schutzschilde für die interventionelle Radiologie – inklusive passender Aufbewahrungs- und Haltesysteme.</p>
          <span class="m-ac-src">Hersteller: KENEX (Electro-Medical) Ltd · vertrieben durch medeqon</span>
          <div class="m-prod-grid">
            <div class="m-prod"><h4>Tischmontierter Strahlenschutz</h4><div class="desc">Tischmontierte Schutzschilde für die interventionelle Radiologie.</div></div>
            <div class="m-prod"><h4>Aufbewahrung</h4><div class="desc">Aufbewahrungs- und Haltesysteme für Schutzkleidung und Schilde.</div></div>
          </div>
        </div>
      </details>
    </div>
  </div>
</section>

<section class="m-section alt" id="medizinische-einrichtung">
  <div class="m-shell">
    <div class="m-cat-head">
      <h2>Medizinische Einrichtung<span class="end-dot">.</span></h2>
      <div class="sub">Ausstattung und Einrichtung für klinische Bereiche – vom Untersuchungsplatz bis zum Sichtschutz. Die einzelnen Produktbereiche werden derzeit aufbereitet.</div>
    </div>

    <div class="m-acc">
      <details class="m-ac" id="untersuchungsliegen">
        <summary><span class="m-ac-num">01</span><span class="m-ac-title">Untersuchungsliegen</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-ac-lead">Untersuchungs- und Behandlungsliegen für Praxis und Klinik – in drei Antriebsvarianten.</p>
          <div class="m-acc m-acc-nested">

            <details class="m-ac m-ac-sub" id="liegen-elektrisch" open>
              <summary><span class="m-ac-title">Elektrisch</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-pl-count">''' + str(len(_liegen)) + ''' Modelle verfügbar</p>
                <div class="m-pl-list">
''' + LIEGEN_CARDS + '''
                </div>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="liegen-hydraulisch">
              <summary><span class="m-ac-title">Hydraulisch</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-ac-lead">Hydraulisch höhenverstellbare Untersuchungs- und Behandlungsliegen.</p>
                <span class="m-ac-soon">◦ Inhalte in Vorbereitung</span>
              </div>
            </details>

            <details class="m-ac m-ac-sub" id="liegen-fix">
              <summary><span class="m-ac-title">Fix</span>''' + CHEV + '''</summary>
              <div class="m-ac-body">
                <p class="m-ac-lead">Untersuchungsliegen mit fixer Höhe – robust und wartungsarm.</p>
                <span class="m-ac-soon">◦ Inhalte in Vorbereitung</span>
              </div>
            </details>

          </div>
        </div>
      </details>

      <details class="m-ac" id="medizinische-stuehle">
        <summary><span class="m-ac-num">02</span><span class="m-ac-title">Medizinische Stühle</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-ac-lead">Behandlungs-, Blutabnahme- und Arbeitsstühle sowie Hocker für den medizinischen Einsatz.</p>
          <p class="m-pl-count">''' + str(len(_stuehle)) + ''' Modelle verfügbar</p>
          <div class="m-pl-list">
''' + STUEHLE_CARDS + '''
          </div>
        </div>
      </details>

      <details class="m-ac" id="sichtschutz">
        <summary><span class="m-ac-num">03</span><span class="m-ac-title">Sichtschutz</span>''' + CHEV + '''</summary>
        <div class="m-ac-body">
          <p class="m-ac-lead">Sicht- und Trennwandsysteme für diskrete, flexibel teilbare Raumbereiche.</p>
          <div class="m-pl-list">
''' + SICHTSCHUTZ_CARDS + '''
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
