#!/usr/bin/env python3
"""Generate all medeqon website pages from one shared template.
Header + footer are identical on every page; only the body changes.
Run: python3 build.py
"""
from pathlib import Path
import urllib.parse as _urlparse

ROOT = Path(__file__).parent

# ---- Navigation (main pages, in order) ----------------------------------
NAV = [
    ("index.html", "Startseite"),
    ("leistungen.html", "Leistungen"),
    ("produkte.html", "Produkte"),
    ("referenzen.html", "Referenzen"),
    ("management.html", "Management"),
    ("karriere.html", "Karriere"),
    ("kontakt.html", "Kontakt"),
]

# Schriften werden selbst gehostet (siehe @font-face in styles.css) — kein externer Font-Aufruf mehr.
FONTS = ""
FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Crect width='100' height='100' rx='24' fill='%23004AAD'/%3E%3Ctext x='50' y='70' "
    "font-family='Arial,sans-serif' font-size='60' font-weight='700' fill='white' "
    "text-anchor='middle'%3Em%3C/text%3E%3C/svg%3E"
)

# ---- Mehrsprachigkeit ----------------------------------------------------
LANGS = [
    {"code": "de", "prefix": "",    "label": "DE", "name": "Deutsch"},
    {"code": "en", "prefix": "en/", "label": "EN", "name": "English"},
    {"code": "pl", "prefix": "pl/", "label": "PL", "name": "Polski"},
    {"code": "ro", "prefix": "ro/", "label": "RO", "name": "Română"},
]
# Sprachen, für die eine bestimmte Seite bereits übersetzt vorliegt.
# Nicht übersetzte Seiten fallen im Menü/Umschalter auf Deutsch zurück.
AVAILABLE = {
    "de": {"index.html", "leistungen.html", "produkte.html", "referenzen.html",
           "management.html", "karriere.html", "kontakt.html",
           "agb.html", "datenschutz.html", "impressum.html"},
    "en": {"index.html", "leistungen.html", "produkte.html", "referenzen.html", "management.html", "kontakt.html", "karriere.html", "agb.html", "datenschutz.html", "impressum.html"},
    "pl": {"index.html", "leistungen.html", "produkte.html", "referenzen.html", "management.html", "kontakt.html", "karriere.html", "agb.html", "datenschutz.html", "impressum.html"},
    "ro": {"index.html", "leistungen.html", "produkte.html", "referenzen.html", "management.html", "kontakt.html", "karriere.html", "agb.html", "datenschutz.html", "impressum.html"},
}

NAV_LABELS = {
    "de": {"index.html": "Startseite", "leistungen.html": "Leistungen", "produkte.html": "Produkte",
           "referenzen.html": "Referenzen", "management.html": "Management",
           "karriere.html": "Karriere", "kontakt.html": "Kontakt"},
    "en": {"index.html": "Home", "leistungen.html": "Services", "produkte.html": "Products",
           "referenzen.html": "References", "management.html": "Management",
           "karriere.html": "Careers", "kontakt.html": "Contact"},
    "pl": {"index.html": "Start", "leistungen.html": "Usługi", "produkte.html": "Produkty",
           "referenzen.html": "Referencje", "management.html": "Kierownictwo",
           "karriere.html": "Kariera", "kontakt.html": "Kontakt"},
    "ro": {"index.html": "Acasă", "leistungen.html": "Servicii", "produkte.html": "Produse",
           "referenzen.html": "Referințe", "management.html": "Management",
           "karriere.html": "Cariere", "kontakt.html": "Contact"},
}

def _href(filename, lang):
    """Wurzelabsoluter Link zur Seite in Sprache `lang` (mit Deutsch-Fallback)."""
    if lang != "de" and filename in AVAILABLE.get(lang, set()):
        return "/" + lang + "/" + filename
    return "/" + filename

# Landesflaggen als kompakte Inline-SVGs (viewBox 0 0 60 40)
FLAGS = {
    "de": '<svg viewBox="0 0 60 40" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="60" height="40" fill="#000"/><rect y="13.34" width="60" height="13.33" fill="#DD0000"/><rect y="26.67" width="60" height="13.33" fill="#FFCE00"/></svg>',
    "en": '<svg viewBox="0 0 60 40" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><clipPath id="flgen"><rect width="60" height="40"/></clipPath><g clip-path="url(#flgen)"><rect width="60" height="40" fill="#012169"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="8"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#C8102E" stroke-width="4"/><rect x="24" width="12" height="40" fill="#fff"/><rect y="14" width="60" height="12" fill="#fff"/><rect x="26" width="8" height="40" fill="#C8102E"/><rect y="16" width="60" height="8" fill="#C8102E"/></g></svg>',
    "pl": '<svg viewBox="0 0 60 40" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="60" height="20" fill="#fff"/><rect y="20" width="60" height="20" fill="#DC143C"/></svg>',
    "ro": '<svg viewBox="0 0 60 40" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="20" height="40" fill="#002B7F"/><rect x="20" width="20" height="40" fill="#FCD116"/><rect x="40" width="20" height="40" fill="#CE1126"/></svg>',
}

def _lang_switcher(filename, lang):
    opts = []
    for L in LANGS:
        code = L["code"]
        on = " is-on" if code == lang else ""
        cur = ' aria-current="true"' if code == lang else ''
        opts.append(f'<a class="m-flag{on}" href="{_href(filename, code)}" '
                    f'hreflang="{code}" title="{L["name"]}" aria-label="{L["name"]}"{cur}>'
                    f'{FLAGS[code]}</a>')
    return ('  <div class="m-lang" role="group" aria-label="Sprache / Language">\n    '
            + "".join(opts) + '\n  </div>')

def header(filename, lang="de"):
    labels = NAV_LABELS[lang]
    def link(fn):
        cls = ' class="active"' if fn == filename else ''
        return f'    <a href="{_href(fn, lang)}"{cls}>{labels[fn]}</a>'
    links = "\n".join(link(fn) for fn, _ in NAV)
    return f'''<header class="m-nav">
  <a class="brandlogo" href="{_href("index.html", lang)}" aria-label="medeqon — {labels["index.html"]}">
    <span class="brandlogo-mono" aria-hidden="true">m</span>
    <span class="brandlogo-word">medeqon</span>
  </a>
  <nav class="m-nav-links" aria-label="Navigation">
{links}
  </nav>
{_lang_switcher(filename, lang)}
</header>'''

_FOOT_ICONS = {
    "planung": '<svg class="m-foot-ico" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 38 L38 38 L10 12 Z"/><path d="M10 27 L21 27"/><circle cx="38" cy="38" r="2.6" class="sig-fill"/></svg>',
    "consulting": '<svg class="m-foot-ico" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 13 h26 a3 3 0 0 1 3 3 v13 a3 3 0 0 1 -3 3 H21 l-7 6 v-6 h-2 a3 3 0 0 1 -3 -3 V16 a3 3 0 0 1 3 -3 Z"/><circle cx="23" cy="22.5" r="2.4" class="sig-fill"/></svg>',
    "handel": '<svg class="m-foot-ico" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 8 L39 16 L39 32 L24 40 L9 32 L9 16 Z"/><path d="M9 16 L24 24 L39 16"/><path d="M24 24 L24 40"/><circle cx="24" cy="24" r="2.4" class="sig-fill"/></svg>',
    "pruefung": '<svg class="m-foot-ico" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="21" cy="21" r="11"/><path d="M29 29 L39 39"/><path d="M16.5 21.5 l3.5 3.5 l6.5 -7.5" class="sig-stroke"/></svg>',
}
_FOOT_T = {
    "de": {"tagline": "Ingenieurbüro für Medizintechnik.", "svc": "Leistungen",
           "planung": "Planung", "consulting": "Consulting", "handel": "Handel", "pruefung": "Prüfung",
           "contact": "Kontakt", "legal": "Rechtliches", "agb": "AGB", "ds": "Datenschutz", "imp": "Impressum",
           "b1": "Ingenieurbüro — staatlich geprüft", "b2": "Medizinproduktehandel — staatlich geprüft",
           "b3": "Ingenieurbüros Österreich · EU", "skip": "Zum Inhalt springen"},
    "en": {"tagline": "Medical technology engineering firm.", "svc": "Services",
           "planung": "Medical Technology Design", "consulting": "Consulting", "handel": "Procurement", "pruefung": "Inspection",
           "contact": "Contact", "legal": "Legal", "agb": "Terms &amp; Conditions", "ds": "Privacy", "imp": "Imprint",
           "b1": "Engineering firm — state-certified", "b2": "Medical device trade — state-certified",
           "b3": "Engineering firms Austria · EU", "skip": "Skip to content"},
    "pl": {"tagline": "Biuro inżynieryjne techniki medycznej.", "svc": "Usługi",
           "planung": "Projektowanie techniki medycznej", "consulting": "Doradztwo", "handel": "Zaopatrzenie", "pruefung": "Kontrola techniczna",
           "contact": "Kontakt", "legal": "Informacje prawne", "agb": "Regulamin", "ds": "Prywatność", "imp": "Nota prawna",
           "b1": "Biuro inżynieryjne — certyfikat państwowy", "b2": "Handel wyrobami medycznymi — certyfikat państwowy",
           "b3": "Biura inżynieryjne Austria · UE", "skip": "Przejdź do treści"},
    "ro": {"tagline": "Birou de inginerie pentru tehnologie medicală.", "svc": "Servicii",
           "planung": "Proiectarea tehnologiei medicale", "consulting": "Consultanță", "handel": "Achiziții", "pruefung": "Verificare tehnică",
           "contact": "Contact", "legal": "Informații legale", "agb": "Termeni și condiții", "ds": "Confidențialitate", "imp": "Notă legală",
           "b1": "Birou de inginerie — certificat de stat", "b2": "Comerț cu dispozitive medicale — certificat de stat",
           "b3": "Birouri de inginerie Austria · UE", "skip": "Salt la conținut"},
}

def footer(lang="de"):
    t = _FOOT_T[lang]
    def svc(anchor, key):
        return (f'        <a class="m-foot-svc" href="{_href("leistungen.html", lang)}#{anchor}">'
                f'{_FOOT_ICONS[anchor]}<span>{t[key]}</span></a>')
    return f'''<footer class="m-foot">
  <div class="m-shell m-foot-top">
    <div class="m-foot-brand">
      <a class="m-foot-logo" href="{_href("index.html", lang)}" aria-label="medeqon">
        <span class="m-foot-mono" aria-hidden="true">m</span>
        <span class="m-foot-word">medeqon</span>
      </a>
      <div class="m-foot-words">{t["tagline"]}</div>
      <div class="m-foot-legalline">medeqon GmbH<br>FN&nbsp;672926y<br>UID&nbsp;ATU83016237</div>
    </div>
    <div class="m-foot-links">
      <div class="m-foot-col">
        <div class="m-foot-tag">{t["svc"]}</div>
{svc("planung","planung")}
{svc("consulting","consulting")}
{svc("handel","handel")}
{svc("pruefung","pruefung")}
      </div>
      <div class="m-foot-col">
        <div class="m-foot-tag">{t["contact"]}</div>
        <a href="mailto:office@medeqon.com">office@medeqon.com</a>
        <a href="tel:+4313580045">+43 1 3580045</a>
        <a href="https://www.medeqon.com">www.medeqon.com</a>
        <div class="m-foot-plain">Bergstrasse 42/5/3<br>2102 Hagenbrunn · AT</div>
      </div>
      <div class="m-foot-col">
        <div class="m-foot-tag">{t["legal"]}</div>
        <a href="{_href("agb.html", lang)}">{t["agb"]}</a>
        <a href="{_href("datenschutz.html", lang)}">{t["ds"]}</a>
        <a href="{_href("impressum.html", lang)}">{t["imp"]}</a>
      </div>
    </div>
    <div class="m-foot-badges">
      <img class="m-badge" src="/assets/siegel-ingenieurbuero.png" alt="{t["b1"]}" loading="lazy">
      <img class="m-badge" src="/assets/siegel-medizinproduktehandel.png" alt="{t["b2"]}" loading="lazy">
      <img class="m-badge m-badge-wide" src="/assets/siegel-ingenieurbueros-at-eu.png" alt="{t["b3"]}" loading="lazy">
    </div>
  </div>
  <div class="m-shell m-foot-base">
    <div>© 2026 medeqon GmbH</div>
    <div>MED-CI-01 · V2.0</div>
  </div>
</footer>'''

_COOKIE = {
    "de": ("Diese Website verwendet nur technisch notwendige Cookies, die für den Betrieb erforderlich sind. Es findet kein Tracking statt.", "Datenschutzerklärung", "Verstanden"),
    "en": ("This website only uses technically necessary cookies required for its operation. No tracking takes place.", "Privacy policy", "Got it"),
    "pl": ("Ta strona używa wyłącznie technicznie niezbędnych plików cookie, koniecznych do jej działania. Nie odbywa się żadne śledzenie.", "Polityka prywatności", "Rozumiem"),
    "ro": ("Acest site utilizează doar cookie-uri necesare din punct de vedere tehnic pentru funcționarea sa. Nu are loc nicio urmărire.", "Politica de confidențialitate", "Am înțeles"),
}

def cookie_banner(lang="de"):
    txt, more, ok = _COOKIE.get(lang, _COOKIE["de"])
    ds = _href("datenschutz.html", lang)
    return f'''<div class="m-cookie" id="cookieBar" role="region" aria-label="Cookie" hidden>
  <p class="m-cookie-txt">{txt} <a href="{ds}">{more}</a></p>
  <button class="m-cookie-ok" id="cookieOk" type="button">{ok}</button>
</div>
<script>
(function(){{
  try{{ if(localStorage.getItem('mq_cookie')==='1') return; }}catch(e){{}}
  var bar=document.getElementById('cookieBar'); if(!bar) return;
  bar.removeAttribute('hidden');
  var b=document.getElementById('cookieOk');
  if(b) b.addEventListener('click', function(){{
    bar.setAttribute('hidden','');
    try{{ localStorage.setItem('mq_cookie','1'); }}catch(e){{}}
  }});
}})();
</script>'''

def page(filename, title, desc, body, lang="de"):
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#004AAD">
<link rel="icon" href="{FAVICON}">
{FONTS}
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip" href="#main">{_FOOT_T[lang]["skip"]}</a>

{header(filename, lang)}

<main id="main">
{body}
</main>

{footer(lang)}

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

{cookie_banner(lang)}

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

<!--FLYER-->

<section class="m-section" id="tco">
  <div class="m-shell">
    <div class="m-tco-truecost">
      <div class="m-tco-intro">
        <span class="m-tag">Total Cost of Ownership</span>
        <h2 class="m-bigH">Was kostet Medizintechnik wirklich<span class="end-dot">?</span></h2>
        <p class="m-tco-lead">Der Anschaffungspreis ist nur die Spitze des Eisbergs. Über den gesamten Lebenszyklus entstehen weit höhere Kosten – im Betrieb, in der Wartung, im Verbrauch und im Personal. Wir kennen diese Gesamtkosten im Detail und beziehen sie von Anfang an in jede Entscheidung ein.</p>
        <p class="m-tco-principle">Früh planen · Gesamtkosten senken · Werterhalt langfristig sichern<span class="em">.</span></p>
      </div>

      <figure class="m-tco-iceberg">
          <svg viewBox="0 0 680 620" role="img" aria-label="Eisberg-Modell: Über der Wasserlinie die sichtbaren Anschaffungskosten, darunter die verborgenen Kosten wie Transport, Installation, Inbetriebnahme, Betriebskosten, Personal, Verbrauchsmaterial, Wartung, Schulung und Entsorgung." xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="icebergGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0" stop-color="#6AA0D6"/>
                <stop offset="0.5" stop-color="#1E63B3"/>
                <stop offset="1" stop-color="#003278"/>
              </linearGradient>
            </defs>
            <rect x="0" y="210" width="680" height="410" fill="#E8EEF7"/>
            <polygon points="296,209 320,146 342,106 362,90 384,108 406,148 424,209" fill="#D5E1F2"/>
            <polygon points="296,210 256,250 226,330 240,432 276,520 326,586 362,602 402,584 446,516 470,426 478,330 452,250 424,210" fill="url(#icebergGrad)"/>
            <line x1="30" y1="210" x2="650" y2="210" stroke="#004AAD" stroke-width="1.5"/>
            <circle cx="30" cy="210" r="4" fill="#fff" stroke="#004AAD" stroke-width="1.5"/>
            <text x="646" y="202" font-family="IBM Plex Mono, monospace" font-size="15" letter-spacing="1" fill="#6B7785" text-anchor="end">WASSERLINIE</text>
            <line x1="368" y1="112" x2="452" y2="92" stroke="#0F1B2C" stroke-width="1.3"/>
            <circle cx="368" cy="112" r="4" fill="#004AAD"/>
            <text x="460" y="84" font-family="IBM Plex Mono, monospace" font-size="12" letter-spacing="1" fill="#6B7785">DIE SPITZE</text>
            <text x="460" y="107" font-family="Hanken Grotesk, sans-serif" font-size="19" font-weight="700" fill="#0F1B2C">Anschaffungskosten</text>
            <g fill="#fff" font-family="Hanken Grotesk, sans-serif" font-size="15.5" font-weight="600" text-anchor="middle">
              <text x="362" y="248">Transport</text>
              <text x="362" y="286">Installation</text>
              <text x="362" y="324">Inbetriebnahme</text>
              <text x="362" y="362">Betriebskosten</text>
              <text x="362" y="400">Personalkosten</text>
              <text x="362" y="438">Verbrauchsmaterial</text>
              <text x="362" y="476">Wartung</text>
              <text x="362" y="514">Schulung</text>
              <text x="362" y="552">Entsorgung</text>
            </g>
            <g>
              <line x1="54" y1="130" x2="54" y2="192" stroke="#004AAD" stroke-width="2.5"/>
              <text x="70" y="148" font-family="IBM Plex Mono, monospace" font-size="15" letter-spacing="1" fill="#004AAD">SICHTBAR</text>
              <text x="70" y="171" font-family="Hanken Grotesk, sans-serif" font-size="16" fill="#6B7785">was der Preis</text>
              <text x="70" y="190" font-family="Hanken Grotesk, sans-serif" font-size="16" fill="#6B7785">zeigt</text>
              <line x1="54" y1="250" x2="54" y2="454" stroke="#004AAD" stroke-width="2.5"/>
              <text x="70" y="300" font-family="IBM Plex Mono, monospace" font-size="15" letter-spacing="1" fill="#004AAD">VERBORGEN</text>
              <text x="70" y="323" font-family="Hanken Grotesk, sans-serif" font-size="16" fill="#6B7785">was das Gerät</text>
              <text x="70" y="343" font-family="Hanken Grotesk, sans-serif" font-size="16" fill="#6B7785">wirklich kostet</text>
            </g>
          </svg>
          <figcaption>Der Kaufpreis ist nur die Spitze des Eisbergs.</figcaption>
        </figure>
    </div>

    <div class="m-tco-below">
      <div class="m-tco-split-bar">
        <span class="seg-acq" style="width:20%"><em>20&thinsp;%</em>Anschaffung</span>
        <span class="seg-op" style="width:80%"><em>80&thinsp;%</em>Betrieb über den Lebenszyklus</span>
      </div>
      <p class="m-tco-split-cap">Der Anschaffungspreis macht typischerweise nur rund ein Fünftel der Gesamtkosten aus – der Großteil entsteht im laufenden Betrieb: Wartung, Verbrauch, Energie und Personal.</p>
    </div>
  </div>
</section>

<section class="m-section alt" id="mtd">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Medizintechnik-Planung</span>
      <h2 class="m-bigH">Frühe Planung, die sich über den gesamten Lebenszyklus rechnet<span class="end-dot">.</span></h2>
      <div class="sub">Wir bringen Medizintechnik von der ersten Konzeptphase an in die Planung ein – das senkt Kosten, schafft Termin- und Kostensicherheit und verankert die Anforderungen des späteren Betriebs von Beginn an.</div>
    </div>

    <div class="m-tco-cards">
        <div class="m-tco-card m-tco-card--early">
          <span class="m-tco-card-cap">Frühe Integration</span>
          <p>Anforderungen an Funktion, Betrieb, Infrastruktur und Kosteneffizienz werden von Beginn an berücksichtigt.</p>
        </div>
        <div class="m-tco-card m-tco-card--warn">
          <span class="m-tco-card-cap">Ohne Medizintechnik-Planung</span>
          <p>Höhere Kosten und erhöhter Koordinationsaufwand in späteren Projektphasen.</p>
        </div>
        <div class="m-tco-card m-tco-card--task">
          <span class="m-tco-card-cap">Unsere Aufgabe</span>
          <p class="m-tco-card-title">Verlässliche Grundlagen in den frühen Phasen schaffen<span class="em">.</span></p>
        </div>
      </div>

      <figure class="m-tco-chart">
        <div class="m-tco-chart-title">Kosteneffizienz durch frühe Planung</div>
        <svg viewBox="0 0 720 400" role="img" aria-label="Diagramm: Projektkosten über 30 Jahre – mit früher Planung deutlich niedrigere Lebenszykluskosten." xmlns="http://www.w3.org/2000/svg">
          <line x1="64" y1="48" x2="64" y2="320" stroke="#0F1B2C" stroke-width="1.5"/>
          <line x1="64" y1="320" x2="612" y2="320" stroke="#0F1B2C" stroke-width="1.5"/>
          <path d="M64,320 C120,300 150,285 163,268 C210,238 235,222 262,198 C310,168 335,158 361,138 C408,110 432,98 460,84 C505,68 535,64 560,58 L560,141 C520,146 480,151 411,157 C350,162 330,173 262,179 C228,182 205,184 163,200 C138,214 108,252 64,320 Z" fill="#004AAD" fill-opacity="0.08"/>
          <path d="M64,320 C120,300 150,285 163,268 C210,238 235,222 262,198 C310,168 335,158 361,138 C408,110 432,98 460,84 C505,68 535,64 560,58" fill="none" stroke="#5B9BD5" stroke-width="4" stroke-linecap="round"/>
          <path d="M64,320 C108,252 138,214 163,200 C205,184 228,182 262,179 C330,173 350,162 411,157 C480,151 520,146 560,141" fill="none" stroke="#004AAD" stroke-width="4" stroke-linecap="round"/>
          <circle cx="560" cy="58" r="6" fill="#5B9BD5"/>
          <circle cx="560" cy="141" r="6" fill="#004AAD"/>
          <text x="576" y="51" font-family="Hanken Grotesk, sans-serif" font-size="16.5" font-weight="700" fill="#5B9BD5">Kosten ohne</text>
          <text x="576" y="71" font-family="Hanken Grotesk, sans-serif" font-size="16.5" font-weight="700" fill="#5B9BD5">Planung</text>
          <text x="576" y="134" font-family="Hanken Grotesk, sans-serif" font-size="16.5" font-weight="700" fill="#004AAD">Kosten mit</text>
          <text x="576" y="154" font-family="Hanken Grotesk, sans-serif" font-size="16.5" font-weight="700" fill="#004AAD">Planung</text>
          <g stroke-linecap="round">
            <line x1="560" y1="66" x2="560" y2="133" stroke="#159A55" stroke-width="2.4"/>
            <polygon points="560,64 555,73 565,73" fill="#159A55"/>
            <polygon points="560,135 555,126 565,126" fill="#159A55"/>
          </g>
          <text x="551" y="106" text-anchor="end" font-family="Hanken Grotesk, sans-serif" font-size="15.5" font-weight="700" fill="#159A55">Ersparnis</text>
          <g font-family="IBM Plex Mono, monospace" font-size="14" fill="#0F1B2C" text-anchor="middle">
            <text x="64" y="342">0</text><text x="155" y="342">5</text><text x="246" y="342">10</text>
            <text x="336" y="342">15</text><text x="427" y="342">20</text><text x="518" y="342">25</text><text x="560" y="342">30</text>
          </g>
          <text x="628" y="325" font-family="IBM Plex Mono, monospace" font-size="14" fill="#0F1B2C">Jahre</text>
          <text x="22" y="184" font-family="IBM Plex Mono, monospace" font-size="12.5" letter-spacing="1.5" fill="#0F1B2C" transform="rotate(-90 22 184)" text-anchor="middle">PROJEKTKOSTEN</text>
          <rect x="64" y="356" width="99" height="24" rx="5" fill="#D5E1F2"/>
          <rect x="167" y="356" width="445" height="24" rx="5" fill="#E8EEF7"/>
          <text x="113" y="372" font-family="IBM Plex Mono, monospace" font-size="12.5" letter-spacing="1" fill="#004AAD" text-anchor="middle">PLANUNG</text>
          <text x="389" y="372" font-family="IBM Plex Mono, monospace" font-size="12.5" letter-spacing="1" fill="#0F1B2C" text-anchor="middle">BETRIEB</text>
        </svg>
        <figcaption>Früh planen. Geringere Lebenszykluskosten.</figcaption>
      </figure>

    <h3 class="m-mtd-subhead">Medizintechnik-Planung als integraler Prozess</h3>
    <div class="m-mtd-enable">
      <span class="m-mtd-enable-cap">Was unsere Medizintechnik-Planung ermöglicht</span>
      <div class="m-mtd-enable-items">
        <span>Weniger Änderungen</span>
        <span>Sichere Kosten</span>
        <span>Verlässliche Termine</span>
        <span>Effiziente Zusammenarbeit</span>
        <span>Optimale Betriebsabläufe</span>
      </div>
    </div>
    <figure class="m-mtd-figure">
      <img src="assets/brands/integrated-design-model-mist.png" alt="Integriertes Planungsmodell – BIM als zentrale Koordinationsdrehscheibe zwischen Architektur, Medizintechnik, Gebäudetechnik und Betriebsorganisation, geprägt von Budget, Hygieneanforderungen, behördlichen Anforderungen und Nutzerbedürfnissen." loading="lazy">
    </figure>
  </div>
</section>

<section class="m-section" id="bim">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">BIM</span>
      <h2 class="m-bigH">BIM-basierte Planung und standardisierte Prozesse<span class="end-dot">.</span></h2>
      <div class="sub">Modellbasiertes Arbeiten, eigene Datenbanken und wiederholbare Ergebnisse – das Rückgrat unserer Medizintechnik-Planung.</div>
    </div>
    <div class="m-bim-grid">
      <figure class="m-bim-figure">
        <svg viewBox="-30 0 400 300" role="img" aria-label="BIM als zentrale Koordinationsdrehscheibe – vernetzt mit IFC, REVIT, BCF und Daten." xmlns="http://www.w3.org/2000/svg">
          <circle cx="160" cy="150" r="118" fill="none" stroke="#E8EEF7" stroke-width="1"/>
          <circle cx="160" cy="150" r="88" fill="none" stroke="#E8EEF7" stroke-width="1"/>
          <circle cx="160" cy="150" r="58" fill="none" stroke="#E8EEF7" stroke-width="1"/>
          <g stroke="#9DBCE3" stroke-width="1.5">
            <line x1="160" y1="150" x2="160" y2="40"/>
            <line x1="160" y1="150" x2="270" y2="150"/>
            <line x1="160" y1="150" x2="160" y2="260"/>
            <line x1="160" y1="150" x2="50" y2="150"/>
          </g>
          <circle cx="160" cy="150" r="50" fill="#004AAD"/>
          <text x="160" y="147" font-family="Hanken Grotesk, sans-serif" font-size="23" font-weight="700" fill="#fff" text-anchor="middle">BIM</text>
          <text x="160" y="167" font-family="Hanken Grotesk, sans-serif" font-size="11" font-weight="500" fill="#fff" text-anchor="middle">Koordination</text>
          <g fill="#fff" stroke="#004AAD" stroke-width="2">
            <circle cx="160" cy="40" r="17"/><circle cx="270" cy="150" r="17"/>
            <circle cx="160" cy="260" r="17"/><circle cx="50" cy="150" r="17"/>
          </g>
          <g fill="#004AAD" stroke="none">
            <circle cx="160" cy="40" r="3.2"/><circle cx="270" cy="150" r="3.2"/>
            <circle cx="160" cy="260" r="3.2"/><circle cx="50" cy="150" r="3.2"/>
          </g>
          <g font-family="Hanken Grotesk, sans-serif" font-size="14.5" font-weight="700" fill="#0F1B2C">
            <text x="160" y="20" text-anchor="middle">IFC</text>
            <text x="294" y="155" text-anchor="start">REVIT</text>
            <text x="160" y="297" text-anchor="middle">BCF</text>
            <text x="26" y="155" text-anchor="end">Daten</text>
          </g>
        </svg>
      </figure>
      <div class="m-bim-points">
        <div class="m-bim-card">
          <span class="m-bim-cap">01 · Tool</span>
          <h3>Modellbasierte Arbeitsweise</h3>
          <ul>
            <li>Autodesk Revit als Standardwerkzeug</li>
            <li>Modellbasierte Planung über alle Leistungsphasen</li>
            <li>Integration in Architektur- und TGA-Modelle</li>
          </ul>
        </div>
        <div class="m-bim-card">
          <span class="m-bim-cap">02 · Data</span>
          <h3>Eigene Datenbanken</h3>
          <ul>
            <li>Geräte- und Anschlussdatenbank</li>
            <li>BIM-Familienbibliothek</li>
          </ul>
        </div>
        <div class="m-bim-card">
          <span class="m-bim-cap">03 · Process</span>
          <h3>Standardisierte Ergebnisse</h3>
          <ul>
            <li>Strukturierte Raumbücher und Funktionsprogramme</li>
            <li>Geprüfte Ausschreibungstexte</li>
            <li>Wissensbasis aus laufender Projektarbeit</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<!--PARTNER-->

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

BODY_LEISTUNGEN_EN = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Services</span>
    <h1>Our Services<span class="end-dot">.</span></h1>
    <p class="lede">With our many years of experience in medical technology, we offer a comprehensive range of services tailored precisely to your requirements. From initial concept ideas and sound feasibility studies through strategic procurement to the detailed design of your clinic, we support you competently, reliably and efficiently in every project phase.</p>
  </div>
</section>

<section class="m-graphic-sec" style="background-image:url(/assets/slogan-bg.jpg)">
  <div class="m-shell">
    <div class="m-cross">
      <span class="m-cross-line v"></span>
      <span class="m-cross-line h"></span>

      <a class="m-cx-node n-top" href="#planung">
        <span class="m-hg-ring"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 38 L38 38 L10 12 Z"/><path d="M10 27 L21 27"/><circle cx="38" cy="38" r="4.4" class="sig-fill"/></svg></span>
        <span class="m-cx-label">Medical Technology Design</span>
      </a>

      <a class="m-cx-node n-right" href="#consulting">
        <span class="m-hg-ring"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 13 h26 a3 3 0 0 1 3 3 v13 a3 3 0 0 1 -3 3 H21 l-7 6 v-6 h-2 a3 3 0 0 1 -3 -3 V16 a3 3 0 0 1 3 -3 Z"/><circle cx="23" cy="22.5" r="4.2" class="sig-fill"/></svg></span>
        <span class="m-cx-label">Consulting</span>
      </a>

      <a class="m-cx-node n-bottom" href="#handel">
        <span class="m-hg-ring"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 8 L39 16 L39 32 L24 40 L9 32 L9 16 Z"/><path d="M9 16 L24 24 L39 16"/><path d="M24 24 L24 40"/><circle cx="24" cy="24" r="4.2" class="sig-fill"/></svg></span>
        <span class="m-cx-label">Procurement</span>
      </a>

      <a class="m-cx-node n-left" href="#pruefung">
        <span class="m-hg-ring"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="21" cy="21" r="11"/><path d="M29 29 L39 39"/><path d="M16.5 21.5 l3.5 3.5 l6.5 -7.5" class="sig-stroke" stroke-width="3.2"/></svg></span>
        <span class="m-cx-label">Inspection</span>
      </a>

      <div class="m-cross-center"><img src="/assets/m-logo.png" alt="medeqon" width="372" height="335"></div>
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
        <h2 class="m-svc2-title">Medical Technology Design &amp; construction supervision<span class="end-dot">.</span></h2>
        <p class="m-svc2-lead">From concept to completion – we bring your projects to life.</p>
        <p class="m-svc2-desc">In project work we support you as an equal partner from the very start. Clear structures and efficiently managed workflows save you time and resources. Our precise project management and high quality standards ensure on-time delivery, cost certainty and first-class results.</p>
        <ul class="m-svc2-list">
          <li>Delivery across service phases 1–9</li>
          <li>Design in 3D</li>
          <li>Active cost control</li>
          <li>Clear room books</li>
          <li>Project management</li>
        </ul>
      </article>
      <article class="m-svc2" id="consulting">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 13 h26 a3 3 0 0 1 3 3 v13 a3 3 0 0 1 -3 3 H21 l-7 6 v-6 h-2 a3 3 0 0 1 -3 -3 V16 a3 3 0 0 1 3 -3 Z"/><circle cx="23" cy="22.5" r="3.4" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">02</span>
        </div>
        <h2 class="m-svc2-title">Consulting<span class="end-dot">.</span></h2>
        <p class="m-svc2-lead">Strategies with substance – consulting backed by medical technology experience.</p>
        <p class="m-svc2-desc">We develop tailored solutions that fit technically, organisationally and economically. Our many years of experience in medical technology consulting combine expertise with practical implementation, optimising processes, reducing costs and creating sustainable results – today and tomorrow.</p>
        <ul class="m-svc2-list">
          <li>Needs analysis</li>
          <li>Goal definition</li>
          <li>Technical and economic assessment</li>
          <li>Strategic concept development</li>
          <li>Implementation support</li>
          <li>Training and knowledge transfer</li>
        </ul>
      </article>
    </div>

    <div class="m-cta-mid">
      <div class="m-shell m-cta-inner">
        <div class="line"></div>
        <h2>Work with us<span class="end-dot">.</span></h2>
        <p>Rely on precisely fitting solutions, competent advice and personal support – for successful projects and lasting results.</p>
        <a class="m-cta-link" href="/en/kontakt.html">Get in touch</a>
      </div>
    </div>

    <div class="m-svc2-grid">
      <article class="m-svc2" id="handel">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 8 L39 16 L39 32 L24 40 L9 32 L9 16 Z"/><path d="M9 16 L24 24 L39 16"/><path d="M24 24 L24 40"/><circle cx="24" cy="24" r="3.4" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">03</span>
        </div>
        <h2 class="m-svc2-title">Procurement<span class="end-dot">.</span></h2>
        <p class="m-svc2-lead">Quality that lasts. Solutions that pay off.</p>
        <p class="m-svc2-desc">We offer durable, low-maintenance medical products with low life-cycle costs. Individual solutions are tailored precisely to your needs – including personal advice and a partnership-based approach.</p>
        <ul class="m-svc2-list">
          <li>Product sourcing</li>
          <li>Selection advice</li>
          <li>Quality assurance</li>
          <li>Procurement and installation</li>
          <li>Cost-effectiveness analysis</li>
          <li>After-sales service</li>
          <li>Technical support</li>
        </ul>
      </article>
      <article class="m-svc2" id="pruefung">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="21" cy="21" r="11"/><path d="M29 29 L39 39"/><path d="M16.5 21.5 l3.5 3.5 l6.5 -7.5" class="sig-stroke" stroke-width="2.6"/></svg></span>
          <span class="m-svc2-num">04</span>
        </div>
        <h2 class="m-svc2-title">Inspection, repair and safety<span class="end-dot">.</span></h2>
        <p class="m-svc2-lead">Reliable technical service for maximum safety.</p>
        <p class="m-svc2-desc">Our mechatronics technicians ensure flawless medical technology equipment, legally compliant inspections and early recommendations – for minimal downtime and maximum safety. This keeps your medical technology ready for use at all times and meets the highest quality and safety standards.</p>
        <ul class="m-svc2-list">
          <li>Recurring inspections</li>
          <li>Inspection and repair per EN 6253</li>
          <li>Visual inspection and functional checks</li>
          <li>Repair and replacement recommendations</li>
          <li>Support with transfer into the asset register</li>
          <li>Traceable documentation</li>
        </ul>
      </article>
    </div>
  </div>
</section>'''

_LEIST_PL = [
    ("<span class=\"m-tag\">Services</span>", "<span class=\"m-tag\">Usługi</span>"),
    ("Our Services<span", "Nasze usługi<span"),
    ("With our many years of experience in medical technology, we offer a comprehensive range of services tailored precisely to your requirements. From initial concept ideas and sound feasibility studies through strategic procurement to the detailed design of your clinic, we support you competently, reliably and efficiently in every project phase.",
     "Dzięki wieloletniemu doświadczeniu w technice medycznej oferujemy kompleksowy zakres usług, dokładnie dopasowany do Państwa wymagań. Od pierwszych koncepcji i rzetelnych studiów wykonalności, poprzez strategiczne zaopatrzenie, aż po szczegółowe projektowanie Państwa kliniki – wspieramy Państwa kompetentnie, niezawodnie i efektywnie na każdym etapie projektu."),
    (">Medical Technology Design</span>", ">Projektowanie techniki medycznej</span>"),
    (">Consulting</span>", ">Doradztwo</span>"),
    (">Procurement</span>", ">Zaopatrzenie</span>"),
    (">Inspection</span>", ">Kontrola techniczna</span>"),
    ("Medical Technology Design &amp; construction supervision<span", "Projektowanie techniki medycznej i nadzór budowlany<span"),
    ("From concept to completion – we bring your projects to life.", "Od pomysłu do realizacji – urzeczywistniamy Państwa projekty."),
    ("In project work we support you as an equal partner from the very start. Clear structures and efficiently managed workflows save you time and resources. Our precise project management and high quality standards ensure on-time delivery, cost certainty and first-class results.",
     "W realizacji projektów towarzyszymy Państwu jako równorzędny partner od samego początku. Dzięki przejrzystym strukturom i sprawnie zarządzanym procesom oszczędzają Państwo czas i zasoby. Nasze precyzyjne zarządzanie projektem i wysokie standardy jakości zapewniają terminowość, pewność kosztów i pierwszorzędne wyniki."),
    ("<li>Delivery across service phases 1–9</li>", "<li>Realizacja w fazach usługowych 1–9</li>"),
    ("<li>Design in 3D</li>", "<li>Projektowanie w 3D</li>"),
    ("<li>Active cost control</li>", "<li>Aktywne zarządzanie kosztami</li>"),
    ("<li>Clear room books</li>", "<li>Przejrzyste książki pomieszczeń</li>"),
    ("<li>Project management</li>", "<li>Zarządzanie projektem</li>"),
    ("Consulting<span class=\"end-dot\">", "Doradztwo<span class=\"end-dot\">"),
    ("Strategies with substance – consulting backed by medical technology experience.", "Strategie z treścią – doradztwo poparte doświadczeniem w technice medycznej."),
    ("We develop tailored solutions that fit technically, organisationally and economically. Our many years of experience in medical technology consulting combine expertise with practical implementation, optimising processes, reducing costs and creating sustainable results – today and tomorrow.",
     "Opracowujemy rozwiązania szyte na miarę, które pasują pod względem technicznym, organizacyjnym i ekonomicznym. Nasze wieloletnie doświadczenie w doradztwie z zakresu techniki medycznej łączy wiedzę fachową z praktycznym wdrożeniem, optymalizuje procesy, obniża koszty i tworzy trwałe rezultaty – dziś i jutro."),
    ("<li>Needs analysis</li>", "<li>Analiza potrzeb</li>"),
    ("<li>Goal definition</li>", "<li>Definicja celów</li>"),
    ("<li>Technical and economic assessment</li>", "<li>Ocena techniczna i ekonomiczna</li>"),
    ("<li>Strategic concept development</li>", "<li>Strategiczne opracowanie koncepcji</li>"),
    ("<li>Implementation support</li>", "<li>Wsparcie przy wdrożeniu</li>"),
    ("<li>Training and knowledge transfer</li>", "<li>Szkolenia i transfer wiedzy</li>"),
    ("Work with us<span", "Współpracujmy<span"),
    ("Rely on precisely fitting solutions, competent advice and personal support – for successful projects and lasting results.",
     "Postawcie Państwo na precyzyjnie dopasowane rozwiązania, kompetentne doradztwo i osobistą opiekę – dla udanych projektów i trwałych rezultatów."),
    ("/en/kontakt.html\">Get in touch</a>", "/pl/kontakt.html\">Skontaktuj się</a>"),
    ("Procurement<span class=\"end-dot\">", "Zaopatrzenie<span class=\"end-dot\">"),
    ("Quality that lasts. Solutions that pay off.", "Jakość, która trwa. Rozwiązania, które się opłacają."),
    ("We offer durable, low-maintenance medical products with low life-cycle costs. Individual solutions are tailored precisely to your needs – including personal advice and a partnership-based approach.",
     "Oferujemy trwałe, niewymagające konserwacji wyroby medyczne o niskich kosztach cyklu życia. Indywidualne rozwiązania są dokładnie dopasowane do Państwa potrzeb – w tym osobiste doradztwo i partnerska współpraca."),
    ("<li>Product sourcing</li>", "<li>Pozyskiwanie produktów</li>"),
    ("<li>Selection advice</li>", "<li>Doradztwo w doborze</li>"),
    ("<li>Quality assurance</li>", "<li>Zapewnienie jakości</li>"),
    ("<li>Procurement and installation</li>", "<li>Zaopatrzenie i montaż</li>"),
    ("<li>Cost-effectiveness analysis</li>", "<li>Analiza opłacalności</li>"),
    ("<li>After-sales service</li>", "<li>Serwis posprzedażny</li>"),
    ("<li>Technical support</li>", "<li>Wsparcie techniczne</li>"),
    ("Inspection, repair and safety<span", "Kontrola, naprawa i bezpieczeństwo<span"),
    ("Reliable technical service for maximum safety.", "Niezawodny serwis techniczny dla maksymalnego bezpieczeństwa."),
    ("Our mechatronics technicians ensure flawless medical technology equipment, legally compliant inspections and early recommendations – for minimal downtime and maximum safety. This keeps your medical technology ready for use at all times and meets the highest quality and safety standards.",
     "Nasi mechatronicy zapewniają nienaganne działanie urządzeń techniki medycznej, kontrole zgodne z prawem oraz wczesne zalecenia – dla minimalnych przestojów i maksymalnego bezpieczeństwa. Dzięki temu Państwa technika medyczna pozostaje zawsze gotowa do użytku i spełnia najwyższe standardy jakości i bezpieczeństwa."),
    ("<li>Recurring inspections</li>", "<li>Badania okresowe</li>"),
    ("<li>Inspection and repair per EN 6253</li>", "<li>Kontrola i naprawa wg EN 6253</li>"),
    ("<li>Visual inspection and functional checks</li>", "<li>Oględziny i kontrola sprawności działania</li>"),
    ("<li>Repair and replacement recommendations</li>", "<li>Zalecenia dotyczące napraw i wymiany</li>"),
    ("<li>Support with transfer into the asset register</li>", "<li>Wsparcie przy wpisie do rejestru środków trwałych</li>"),
    ("<li>Traceable documentation</li>", "<li>Przejrzysta dokumentacja</li>"),
]

_LEIST_RO = [
    ("<span class=\"m-tag\">Services</span>", "<span class=\"m-tag\">Servicii</span>"),
    ("Our Services<span", "Serviciile noastre<span"),
    ("With our many years of experience in medical technology, we offer a comprehensive range of services tailored precisely to your requirements. From initial concept ideas and sound feasibility studies through strategic procurement to the detailed design of your clinic, we support you competently, reliably and efficiently in every project phase.",
     "Cu experiența noastră îndelungată în tehnologia medicală, oferim o gamă completă de servicii, adaptată exact cerințelor dumneavoastră. De la primele idei conceptuale și studii de fezabilitate solide, prin achiziția strategică, până la proiectarea detaliată a clinicii dumneavoastră – vă sprijinim competent, fiabil și eficient în fiecare fază a proiectului."),
    (">Medical Technology Design</span>", ">Proiectarea tehnologiei medicale</span>"),
    (">Consulting</span>", ">Consultanță</span>"),
    (">Procurement</span>", ">Achiziții</span>"),
    (">Inspection</span>", ">Verificare tehnică</span>"),
    ("Medical Technology Design &amp; construction supervision<span", "Proiectarea tehnologiei medicale și supravegherea execuției<span"),
    ("From concept to completion – we bring your projects to life.", "De la idee la realizare – dăm viață proiectelor dumneavoastră."),
    ("In project work we support you as an equal partner from the very start. Clear structures and efficiently managed workflows save you time and resources. Our precise project management and high quality standards ensure on-time delivery, cost certainty and first-class results.",
     "În derularea proiectelor vă însoțim ca partener egal încă de la început. Prin structuri clare și fluxuri de lucru gestionate eficient economisiți timp și resurse. Managementul nostru precis al proiectelor și standardele înalte de calitate asigură respectarea termenelor, siguranța costurilor și rezultate de primă clasă."),
    ("<li>Delivery across service phases 1–9</li>", "<li>Derulare pe fazele de servicii 1–9</li>"),
    ("<li>Design in 3D</li>", "<li>Proiectare în 3D</li>"),
    ("<li>Active cost control</li>", "<li>Controlul activ al costurilor</li>"),
    ("<li>Clear room books</li>", "<li>Registre de încăperi clare</li>"),
    ("<li>Project management</li>", "<li>Managementul proiectului</li>"),
    ("Consulting<span class=\"end-dot\">", "Consultanță<span class=\"end-dot\">"),
    ("Strategies with substance – consulting backed by medical technology experience.", "Strategii cu substanță – consultanță susținută de experiență în tehnologia medicală."),
    ("We develop tailored solutions that fit technically, organisationally and economically. Our many years of experience in medical technology consulting combine expertise with practical implementation, optimising processes, reducing costs and creating sustainable results – today and tomorrow.",
     "Dezvoltăm soluții personalizate care se potrivesc tehnic, organizatoric și economic. Experiența noastră îndelungată în consultanța de tehnologie medicală îmbină expertiza cu implementarea practică, optimizează procesele, reduce costurile și creează rezultate durabile – astăzi și mâine."),
    ("<li>Needs analysis</li>", "<li>Analiza necesităților</li>"),
    ("<li>Goal definition</li>", "<li>Definirea obiectivelor</li>"),
    ("<li>Technical and economic assessment</li>", "<li>Evaluare tehnică și economică</li>"),
    ("<li>Strategic concept development</li>", "<li>Dezvoltarea conceptului strategic</li>"),
    ("<li>Implementation support</li>", "<li>Sprijin la implementare</li>"),
    ("<li>Training and knowledge transfer</li>", "<li>Instruire și transfer de cunoștințe</li>"),
    ("Work with us<span", "Lucrați cu noi<span"),
    ("Rely on precisely fitting solutions, competent advice and personal support – for successful projects and lasting results.",
     "Bazați-vă pe soluții perfect adaptate, consultanță competentă și asistență personală – pentru proiecte reușite și rezultate durabile."),
    ("/en/kontakt.html\">Get in touch</a>", "/ro/kontakt.html\">Contactați-ne</a>"),
    ("Procurement<span class=\"end-dot\">", "Achiziții<span class=\"end-dot\">"),
    ("Quality that lasts. Solutions that pay off.", "Calitate care rezistă. Soluții care merită."),
    ("We offer durable, low-maintenance medical products with low life-cycle costs. Individual solutions are tailored precisely to your needs – including personal advice and a partnership-based approach.",
     "Oferim produse medicale durabile, cu întreținere redusă și costuri scăzute pe durata ciclului de viață. Soluțiile individuale sunt adaptate exact nevoilor dumneavoastră – inclusiv consultanță personală și o colaborare de tip parteneriat."),
    ("<li>Product sourcing</li>", "<li>Identificarea produselor</li>"),
    ("<li>Selection advice</li>", "<li>Consultanță la selecție</li>"),
    ("<li>Quality assurance</li>", "<li>Asigurarea calității</li>"),
    ("<li>Procurement and installation</li>", "<li>Achiziție și instalare</li>"),
    ("<li>Cost-effectiveness analysis</li>", "<li>Analiza rentabilității</li>"),
    ("<li>After-sales service</li>", "<li>Servicii post-vânzare</li>"),
    ("<li>Technical support</li>", "<li>Asistență tehnică</li>"),
    ("Inspection, repair and safety<span", "Verificare, reparare și siguranță<span"),
    ("Reliable technical service for maximum safety.", "Serviciu tehnic fiabil pentru siguranță maximă."),
    ("Our mechatronics technicians ensure flawless medical technology equipment, legally compliant inspections and early recommendations – for minimal downtime and maximum safety. This keeps your medical technology ready for use at all times and meets the highest quality and safety standards.",
     "Mecatroniștii noștri asigură echipamente de tehnologie medicală impecabile, verificări conforme legal și recomandări timpurii – pentru timpi de nefuncționare minimi și siguranță maximă. Astfel, tehnologia dumneavoastră medicală rămâne oricând gata de utilizare și îndeplinește cele mai înalte standarde de calitate și siguranță."),
    ("<li>Recurring inspections</li>", "<li>Verificări periodice</li>"),
    ("<li>Inspection and repair per EN 6253</li>", "<li>Verificare și reparare conform EN 6253</li>"),
    ("<li>Visual inspection and functional checks</li>", "<li>Inspecție vizuală și verificarea funcționării</li>"),
    ("<li>Repair and replacement recommendations</li>", "<li>Recomandări de reparare și înlocuire</li>"),
    ("<li>Support with transfer into the asset register</li>", "<li>Sprijin la înregistrarea în registrul de inventar</li>"),
    ("<li>Traceable documentation</li>", "<li>Documentație trasabilă</li>"),
]

CHEV ='<svg class="m-ac-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'

# ---- Produktkarten (Medizinische Einrichtung) aus products.json generieren ----
import json, html as _html, glob as _glob
_products = json.loads((ROOT / "products.json").read_text(encoding="utf-8"))

# ---- Produkt-i18n: übersetzte Datensätze (Modell/Beschreibung/Specs) je Sprache ----
_PROD_TR = {"en": {}, "pl": {}, "ro": {}}
for _L in ("en", "pl", "ro"):
    for _srcname in ("products", "kenex", "strahlenschutz", "heilbehelfe"):
        _pf = ROOT / "i18n" / f"prod_{_srcname}_{_L}.json"
        if _pf.exists():
            _PROD_TR[_L].update(json.loads(_pf.read_text(encoding="utf-8")))

_PUIT_MISS = set()

def _prodt(lang, p):
    """Übersetzten Datensatz (model/description/specs) liefern; sonst Original."""
    if lang == "de":
        return p["model"], p.get("description", ""), p.get("specs", [])
    t = _PROD_TR.get(lang, {}).get(p["slug"])
    if not t:
        print(f"  WARN [PROD {lang}] Produkt nicht übersetzt: {p['slug']!r}")
        return p["model"], p.get("description", ""), p.get("specs", [])
    return t.get("model", p["model"]), t.get("description", p.get("description", "")), t.get("specs", p.get("specs", []))

def _puit(lang, s):
    """Produkt-UI-Übersetzung (Überschriften/Labels). Fallback = Original."""
    if lang == "de" or not s:
        return s
    m = _PUI.get(lang, {})
    if s in m:
        return m[s]
    _PUIT_MISS.add((lang, s))
    return s

_PL_VIEW = {"en": "View", "pl": "Widok", "ro": "Vedere"}

def _gallery(p, lang="de"):
    imgs = sorted(_glob.glob(str(ROOT / "assets" / "produkte" / p["slug"] / "*.jpg")))
    n = len(imgs) or 1
    model_raw = _prodt(lang, p)[0]
    model = _html.escape(model_raw)
    view = _PL_VIEW.get(lang, "Ansicht")
    shots = []
    for i in range(1, n + 1):
        cls = "m-pl-shot is-on" if i == 1 else "m-pl-shot"
        alt = model if i == 1 else f"{model} – {view} {i}"
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
def _render_liege(p, lang="de"):
    model, desc, specrows = _prodt(lang, p)
    specs = "\n".join(
        f'                        <li><span>{_html.escape(k)}</span>{_html.escape(v)}</li>'
        for k, v in specrows)
    return (
'                  <article class="m-pl">\n'
+ _gallery(p, lang) + '\n'
'                    <div class="m-pl-info">\n'
+ (f'                      <span class="m-pl-ref">Ref. {_html.escape(p["ref"])}</span>\n' if p.get("ref") else '')
+ f'                      <h4 class="m-pl-name">{_html.escape(model)}</h4>\n'
f'                      <p class="m-pl-desc">{_html.escape(desc)}</p>\n'
'                      <ul class="m-pl-specs">\n'
f'{specs}\n'
'                      </ul>\n'
'                    </div>\n'
'                  </article>')
def _cards(cat, lang="de"):
    return "\n\n".join(_render_liege(p, lang) for p in _products if p["cat"] == cat)
def _count(cat):
    return sum(1 for p in _products if p["cat"] == cat)
CARDS = {c: _cards(c) for c in ("chiro", "elektrisch", "hydraulisch", "fix", "stuehle", "sichtschutz", "mrt", "wagen", "station", "gvw", "btisch", "trans")}

# ---- Heilbehelfe & Hilfsmittel ----
_hb = json.loads((ROOT / "heilbehelfe.json").read_text(encoding="utf-8"))
def _hb_cards(sub, group=None, lang="de"):
    return "\n\n".join(_render_liege(p, lang) for p in _hb
                       if p["sub"] == sub and (group is None or p.get("group") == group))
def _hb_count(sub):
    return sum(1 for p in _hb if p["sub"] == sub)

# ---- Strahlenschutz (ROTHBAND) ----
_ss = json.loads((ROOT / "strahlenschutz.json").read_text(encoding="utf-8"))
def _ss_cards(sub, lang="de"):
    return "\n\n".join(_render_liege(p, lang) for p in _ss if p["sub"] == sub)
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
def _optionen_html(lang="de"):
    out = []
    for group, items in _OPTIONEN:
        tiles = []
        for key, title, desc in items:
            t_title = _puit(lang, title); t_desc = _puit(lang, desc)
            tiles.append(
'                    <figure class="m-opt">\n'
f'                      <div class="m-opt-img"><img src="assets/optionen/{key}.jpg" alt="{_html.escape(t_title)}" loading="lazy"></div>\n'
'                      <figcaption class="m-opt-body">\n'
f'                        <h4 class="m-opt-title">{_html.escape(t_title)}</h4>\n'
f'                        <p class="m-opt-desc">{_html.escape(t_desc)}</p>\n'
'                      </figcaption>\n'
'                    </figure>')
        out.append(
'                <div class="m-opt-group">\n'
f'                  <div class="m-opt-grouptitle">{_html.escape(_puit(lang, group))}</div>\n'
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
def _farben_html(lang="de"):
    out = []
    for group, items in _FARBEN:
        tiles = []
        for key, name in items:
            t_name = _puit(lang, name)
            tiles.append(
'                    <figure class="m-sw">\n'
f'                      <div class="m-sw-img"><img src="assets/farben/{key}.jpg" alt="{_html.escape(t_name)}" loading="lazy"></div>\n'
f'                      <figcaption class="m-sw-name">{_html.escape(t_name)}</figcaption>\n'
'                    </figure>')
        out.append(
'                <div class="m-opt-group">\n'
f'                  <div class="m-opt-grouptitle">{_html.escape(_puit(lang, group))}</div>\n'
'                  <div class="m-sw-grid">\n'
+ "\n".join(tiles) + '\n'
'                  </div>\n'
'                </div>')
    return "\n".join(out)

# ---- Montierter Strahlenschutz (KENEX) ----
_kenex = json.loads((ROOT / "kenex.json").read_text(encoding="utf-8"))
def _kenex_cards(cat, sub=None, lang="de"):
    return "\n\n".join(_render_liege(p, lang) for p in _kenex
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

def _dl_card(item, lang="de"):
    icon = _DL_ICONS.get(item.get("icon", "doc"), _DL_ICONS["doc"])
    title = _html.escape(_puit(lang, item["title"]))
    meta = _html.escape(_puit(lang, item.get("meta", "PDF-Dokument")))
    langs = item.get("langs")
    f = item.get("file")
    if langs:
        btns = "\n".join(
            f'                        <a class="m-dl-lang" href="{fp}" download aria-label="{title} ({lb}) herunterladen"><span class="m-dl-lc">{lb}</span>{_DL_DOWNLOAD}</a>'
            for lb, fp in langs)
        action = '<span class="m-dl-langs">\n' + btns + '\n                      </span>'
        soon = ""
    elif f:
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

def _downloads_category(num, cid, lead, groups, note=None, lang="de"):
    parts = [
'      <details class="m-ac" id="' + cid + '">\n'
'        <summary><span class="m-ac-num">' + num + '</span><span class="m-ac-title">' + _puit(lang, "Downloads &amp; Unterlagen") + '</span>' + CHEV + '</summary>\n'
'        <div class="m-ac-body">\n']
    if lead:
        parts.append('          <p class="m-ac-lead">' + _puit(lang, lead) + '</p>\n')
    parts.append('          <div class="m-dl-wrap">')
    for group, items in groups:
        parts.append(
'            <div class="m-dl-group">\n'
f'              <div class="m-dl-grouptitle">{_html.escape(_puit(lang, group))}</div>\n'
'              <div class="m-dl-grid">\n'
+ "\n".join(_dl_card(it, lang) for it in items) + '\n'
'              </div>\n'
'            </div>')
    if note is not None:
        note_p = ('              <p>' + _puit(lang, note) + '</p>\n') if note else ''
        parts.append(
'            <div class="m-dl-note">\n'
+ note_p +
'              <a class="m-dl-note-btn" href="kontakt.html">' + _puit(lang, "Zur Kontaktseite") + '</a>\n'
'            </div>')
    parts.append(
'          </div>\n'
'        </div>\n'
'      </details>')
    return "\n".join(parts)

_DL_LEAD = ("Hier stellen wir Ihnen Unterlagen zum Herunterladen bereit &ndash; "
            "Herstellerkataloge, technische Datenblätter, Produktinformationen sowie "
            "CE- und Konformitätszertifikate. Neue Dokumente ergänzen wir laufend.")

_DL_LEAD_SS = ("Hier finden Sie unsere Produktkataloge und Unterlagen zu unseren Produkten "
               "des Strahlenschutzes. Neue Dokumente ergänzen wir laufend.")

_DL_LEAD_HB = ("Herstellerkataloge, Datenblätter, Produktinformationen und Zertifikate "
               "zu unseren Heilbehelfen und Hilfsmitteln.")

_DL_NOTE_REQUEST = ("Weitere Kataloge und Unterlagen &ndash; Datenblätter, "
                    "Produktinformationen und Zertifikate &ndash; übermitteln wir Ihnen "
                    "gerne auf Anfrage.")

_DL_NOTE_SS = ("Weitere Sprachversionen des Katalogs (Englisch, Polnisch) sowie "
               "Datenblätter, Produktinformationen und Zertifikate übermitteln wir Ihnen "
               "gerne auf Anfrage.")

_DL_NOTE_ANFRAGE_SS = ("Die Unterlagen zu unseren Produkten des Strahlenschutzes senden "
                       "wir Ihnen gerne auf Anfrage zu.")

_DL_NOTE_ANFRAGE_HB = ("Die Unterlagen zu unseren Heilbehelfen und Hilfsmitteln senden "
                       "wir Ihnen gerne auf Anfrage zu.")

_DL_NOTE_ANFRAGE_MED = ("Die Unterlagen zu unseren Produkten der Medizinischen Einrichtung "
                        "senden wir Ihnen gerne auf Anfrage zu.")

_DL_LEAD_MED = ("Hier finden Sie unsere Produktkataloge und Farbkarten sowie die technischen "
                "Datenblätter zu unseren Produkten der Medizinischen Einrichtung. Der "
                "COINFYCARE-Katalog deckt die Bereiche 01–03 ab, der TECH-MED-Katalog samt "
                "Farbkarten die Bereiche 04–09 einschließlich Schienensysteme. "
                "Neue Dokumente ergänzen wir laufend.")

_DL_LEAD_MED_REQUEST = ("Die Unterlagen zu unseren Produkten der Medizinischen Einrichtung "
                        "senden wir Ihnen gerne auf Anfrage zu.")

_DL_NOTE_MED_REQUEST = ("Kontaktieren Sie uns &ndash; wir übermitteln Ihnen Datenblätter, "
                        "Produktinformationen und Zertifikate zu unseren Produkten der "
                        "Medizinischen Einrichtung umgehend.")

# --- Datasheet download area (Datenblätter only), grouped like the product catalogue ---
_MODEL2PROD = {p["model"]: p for p in _products}

_DS_WORD = {"de": "Datenblatt", "en": "Data sheet", "pl": "Karta techniczna", "ro": "Fișă tehnică"}
_DS_NO_PL = set()  # Modelle ohne PL-Datenblatt (nur DE/EN); aktuell keine
def _ds_card(model, lang="de"):
    p = _MODEL2PROD.get(model, {})
    title = _html.escape(model)
    ref = p.get("ref", "")
    dw = _DS_WORD.get(lang, "Datenblatt")
    mn = model.replace(" ", "_")
    langbtns = [("DE", "Datenblatt_", "Deutsch", "Datenblatt"),
                ("EN", "DataSheet_", "English", "Data sheet")]
    if model not in _DS_NO_PL:
        langbtns.append(("PL", "KartaTechniczna_", "Polski", "Karta techniczna"))
    codes = " / ".join(lb for lb, _p, _n, _w in langbtns)
    meta = ("Ref. " + ref + " · " + dw + " · " + codes) if ref else (dw + " · " + codes)
    meta = _html.escape(meta)
    icon = _DL_ICONS["doc"]
    btns = "\n".join(
        f'                          <a class="m-dl-lang" href="assets/downloads/med/{pre}{mn}.pdf" download aria-label="{word} {title} ({lname}) herunterladen"><span class="m-dl-lc">{lb}</span>{_DL_DOWNLOAD}</a>'
        for (lb, pre, lname, word) in langbtns)
    return (
'                      <figure class="m-dl-card">\n'
f'                        <span class="m-dl-ic">{icon}</span>\n'
'                        <span class="m-dl-main">\n'
f'                          <span class="m-dl-title">{title}</span>\n'
f'                          <span class="m-dl-meta">{meta}</span>\n'
'                        </span>\n'
'                        <span class="m-dl-langs">\n'
+ btns + '\n'
'                        </span>\n'
'                      </figure>')

def _downloads_datasheets(num, cid, lead, cats, note=None, lang="de", catalog=None):
    parts = [
'      <details class="m-ac" id="' + cid + '">\n'
'        <summary><span class="m-ac-num">' + num + '</span><span class="m-ac-title">' + _puit(lang, "Downloads &amp; Unterlagen") + '</span>' + CHEV + '</summary>\n'
'        <div class="m-ac-body">\n'
'          <p class="m-ac-lead">' + _puit(lang, lead) + '</p>\n'
'          <div class="m-dl-wrap">']
    if catalog:
        parts.append(
'            <div class="m-dl-group">\n'
'              <div class="m-dl-grouptitle">' + _html.escape(_puit(lang, "Produktkataloge & Farbkarten")) + '</div>\n'
'              <div class="m-dl-grid">\n'
+ "\n".join(_dl_card(it, lang) for it in catalog) + '\n'
'              </div>\n'
'            </div>')
    for cnum, ctitle, subs in cats:
        parts.append(
'            <div class="m-dl-cat">\n'
'              <div class="m-dl-cat-head"><span class="m-dl-catnum">' + cnum + '</span>'
'<span class="m-dl-cat-title">' + _html.escape(_puit(lang, ctitle)) + '</span></div>')
        for subtitle, models in subs:
            if subtitle:
                parts.append('              <div class="m-dl-sub">' + _html.escape(_puit(lang, subtitle)) + '</div>')
            parts.append(
'              <div class="m-dl-grid">\n'
+ "\n".join(_ds_card(m, lang) for m in models) + '\n'
'              </div>')
        parts.append('            </div>')
    if note:
        parts.append(
'            <div class="m-dl-note">\n'
'              <p>' + _puit(lang, note) + '</p>\n'
'              <a class="m-dl-note-btn" href="kontakt.html">' + _puit(lang, "Zur Kontaktseite") + '</a>\n'
'            </div>')
    parts.append(
'          </div>\n'
'        </div>\n'
'      </details>')
    return "\n".join(parts)

def _downloads_cat_cards(num, cid, lead, cats, note=None, lang="de"):
    """Wie _downloads_datasheets (nummerierte Kategorien mit Unterüberschriften),
    aber mit Katalog-/Karten-Einträgen (_dl_card) statt Datenblatt-Karten."""
    parts = [
'      <details class="m-ac" id="' + cid + '">\n'
'        <summary><span class="m-ac-num">' + num + '</span><span class="m-ac-title">' + _puit(lang, "Downloads &amp; Unterlagen") + '</span>' + CHEV + '</summary>\n'
'        <div class="m-ac-body">\n'
'          <p class="m-ac-lead">' + _puit(lang, lead) + '</p>\n'
'          <div class="m-dl-wrap">']
    for cnum, ctitle, subs in cats:
        parts.append(
'            <div class="m-dl-cat">\n'
'              <div class="m-dl-cat-head"><span class="m-dl-catnum">' + cnum + '</span>'
'<span class="m-dl-cat-title">' + _html.escape(_puit(lang, ctitle)) + '</span></div>')
        for subtitle, items in subs:
            if subtitle:
                parts.append('              <div class="m-dl-sub">' + _html.escape(_puit(lang, subtitle)) + '</div>')
            parts.append(
'              <div class="m-dl-grid">\n'
+ "\n".join(_dl_card(it, lang) for it in items) + '\n'
'              </div>')
        parts.append('            </div>')
    if note:
        parts.append(
'            <div class="m-dl-note">\n'
'              <p>' + _puit(lang, note) + '</p>\n'
'              <a class="m-dl-note-btn" href="kontakt.html">' + _puit(lang, "Zur Kontaktseite") + '</a>\n'
'            </div>')
    parts.append(
'          </div>\n'
'        </div>\n'
'      </details>')
    return "\n".join(parts)

DL_MED_CATS = [
    ("01", "Untersuchungsliegen", [
        ("Fix", ["FIX"]),
        ("Hydraulisch", ["KEND PRO", "LING PRO", "MAIT PRO", "TENB PRO"]),
        ("Elektrisch", ["ENID PRO", "ENID", "GUTH PRO", "GUTH", "ROTH", "RILA PRO",
                        "RILA", "JULL PRO", "BROM PRO", "BROM", "NOTT PRO", "NOTT",
                        "GALLEY", "STILL", "PEHR PRO", "PEHR", "BOBATH", "BATEC", "TILT"]),
        ("Chiropraktisch", ["ALMA PRO", "APPA", "SCALL PRO", "SIDO PRO"]),
    ]),
    ("02", "Medizinische Stühle", [
        (None, ["DISK", "DISK PRO", "RIDE", "RIDE PRO", "RIDE FR", "CORE", "SUPP",
                "XTRACT", "ENT", "OB", "PODO", "NOBU"]),
    ]),
    ("03", "Sichtschutz", [
        (None, ["ALU SCREEN 1518"]),
    ]),
]

# --- Produktkataloge & Farbkarten Medizinische Einrichtung für den Download-Bereich ---
# Bereiche 01–03 (COINFYCARE): eigener Katalog, DE/EN/PL.
# Bereiche 04–09 (TECH-MED): eigener Katalog + Farbkarten, DE/EN/PL/RO.
_MEDK = "assets/downloads/med/"
def _med4(base):
    return [(lb, _MEDK + base + "_" + lb + ".pdf") for lb in ("DE", "EN", "PL", "RO")]

DL_MED_CATALOG = [
    {"title": "Produktkatalog · Bereiche 01–03",
     "meta": "COINFYCARE · PDF", "icon": "book",
     "langs": [("DE", _MEDK + "Katalog_Medizinische_Einrichtung_DE.pdf"),
               ("EN", _MEDK + "Catalogue_Medical_Furnishing_EN.pdf"),
               ("PL", _MEDK + "Katalog_Wyposazenie_medyczne_PL.pdf")]},
    {"title": "Produktkatalog · Bereiche 04–09",
     "meta": "TECH-MED · PDF", "icon": "book",
     "langs": _med4("Katalog_TECHMED")},
    {"title": "Farbkarten · Bereiche 04–09",
     "meta": "TECH-MED · PDF", "icon": "doc",
     "langs": _med4("Farbkarten_TECHMED")},
]

_SSK = "assets/downloads/ss/"
def _cat3(base):
    return [("DE", _SSK + base + "_DE.pdf"), ("EN", _SSK + base + "_EN.pdf"), ("PL", _SSK + base + "_PL.pdf")]
# Strahlenschutz-Download: nummerierte Kategorien wie die Produktbereiche oben.
# Struktur je Kategorie: (Nummer, Titel, [(Unterüberschrift|None, [Karten]), ...])
DL_SS = [
    ("01/02", "Persönliche Schutzausrüstung und Aufbewahrung", [
        (None, [
            {"title": "Persönliche Schutzausrüstung", "meta": "ROTHBAND · PDF", "icon": "book",
             "langs": _cat3("Katalog_PSA_ROTHBAND")},
            {"title": "Schnittbildgebung", "meta": "ROTHBAND · PDF", "icon": "book",
             "langs": _cat3("Katalog_Schnittbildgebung_ROTHBAND")},
            {"title": "Strahlenschutzbrillen", "meta": "ROTHBAND · PDF", "icon": "book",
             "langs": _cat3("Katalog_Strahlenschutzbrillen_ROTHBAND")},
            {"title": "Zubehör", "meta": "ROTHBAND · PDF", "icon": "book",
             "langs": _cat3("Katalog_Zubehoer_ROTHBAND")},
        ]),
        ("Innenmaterial der persönlichen Schutzausrüstung", [
            {"title": "OUTLAST®", "meta": "ROTHBAND · PDF", "icon": "doc",
             "langs": _cat3("OUTLAST_Innenmaterial")},
        ]),
    ]),
    ("03", "Mobiler Strahlenschutz", [
        (None, [
            {"title": "Produktkatalog", "meta": "KENEX · PDF", "icon": "book",
             "langs": _cat3("Katalog_Mobiler_Strahlenschutz")},
        ]),
    ]),
    ("04", "Deckenmontierter Strahlenschutz", [
        (None, [
            {"title": "Produktkatalog", "meta": "KENEX · PDF", "icon": "book",
             "langs": _cat3("Katalog_Deckenmontierter_Strahlenschutz")},
        ]),
    ]),
    ("05", "Tischmontierter Strahlenschutz", [
        (None, [
            {"title": "Produktkatalog", "meta": "KENEX · PDF", "icon": "book",
             "langs": _cat3("Katalog_Tischmontierter_Strahlenschutz")},
        ]),
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

DL_HB = []

# ===================== Flyer-Sektion (Startseite + Produkte) =====================
# PDFs und Titelbilder liegen in assets/downloads/flyer/:
#   Flyer_<slug>_medeqon_<DE|EN|PL|RO>.pdf   und   cover_<slug>_<de|en|pl|ro>.jpg
_FLYERS = [
    ("planung",                  4, {"de": "Medizintechnik-Planung",
                                     "en": "Medical Technology Design",
                                     "pl": "Projektowanie techniki medycznej",
                                     "ro": "Proiectarea tehnologiei medicale"}),
    ("produktuebersicht",        2, {"de": "Produktübersicht",
                                     "en": "Product overview",
                                     "pl": "Przegląd produktów",
                                     "ro": "Prezentare produse"}),
    ("strahlenschutz",           2, {"de": "Strahlenschutz",
                                     "en": "Radiation protection",
                                     "pl": "Ochrona radiologiczna",
                                     "ro": "Protecție la radiații"}),
    ("medizinische-einrichtung", 2, {"de": "Medizinische Einrichtung",
                                     "en": "Medical furnishing",
                                     "pl": "Wyposażenie medyczne",
                                     "ro": "Mobilier medical"}),
]
_FLY_T = {
 "de": dict(tag="Flyer & Unterlagen", h2="Ihr Überblick zum Mitnehmen",
            lede="Ob Neubau, Umbau oder Neuausstattung: Auf wenigen Seiten sehen Sie, was Sie von uns erwarten "
                 "können – eine Medizintechnik-Planung, die Kosten früh sichtbar macht und Termine hält, und ein "
                 "Produktprogramm zertifizierter Hersteller, mit dem wir ganze Bereiche ausstatten. Kompakt "
                 "aufbereitet, sofort verständlich und ideal zum Weitergeben an Bauherren, Architekten und Einkauf.",
            pages="Seiten", open="ansehen", dl="herunterladen", pdf="PDF"),
 "en": dict(tag="Flyers & documents", h2="Your overview to take away",
            lede="New build, refurbishment or re-equipment: a few pages show what you can expect from us – Medical "
                 "Technology Design that makes costs visible early and keeps to schedule, and a range of products "
                 "from certified manufacturers with which we equip entire areas. Concise, immediately clear and "
                 "ideal for passing on to clients, architects and procurement.",
            pages="pages", open="view", dl="download", pdf="PDF"),
 "pl": dict(tag="Ulotki i materiały", h2="Przegląd, który weźmiesz ze sobą",
            lede="Nowa budowa, przebudowa czy ponowne wyposażenie: na kilku stronach zobaczysz, czego możesz od nas "
                 "oczekiwać – projektowanie techniki medycznej, które wcześnie uwidacznia koszty i pilnuje terminów, "
                 "oraz asortyment certyfikowanych producentów, którym wyposażamy całe obszary. Zwięźle, zrozumiale "
                 "i idealnie do przekazania inwestorom, architektom i działom zakupów.",
            pages="stron", open="zobacz", dl="pobierz", pdf="PDF"),
 "ro": dict(tag="Pliante și documente", h2="Imaginea de ansamblu, pe scurt",
            lede="Construcție nouă, modernizare sau reechipare: în doar câteva pagini vedeți ce puteți aștepta de la "
                 "noi – o proiectare a tehnologiei medicale care face costurile vizibile din timp și respectă "
                 "termenele, precum și o gamă de produse de la producători certificați cu care dotăm zone întregi. "
                 "Concis, ușor de înțeles și ideal de transmis beneficiarilor, arhitecților și departamentelor de "
                 "achiziții.",
            pages="pagini", open="vizualizare", dl="descărcare", pdf="PDF"),
}

def _flyer_section(lang="de", sid="flyer"):
    t = _FLY_T[lang]
    ap = "assets/" if lang == "de" else "/assets/"
    cards = []
    for slug, pages, titles in _FLYERS:
        title = _html.escape(titles[lang])
        pdf = f'{ap}downloads/flyer/Flyer_{slug}_medeqon_{lang.upper()}.pdf'
        cover = f'{ap}downloads/flyer/cover_{slug}_{lang}.jpg'
        cards.append(
'        <figure class="m-fly">\n'
f'          <a class="m-fly-cover" href="{pdf}" target="_blank" rel="noopener" aria-label="{title} – {t["open"]}">\n'
f'            <img src="{cover}" alt="{title}" width="646" height="914" loading="lazy">\n'
'          </a>\n'
'          <figcaption class="m-fly-foot">\n'
'            <span class="m-fly-txt">\n'
f'              <span class="m-fly-title">{title}</span>\n'
f'              <span class="m-fly-meta">{t["pdf"]} &middot; {pages} {t["pages"]}</span>\n'
'            </span>\n'
f'            <a class="m-dl-btn" href="{pdf}" download aria-label="{title} – {t["dl"]}">{_DL_DOWNLOAD}</a>\n'
'          </figcaption>\n'
'        </figure>')
    return (
f'<section class="m-graphic-sec m-fly-sec" id="{sid}" style="background-image:url({ap}slogan-bg.jpg)">\n'
'  <div class="m-shell">\n'
'    <div class="m-fly-head">\n'
f'      <span class="m-tag">{t["tag"]}</span>\n'
f'      <h2 class="m-bigH">{t["h2"]}<span class="end-dot">.</span></h2>\n'
f'      <p class="lede">{t["lede"]}</p>\n'
'    </div>\n'
'    <div class="m-fly-grid">\n'
+ "\n".join(cards) + '\n'
'    </div>\n'
'  </div>\n'
'</section>')

def _inject_flyer(body, lang):
    return body.replace("<!--FLYER-->", _flyer_section(lang))

# ===================== Partner-Sektion (Startseite) =====================
# Logos liegen als freigestellte PNGs in assets/brands/<slug>.png.
# Die Anzeigehöhe je Logo steuert `.m-part--<slug> .m-part-logo img` in styles.css.
_PARTNERS = [
    ("hersteller", [
        ("coinfycare", "COINFYCARE",    "https://www.coinfycare.com/en"),
        ("techmed",    "TECHMED",       "https://en.techmed.com.pl/"),
        ("mobiak",     "MOBIAK",        "https://www.mobiak.com/en/"),
        ("elers",      "ELERS MEDICAL", "https://elers.com"),
        ("rothband",   "ROTHBAND",      "https://www.rothband.com/de"),
        ("kenex",      "KENEX",         "https://www.kenex.co.uk"),
    ]),
    ("planung", [
        ("plandata",   "PLANDATA",      "https://plandata.eu"),
    ]),
]

_PART_T = {
 "de": dict(
    tag="Partner", h2="Gemeinsam mit starken Partnern",
    lede="Planung und Lieferung sind nur so gut wie das Netzwerk dahinter. Wir arbeiten seit Jahren "
         "mit einer festen Gruppe zertifizierter Hersteller und spezialisierter Partnerfirmen "
         "zusammen &ndash; kurze Wege zur Entwicklung, verlässliche Verfügbarkeit und Sonderlösungen, "
         "die in keinem Katalog stehen. Das ist der Unterschied, den Sie im Projekt merken.",
    groups={"hersteller": "Hersteller &amp; Zulieferer", "planung": "Planung &amp; BIM"},
    aria="Partner {name} – Website in neuem Tab öffnen",
    roles={
      "coinfycare": "Untersuchungs- und Behandlungsliegen, medizinische Stühle und Sichtschutz – "
                    "die Basis unserer Medizinischen Einrichtung.",
      "techmed":    "Klinikeinrichtung aus Edelstahl: Wagen, Behandlungs- und Instrumententische, "
                    "Transport- und Sterilgutlogistik sowie MRT-Ausstattung.",
      "mobiak":     "Heilbehelfe und Hilfsmittel – von Rollstühlen und Gehhilfen bis zu "
                    "Anti-Dekubitus-Systemen und Sauerstoffversorgung.",
      "elers":      "Antimikrobielle Einweg-Sichtschutzvorhänge aus Finnland – Hygiene ohne "
                    "Waschkreislauf.",
      "rothband":   "Persönliche Strahlenschutz-Bekleidung aus britischer Fertigung – Schürzen, "
                    "Zweiteiler, Schilddrüsenschutz und Röntgenschutzbrillen.",
      "kenex":      "Montierter Strahlenschutz: mobile, decken- und tischmontierte Schutzsysteme "
                    "für OP und interventionelle Radiologie.",
      "plandata":   "Unser BIM-Partner aus Wien: Erstellung und Pflege unserer "
                    "Revit-Familienbibliothek und der zugehörigen Datenstandards.",
    }),
 "en": dict(
    tag="Partners", h2="Together with strong partners",
    lede="Design and delivery are only as good as the network behind them. For years we have worked "
         "with a fixed group of certified manufacturers and specialised partner companies &ndash; "
         "short routes to development, reliable availability and custom solutions that are in no "
         "catalogue. That is the difference you notice in a project.",
    groups={"hersteller": "Manufacturers &amp; suppliers", "planung": "Design &amp; BIM"},
    aria="Partner {name} – open website in a new tab",
    roles={
      "coinfycare": "Examination and treatment couches, medical chairs and privacy screens – "
                    "the basis of our medical furnishing.",
      "techmed":    "Hospital furnishing in stainless steel: trolleys, treatment and instrument "
                    "tables, transport and sterile goods logistics, plus MRI equipment.",
      "mobiak":     "Medical aids and assistive devices – from wheelchairs and walking aids to "
                    "anti-decubitus systems and oxygen supply.",
      "elers":      "Antimicrobial disposable privacy curtains from Finland – hygiene without a "
                    "laundry cycle.",
      "rothband":   "Personal radiation-protection wear made in the UK – aprons, two-piece sets, "
                    "thyroid shields and X-ray protective eyewear.",
      "kenex":      "Mounted radiation protection: mobile, ceiling- and table-mounted shielding "
                    "systems for the OR and interventional radiology.",
      "plandata":   "Our BIM partner from Vienna: creation and maintenance of our Revit family "
                    "library and the associated data standards.",
    }),
 "pl": dict(
    tag="Partnerzy", h2="Razem z silnymi partnerami",
    lede="Projektowanie i dostawy są tak dobre, jak sieć, która za nimi stoi. Od lat współpracujemy "
         "ze stałą grupą certyfikowanych producentów i wyspecjalizowanych firm partnerskich &ndash; "
         "krótkie drogi do działów rozwoju, niezawodna dostępność i rozwiązania specjalne, których "
         "nie ma w żadnym katalogu. To różnica, którą widać w projekcie.",
    groups={"hersteller": "Producenci i dostawcy", "planung": "Projektowanie i BIM"},
    aria="Partner {name} – otwórz stronę w nowej karcie",
    roles={
      "coinfycare": "Leżanki do badań i zabiegów, krzesła medyczne i parawany – podstawa naszego "
                    "wyposażenia medycznego.",
      "techmed":    "Wyposażenie szpitali ze stali nierdzewnej: wózki, stoliki zabiegowe i "
                    "narzędziowe, transport i logistyka materiałów sterylnych oraz wyposażenie do MR.",
      "mobiak":     "Środki pomocnicze i wyroby wspomagające – od wózków inwalidzkich i pomocy do "
                    "chodzenia po systemy przeciwodleżynowe i zaopatrzenie w tlen.",
      "elers":      "Antybakteryjne jednorazowe zasłony parawanowe z Finlandii – higiena bez obiegu "
                    "pralniczego.",
      "rothband":   "Osobista odzież ochronna przed promieniowaniem produkcji brytyjskiej – "
                    "fartuchy, komplety dwuczęściowe, osłony tarczycy i okulary rentgenowskie.",
      "kenex":      "Montowana ochrona radiologiczna: mobilne, sufitowe i stołowe systemy osłon na "
                    "blok operacyjny i radiologię zabiegową.",
      "plandata":   "Nasz partner BIM z Wiednia: tworzenie i utrzymanie naszej biblioteki rodzin "
                    "Revit oraz powiązanych standardów danych.",
    }),
 "ro": dict(
    tag="Parteneri", h2="Împreună cu parteneri puternici",
    lede="Proiectarea și livrarea sunt la fel de bune ca rețeaua din spatele lor. De ani de zile "
         "colaborăm cu un grup constant de producători certificați și firme partenere specializate "
         "&ndash; drum scurt către departamentele de dezvoltare, disponibilitate sigură și soluții "
         "speciale care nu se găsesc în niciun catalog. Aceasta este diferența pe care o simțiți în "
         "proiect.",
    groups={"hersteller": "Producători și furnizori", "planung": "Proiectare și BIM"},
    aria="Partener {name} – deschideți site-ul într-o filă nouă",
    roles={
      "coinfycare": "Canapele de examinare și tratament, scaune medicale și paravane – baza "
                    "mobilierului nostru medical.",
      "techmed":    "Dotări pentru clinici din oțel inoxidabil: cărucioare, mese de tratament și "
                    "pentru instrumente, transport și logistica materialelor sterile, dotări pentru RMN.",
      "mobiak":     "Mijloace ajutătoare și dispozitive de asistență – de la scaune rulante și cadre "
                    "de mers până la sisteme antiescară și alimentare cu oxigen.",
      "elers":      "Draperii de intimitate de unică folosință, antimicrobiene, din Finlanda – "
                    "igienă fără circuit de spălare.",
      "rothband":   "Îmbrăcăminte individuală de protecție la radiații, fabricată în Marea Britanie "
                    "– șorțuri, seturi din două piese, protecții pentru tiroidă și ochelari de "
                    "protecție radiologică.",
      "kenex":      "Protecție radiologică montată: sisteme mobile, montate pe tavan și pe masă, "
                    "pentru sala de operație și radiologia intervențională.",
      "plandata":   "Partenerul nostru BIM din Viena: crearea și întreținerea bibliotecii noastre de "
                    "familii Revit și a standardelor de date aferente.",
    }),
}

def _partner_section(lang="de", sid="partner"):
    t = _PART_T[lang]
    ap = "assets/" if lang == "de" else "/assets/"
    groups = []
    for gid, items in _PARTNERS:
        cards = []
        for slug, name, url in items:
            aria = _html.escape(t["aria"].format(name=name))
            cards.append(
f'        <a class="m-part m-part--{slug}" href="{url}" target="_blank" rel="noopener" aria-label="{aria}">\n'
'          <span class="m-part-logo">'
f'<img src="{ap}brands/{slug}.png" alt="{_html.escape(name)}" loading="lazy"></span>\n'
f'          <span class="m-part-role">{t["roles"][slug]}</span>\n'
'        </a>')
        groups.append(
'      <div class="m-part-group">\n'
f'        <div class="m-part-cap">{t["groups"][gid]}</div>\n'
'        <div class="m-part-grid">\n'
+ "\n".join(cards) + '\n'
'        </div>\n'
'      </div>')
    return (
f'<section class="m-graphic-sec m-part-sec" id="{sid}" style="background-image:url({ap}slogan-bg.jpg)">\n'
'  <div class="m-shell">\n'
'    <div class="m-fly-head">\n'
f'      <span class="m-tag">{t["tag"]}</span>\n'
f'      <h2 class="m-bigH">{t["h2"]}<span class="end-dot">.</span></h2>\n'
f'      <p class="lede">{t["lede"]}</p>\n'
'    </div>\n'
'    <div class="m-part-wrap">\n'
+ "\n".join(groups) + '\n'
'    </div>\n'
'  </div>\n'
'</section>')

def _inject_partner(body, lang):
    return body.replace("<!--PARTNER-->", _partner_section(lang))

# --- TECHMED-Bereiche (Medizinische Einrichtung 04–08) --------------------
# Noch ohne Produktdaten: Bereich lässt sich aufklappen und zeigt den Hinweis,
# dass die Modelle folgen. Sobald Daten da sind, wird hier auf Produktkarten
# umgestellt (wie CARDS[...] bei 01–03).
# Vierter Eintrag je Bereich = Unterbereiche (id, Titel); leer = keine.
_TM_SOON = "Die Modelle zu diesem Bereich werden derzeit aufbereitet und in Kürze ergänzt."
_TM_MFR = ('          <img class="m-ac-mfr m-ac-mfr--techmed" src="assets/brands/techmed.png"'
           ' alt="TECHMED" loading="lazy">\n')
_TM_CATS = [
    ("04", "medizinische-wagen",       "Medizinische Wagen", []),
    ("05", "geraete-versorgungswagen", "Geräte- &amp; Versorgungswagen", []),
    ("06", "behandlungstische",        "Behandlungs-, Instrumenten- &amp; Stationstische", []),
    ("07", "transport-sterilgut",      "Transport, Entsorgung &amp; Sterilgutlogistik", []),
    ("08", "stations-ambulanz",        "Stations- und Ambulanzausstattung", []),
    ("09", "mrt-ausstattung",          "MRT-Ausstattung (nicht-magnetisch)", []),
]

_MRT_LEAD = "Ausstattung, die im MRT-Raum verbleiben kann: Liege, Tritte, Infusionsständer, Wagen und Sichtschutz – komplett aus nicht-magnetischen Werkstoffen, damit Arbeitsabläufe nicht am Zonenübergang enden."
_MRT_NOTE = "Wichtiger Hinweis: Alle Produkte dieses Bereichs sind für Magnetfeldstärken bis 3 Tesla zugelassen. Für Systeme mit höherer Feldstärke sprechen Sie uns bitte an."
_WG_LEAD = "Fahrbare Wagen für Anästhesie, Notfall, Station und Behandlung – wahlweise mit geschlossenem Stahlkorpus oder als modulare Aluminium-Plattform, die Sie Schublade für Schublade auf Ihren Ablauf zuschneiden."
_WG_NOTE1 = "Einheitlich aufgebaut: 500 mm Korpustiefe, 1000 mm Arbeitshöhe, vertiefte Arbeitsplatte mit drei Aufkantungen und Ø 125 mm Rollen mit zwei Feststellern. Fronten und Griffe sind farbig nach TECH-MED-Farbkarte erhältlich – so lassen sich Stationen auf einen Blick unterscheiden. Das Zubehörprogramm ist über alle Baureihen hinweg identisch und frei kombinierbar."
_WG_NOTE2 = "Materialausführungen: ABS = Stahlkorpus mit Arbeitsplatte aus ABS-Kunststoff · ST = Korpus und Arbeitsplatte aus pulverbeschichtetem Stahl · KO = Korpus und Arbeitsplatte aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe."
_ST_LEAD = "Ausstattung für Bettenstation und Ambulanz: Nachtkästchen, Bettbeistelltische, Infusionsständer, Auftritte und Injektionsstühle sowie teleskopierbare Wandarme für Infusionen und Sichtschutz – überwiegend aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) oder pulverbeschichtetem Stahl und auf tägliche Wischdesinfektion ausgelegt."
_ST_NOTE = "Farbgebung nach TECH-MED-Farbkarte: Fronten, Türen und Polster sind in mehreren RAL- und Bezugsfarben erhältlich – so lassen sich Stationen und Bereiche auf einen Blick unterscheiden. Materialkürzel: ST = pulverbeschichteter Stahl · KO = Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) · ABS = ABS-Kunststoff · HPL = wasserfeste Schichtstoffplatte."
_GV_LEAD = "Fahrbare Geräteträger und Versorgungswagen für Diagnostik, Behandlung und Stationsalltag: schlanke Aluminium-Säulenwagen, die Sie Ebene für Ebene bestücken, und Behandlungswagen mit Edelstahlplatte für Verbandwechsel, Blutabnahme und Medikamentenverteilung."
_GV_NOTE = "Zwei Bausysteme, ein Zubehörprogramm: Bei den Säulenwagen (ECO, TOP, MOD, K-1, K-1 LUX, APAR) sitzen alle Ebenen auf gemeinsamen Aluminiumsäulen und lassen sich in der Höhe frei versetzen – Steckdosenleiste, Normschiene, Zubehörkorb, Monitorhalter und Infusionsständer sind über alle Baureihen hinweg identisch und frei kombinierbar. Die Stationswagen K-3, MB-3 und WL sind auf tägliche Wischdesinfektion ausgelegt; Fronten und Säulenblenden gibt es farbig nach TECH-MED-Farbkarte."
_BT_LEAD = "Behandlungstische und Instrumententische für Eingriffsraum, Ambulanz und OP: fahrbare Behandlungstische mit vertiefter Arbeitsplatte und Anbauzubehör sowie höhenverstellbare Instrumententische aus Edelstahl – manuell, hydraulisch oder elektrisch."
_BT_NOTE = "Materialausführungen: KO = komplett aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe · ST = komplett aus pulverbeschichtetem Stahl, farbig nach TECH-MED-Farbkarte. Bei den Behandlungstischen STKO bestimmt die gewählte Plattenlänge die Gesamtlänge des Tisches; bei den Instrumententischen verändert die Rollenausführung die Bauhöhe."
_TR_LEAD = "Transport, Entsorgung und Sterilgutlogistik in einem Bereich: Transport- und Speisenwagen, Korbwagen für den innerbetrieblichen Materialfluss, Wäsche- und Abfallwagen für die Entsorgung sowie Packtische und Regalsysteme für die Sterilgutaufbereitung und das Lager."
_TR_NOTE = "Ein Baukasten für alle Regalsysteme: Körbe, Ablagen, Abwurfbeutelhalter und Trockner werden in dieselben Schienen und Gestelle eingehängt – ob als Wandschiene, Standregal oder fahrbarer Wagen. Die Entsorgungswagen gibt es in zwei Bauweisen: komplett aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe (WZ, WZB, MB) oder in Möbelbauweise mit Aluminium-Profilrahmen und farbigen Füllungen nach RAL (WMW, WCB)."

# Bereiche mit echten Produktkarten: sid -> (Kategorie in products.json, Lead, [Hinweise])
_TM_CARDS = {
    "medizinische-wagen":       ("wagen",   _WG_LEAD,  [_WG_NOTE1, _WG_NOTE2]),
    "geraete-versorgungswagen": ("gvw",     _GV_LEAD,  [_GV_NOTE]),
    "behandlungstische":        ("btisch",  _BT_LEAD,  [_BT_NOTE]),
    "transport-sterilgut":      ("trans",   _TR_LEAD,  [_TR_NOTE]),
    "stations-ambulanz":        ("station", _ST_LEAD,  [_ST_NOTE]),
    "mrt-ausstattung":          ("mrt",     _MRT_LEAD, [_MRT_NOTE]),
}

def _tm_card_body(catkey, lead, notes):
    hinweise = ""
    if notes:
        hinweise = ('          <div class="m-dl-note m-dl-note--plain">\n'
                    + "".join(f'            <p>{n}</p>\n' for n in notes)
                    + '          </div>\n')
    return (f'          <p class="m-ac-lead">{lead}</p>\n'
            + hinweise
            + f'          <p class="m-pl-count">{_count(catkey)} Modelle verfügbar</p>\n'
              '          <div class="m-pl-list">\n'
            + CARDS[catkey] + '\n'
              '          </div>\n')

def _techmed_sections():
    out = []
    for num, sid, title, subs in _TM_CATS:
        if subs:
            inner = "\n\n".join(
f'            <details class="m-ac m-ac-sub" id="{ssid}">\n'
f'              <summary><span class="m-ac-title">{stitle}</span>' + CHEV + '</summary>\n'
 '              <div class="m-ac-body">\n'
f'                <p class="m-ac-lead">{_TM_SOON}</p>\n'
 '              </div>\n'
 '            </details>' for ssid, stitle in subs)
            body = ('          <div class="m-acc m-acc-nested">\n\n'
                    + inner + '\n\n          </div>\n')
        elif sid in _TM_CARDS:
            body = _tm_card_body(*_TM_CARDS[sid])
        else:
            body = f'          <p class="m-ac-lead">{_TM_SOON}</p>\n'
        out.append(
f'      <details class="m-ac" id="{sid}">\n'
f'        <summary><span class="m-ac-num">{num}</span><span class="m-ac-title">{title}</span>' + CHEV + '</summary>\n'
 '        <div class="m-ac-body">\n'
 + _TM_MFR + body +
 '        </div>\n'
 '      </details>')
    return "\n\n".join(out)

BODY_PRODUKTE = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Produkte</span>
    <h1>Unsere Produkte<span class="end-dot">.</span></h1>
    <p class="lede">Wir vermitteln und liefern zertifizierte Medizinprodukte in mehreren Kategorien: Strahlenschutz, Medizinische Einrichtung und Heilbehelfe &amp; Hilfsmittel. Darüber hinaus beschaffen wir herstellerunabhängig nahezu jedes Produkt und statten ganze Bereiche projektbasiert aus. Klicken Sie eine Kategorie an, um die einzelnen Bereiche zu entdecken.</p>
  </div>
</section>

<!--FLYER-->

<section class="m-section m-hexbg m-hexbg-l" id="strahlenschutz" style="--hexbg:url('assets/brands/ss-hero.jpg');--hexbg2:url('assets/brands/kenex-hero.jpg')">
  <div class="m-shell">
    <div class="m-cat-head has-mfr">
      <div class="m-cat-head-text">
        <h2>Strahlenschutz<span class="end-dot">.</span></h2>
        <div class="sub">Persönliche Strahlenschutz-Bekleidung „Made in UK\" vom Hersteller ROTHBAND – ergänzt um passende Aufbewahrung sowie mobile, deckenmontierte und tischmontierte Röntgenschutzsysteme von KENEX. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.</div>
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
                <p class="m-ac-lead">Jede Schürze lässt sich individuell anpassen – für eine bessere Zuordnung, mehr Tragekomfort und praktische Details im Klinikalltag. Alle Optionen sind mit den Modellen aus „Persönlicher Strahlenschutz\" kombinierbar.</p>
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
''' + _downloads_cat_cards("06", "downloads-strahlenschutz", _DL_LEAD_SS, DL_SS) + '''
    </div>
  </div>
</section>

<section class="m-section alt m-hexbg m-hexbg-l m-hexbg--photo" id="medizinische-einrichtung" style="--hexbg:url('assets/brands/med-hero.jpg');--hexbg2:url('assets/brands/techmed-hero.jpg')">
  <div class="m-shell">
    <div class="m-cat-head has-mfr">
      <div class="m-cat-head-text">
        <h2>Medizinische Einrichtung<span class="end-dot">.</span></h2>
        <div class="sub">Ausstattung und Einrichtung für klinische Bereiche – vom Untersuchungsplatz bis zur Sterilgutlogistik. Geliefert von COINFYCARE (Liegen, Stühle, Sichtschutz) und TECHMED (Wagen und Tische, Transport und Entsorgung, Stations- und Ambulanzausstattung, MRT-Ausstattung). Klicken Sie einen Bereich an, um die Modelle aufzuklappen.</div>
      </div>
      <div class="m-mfr">
        <span class="m-mfr-cap">Hersteller</span>
        <div class="m-mfr-chips">
          <a class="m-mfr-chip m-mfr-chip--coinfy" href="https://www.coinfycare.com/en" target="_blank" rel="noopener" aria-label="Hersteller COINFYCARE – Website in neuem Tab öffnen"><img src="assets/brands/coinfycare.png" alt="COINFYCARE" loading="lazy"></a>
          <a class="m-mfr-chip m-mfr-chip--techmed" href="https://en.techmed.com.pl/" target="_blank" rel="noopener" aria-label="Hersteller TECHMED – Website in neuem Tab öffnen"><img src="assets/brands/techmed.png" alt="TECHMED" loading="lazy"></a>
        </div>
      </div>
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

''' + _techmed_sections() + '''
''' + _downloads_datasheets("10", "downloads-medizinische-einrichtung", _DL_LEAD_MED, DL_MED_CATS, catalog=DL_MED_CATALOG) + '''
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
''' + _downloads_category("06", "downloads-heilbehelfe", "", [], note=_DL_NOTE_ANFRAGE_HB) + '''
    </div>
  </div>
</section>

<section class="m-section alt m-hexbg m-hexbg--photo" id="beschaffung" style="--hexbg:url('assets/brands/sourcing-hero.jpg')">
  <div class="m-shell">
    <div class="m-cat-head">
      <div class="m-cat-head-text">
        <h2>Herstellerunabhängige Produktbeschaffung<span class="end-dot">.</span></h2>
        <div class="sub">Sie suchen ein Produkt, das nicht in unserem Katalog enthalten ist? Dank unserer Herstellerunabhängigkeit sind wir nicht an bestimmte Marken gebunden und können Produkte verschiedenster Hersteller für Sie beschaffen.</div>
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
</section>
<script>
(function(){
  var L=(document.documentElement.lang||'de');
  var T={de:'Bereich schließen',en:'Close section',pl:'Zamknij sekcję',ro:'Închide secțiunea'};
  var label=T[L]||T.de;
  var chev='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 15l6-6 6 6"/></svg>';
  function closeAndScroll(d){
    d.open=false;
    var y=d.getBoundingClientRect().top+window.scrollY-92;
    window.scrollTo({top:y,behavior:'smooth'});
  }
  // Blatt-Akkordeons = Kategorien OHNE verschachtelte Akkordeons.
  // Gibt es Unterkategorien, sitzt die Schließfunktion auf jeder Unterkategorie, sonst auf der Kategorie selbst.
  var leaves=[];
  document.querySelectorAll('details.m-ac').forEach(function(d){
    if(!d.querySelector('details.m-ac')) leaves.push(d);
  });
  leaves.forEach(function(d){
    var body=d.querySelector(':scope > .m-ac-body');
    if(!body || body.querySelector(':scope > .m-ac-close')) return;
    var btn=document.createElement('button');
    btn.type='button'; btn.className='m-ac-close';
    btn.innerHTML=chev+'<span>'+label+'</span>';
    btn.addEventListener('click',function(){ closeAndScroll(d); });
    body.appendChild(btn);
  });
  // Schwebender Schließen-Button: sichtbar, sobald man in eine geöffnete (Unter-)Kategorie gescrollt ist
  var fab=document.createElement('button');
  fab.type='button'; fab.className='m-ac-fab'; fab.style.display='none';
  fab.innerHTML=chev+'<span>'+label+'</span>';
  document.body.appendChild(fab);
  function currentOpen(){
    var vy=90;
    for(var i=0;i<leaves.length;i++){ var d=leaves[i]; if(!d.open) continue;
      var r=d.getBoundingClientRect();
      if(r.top < vy && r.bottom > vy+60) return d; }
    return null;
  }
  function updateFab(){ var d=currentOpen(); fab._t=d||null; fab.style.display=d?'inline-flex':'none'; }
  fab.addEventListener('click',function(){ if(fab._t) closeAndScroll(fab._t); setTimeout(updateFab,60); });
  window.addEventListener('scroll',updateFab,{passive:true});
  window.addEventListener('resize',updateFab);
  document.addEventListener('toggle',updateFab,true);
  updateFab();
})();
</script>'''

# ================= Produkte-Übersetzungen (statische UI) =================
_PUI = {
 "en": {
  "Produkte": "Products",
  "Unsere Produkte": "Our products",
  "Wir vermitteln und liefern zertifizierte Medizinprodukte in mehreren Kategorien: Strahlenschutz, Medizinische Einrichtung und Heilbehelfe &amp; Hilfsmittel. Darüber hinaus beschaffen wir herstellerunabhängig nahezu jedes Produkt und statten ganze Bereiche projektbasiert aus. Klicken Sie eine Kategorie an, um die einzelnen Bereiche zu entdecken.": "We supply and deliver certified medical products across several categories: radiation protection, medical furnishing, and medical aids &amp; assistive devices. In addition, we procure almost any product manufacturer-independently and equip entire areas on a project basis. Click a category to explore the individual sections.",
  "Strahlenschutz": "Radiation protection",
  "Persönliche Strahlenschutz-Bekleidung „Made in UK\" vom Hersteller ROTHBAND – ergänzt um passende Aufbewahrung sowie mobile, deckenmontierte und tischmontierte Röntgenschutzsysteme von KENEX. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.": "Personal radiation-protection wear „Made in UK“ from manufacturer ROTHBAND – complemented by suitable storage as well as mobile, ceiling-mounted and table-mounted X-ray protection systems from KENEX. Click a section to expand the models.",
  "Hersteller": "Manufacturer",
  "Hersteller ROTHBAND – Website in neuem Tab öffnen": "Manufacturer ROTHBAND – open website in a new tab",
  "Hersteller KENEX – Website in neuem Tab öffnen": "Manufacturer KENEX – open website in a new tab",
  "Hersteller COINFYCARE – Website in neuem Tab öffnen": "Manufacturer COINFYCARE – open website in a new tab",
  "Hersteller TECHMED – Website in neuem Tab öffnen": "Manufacturer TECHMED – open website in a new tab",
  "Medizinische Wagen": "Medical carts",
  "Geräte- &amp; Versorgungswagen": "Equipment &amp; supply carts",
  "Behandlungs-, Instrumenten- &amp; Stationstische": "Treatment, instrument &amp; ward tables",
  "Transport, Entsorgung &amp; Sterilgutlogistik": "Transport, waste disposal &amp; sterile goods logistics",
  "Stations- und Ambulanzausstattung": "Ward and outpatient equipment",
  "MRT-Ausstattung (nicht-magnetisch)": "MRI equipment (non-magnetic)",
  "Die Modelle zu diesem Bereich werden derzeit aufbereitet und in Kürze ergänzt.": "The models for this section are currently being prepared and will be added shortly.",
  "Hersteller MOBIAK – Website in neuem Tab öffnen": "Manufacturer MOBIAK – open website in a new tab",
  "Persönlicher Strahlenschutz": "Personal radiation protection",
  "Strahlenschutzbekleidung für den direkten Personenschutz – Schürzen, Zweiteiler, Schilddrüsenschutz und ergänzendes Zubehör. Fokus auf Ergonomie, Gewichtsverteilung, Schutzleistung und Tragekomfort.": "Radiation-protection wear for direct personal protection – aprons, two-piece sets, thyroid shields and complementary accessories. Focus on ergonomics, weight distribution, protective performance and wearing comfort.",
  "Front-Schürzen": "Front aprons",
  "Umhang-/Tabard-Schürzen": "Tabard aprons",
  "Mantel-/Wickelschürzen": "Coat / wrap-around aprons",
  "Zweiteiler – Oberteil &amp; Rock": "Two-piece – top &amp; skirt",
  "Schilddrüsenschutz": "Thyroid shields",
  "Zubehör": "Accessories",
  "Strahlenschutzbrillen": "Radiation-protection glasses",
  "Röntgenschutzbrillen für den Schutz der Augen bei Durchleuchtung, interventioneller Bildgebung und Radiologie – in zahlreichen Rahmenformen, mit seitlichem Schutz und wahlweise mit Sehstärke. Bleigläser 0,75 mm Pb, Seitenschutz 0,50 mm Pb.": "X-ray protection glasses to protect the eyes during fluoroscopy, interventional imaging and radiology – in numerous frame shapes, with side protection and optionally with prescription lenses. Lead glass 0.75 mm Pb, side protection 0.50 mm Pb.",
  "Personalisierung &amp; Optionen": "Personalisation &amp; options",
  "Jede Schürze lässt sich individuell anpassen – für eine bessere Zuordnung, mehr Tragekomfort und praktische Details im Klinikalltag. Alle Optionen sind mit den Modellen aus „Persönlicher Strahlenschutz\" kombinierbar.": "Every apron can be individually customised – for better identification, greater wearing comfort and practical details in everyday clinical use. All options can be combined with the models from „Personal radiation protection“.",
  "Farboptionen": "Colour options",
  "Alle Schürzen und Zubehörteile sind in zahlreichen Farben, Mustern und Einfassungen erhältlich – für ein individuelles, gut erkennbares Erscheinungsbild. Das Stoffsortiment wird von ROTHBAND laufend erweitert.": "All aprons and accessories are available in numerous colours, patterns and bindings – for an individual, easily recognisable appearance. The fabric range is continuously expanded by ROTHBAND.",
  "Aufbewahrung": "Storage",
  "Ständer, Schwenkarme und Bügel zur sicheren, platzsparenden Aufbewahrung von Strahlenschutzschürzen.": "Stands, swivel arms and hangers for safe, space-saving storage of radiation-protection aprons.",
  "Mobiler Strahlenschutz": "Mobile radiation protection",
  "Fahrbare, frei positionierbare Röntgenschutzsysteme für flexible Einsätze im OP und in der interventionellen Radiologie – vom Hersteller KENEX.": "Wheeled, freely positionable X-ray protection systems for flexible use in the operating theatre and in interventional radiology – from manufacturer KENEX.",
  "Deckenmontierter Strahlenschutz": "Ceiling-mounted radiation protection",
  "Aufgehängte Überkopf-Schutzschilde und komplette Aufhängungssysteme (Deckenschienen, Säulen, Arme, Monitor-Aufhängung) – zur deutlichen Reduktion der Streustrahlung im Arbeitsbereich. Vom Hersteller KENEX.": "Suspended overhead protective shields and complete suspension systems (ceiling rails, columns, arms, monitor suspension) – to significantly reduce scattered radiation in the working area. From manufacturer KENEX.",
  "Überkopf-Schutzschilde": "Overhead protective shields",
  "Aufhängungssysteme": "Suspension systems",
  "Tischmontierter Strahlenschutz": "Table-mounted radiation protection",
  "Am Untersuchungstisch montierte Schutzschilde für die interventionelle Radiologie – Unterkörper-, Kopfende- und Aufsatz-Schilde sowie passende Aufbewahrung. Vom Hersteller KENEX.": "Protective shields mounted on the examination table for interventional radiology – lower-body, head-end and add-on shields as well as suitable storage. From manufacturer KENEX.",
  "Unterkörper-Tischschilde": "Lower-body table shields",
  "Kopfende-Tischschilde": "Head-end table shields",
  "Aufsatz- &amp; Fußende-Schilde": "Add-on &amp; foot-end shields",
  "Aufbewahrung &amp; Zubehör": "Storage &amp; accessories",
  "Modelle verfügbar": "models available",
  "Fahrbare Wagen für Anästhesie, Notfall, Station und Behandlung – wahlweise mit geschlossenem Stahlkorpus oder als modulare Aluminium-Plattform, die Sie Schublade für Schublade auf Ihren Ablauf zuschneiden.": "Mobile trolleys for anaesthesia, emergency, ward and treatment – either with a closed steel cabinet or as a modular aluminium platform that you tailor drawer by drawer to your workflow.",
  "Einheitlich aufgebaut: 500 mm Korpustiefe, 1000 mm Arbeitshöhe, vertiefte Arbeitsplatte mit drei Aufkantungen und Ø 125 mm Rollen mit zwei Feststellern. Fronten und Griffe sind farbig nach TECH-MED-Farbkarte erhältlich – so lassen sich Stationen auf einen Blick unterscheiden. Das Zubehörprogramm ist über alle Baureihen hinweg identisch und frei kombinierbar.": "Built to one standard: 500 mm cabinet depth, 1000 mm working height, a recessed worktop with three raised edges and Ø 125 mm castors with two brakes. Fronts and handles are available in colour according to the TECH-MED colour card, so wards can be told apart at a glance. The accessory programme is identical across all series and freely combinable.",
  "Materialausführungen: ABS = Stahlkorpus mit Arbeitsplatte aus ABS-Kunststoff · ST = Korpus und Arbeitsplatte aus pulverbeschichtetem Stahl · KO = Korpus und Arbeitsplatte aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe.": "Material versions: ABS = steel cabinet with an ABS plastic worktop · ST = cabinet and worktop of powder-coated steel · KO = cabinet and worktop of stainless steel 0H18N9 (austenitic, 1.4301) for the highest hygiene level.",
  "Ausstattung für Bettenstation und Ambulanz: Nachtkästchen, Bettbeistelltische, Infusionsständer, Auftritte und Injektionsstühle sowie teleskopierbare Wandarme für Infusionen und Sichtschutz – überwiegend aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) oder pulverbeschichtetem Stahl und auf tägliche Wischdesinfektion ausgelegt.": "Equipment for inpatient wards and outpatient clinics: bedside cabinets, overbed tables, IV pole stands, foot stools and injection chairs, plus telescopic wall arms for infusions and privacy screening – mostly in stainless steel 0H18N9 (austenitic, 1.4301) or powder-coated steel and designed for daily wipe disinfection.",
  "Farbgebung nach TECH-MED-Farbkarte: Fronten, Türen und Polster sind in mehreren RAL- und Bezugsfarben erhältlich – so lassen sich Stationen und Bereiche auf einen Blick unterscheiden. Materialkürzel: ST = pulverbeschichteter Stahl · KO = Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) · ABS = ABS-Kunststoff · HPL = wasserfeste Schichtstoffplatte.": "Colours to the TECH-MED colour chart: fronts, doors and upholstery are available in several RAL and fabric colours – so wards and areas can be told apart at a glance. Material codes: ST = powder-coated steel · KO = stainless steel 0H18N9 (austenitic, 1.4301) · ABS = ABS plastic · HPL = waterproof laminate board.",
  "Fahrbare Geräteträger und Versorgungswagen für Diagnostik, Behandlung und Stationsalltag: schlanke Aluminium-Säulenwagen, die Sie Ebene für Ebene bestücken, und Behandlungswagen mit Edelstahlplatte für Verbandwechsel, Blutabnahme und Medikamentenverteilung.": "Mobile equipment trolleys and supply carts for diagnostics, treatment and everyday ward work: slim aluminium column trolleys that you equip level by level, and treatment trolleys with a stainless steel top for dressing changes, blood sampling and medication distribution.",
  "Zwei Bausysteme, ein Zubehörprogramm: Bei den Säulenwagen (ECO, TOP, MOD, K-1, K-1 LUX, APAR) sitzen alle Ebenen auf gemeinsamen Aluminiumsäulen und lassen sich in der Höhe frei versetzen – Steckdosenleiste, Normschiene, Zubehörkorb, Monitorhalter und Infusionsständer sind über alle Baureihen hinweg identisch und frei kombinierbar. Die Stationswagen K-3, MB-3 und WL sind auf tägliche Wischdesinfektion ausgelegt; Fronten und Säulenblenden gibt es farbig nach TECH-MED-Farbkarte.": "Two construction systems, one accessory range: on the column trolleys (ECO, TOP, MOD, K-1, K-1 LUX, APAR) all levels sit on shared aluminium columns and can be repositioned freely in height – power socket strip, medi-rail, accessories basket, monitor holder and IV pole are identical across all series and freely combinable. The K-3, MB-3 and WL ward trolleys are designed for daily wipe disinfection; fronts and column trims are available in colour to the TECH-MED colour chart.",
  "Behandlungstische und Instrumententische für Eingriffsraum, Ambulanz und OP: fahrbare Behandlungstische mit vertiefter Arbeitsplatte und Anbauzubehör sowie höhenverstellbare Instrumententische aus Edelstahl – manuell, hydraulisch oder elektrisch.": "Treatment tables and instrument tables for the procedure room, outpatient clinic and operating theatre: mobile treatment trolleys with a recessed worktop and add-on accessories, plus height-adjustable stainless steel instrument tables – manual, hydraulic or electric.",
  "Materialausführungen: KO = komplett aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe · ST = komplett aus pulverbeschichtetem Stahl, farbig nach TECH-MED-Farbkarte. Bei den Behandlungstischen STKO bestimmt die gewählte Plattenlänge die Gesamtlänge des Tisches; bei den Instrumententischen verändert die Rollenausführung die Bauhöhe.": "Material versions: KO = entirely of stainless steel 0H18N9 (austenitic, 1.4301) for the highest hygiene level · ST = entirely of powder-coated steel, in colour to the TECH-MED colour chart. On the STKO treatment trolleys the chosen top length determines the overall length of the trolley; on the instrument tables the castor type changes the overall height.",
  "Transport, Entsorgung und Sterilgutlogistik in einem Bereich: Transport- und Speisenwagen, Korbwagen für den innerbetrieblichen Materialfluss, Wäsche- und Abfallwagen für die Entsorgung sowie Packtische und Regalsysteme für die Sterilgutaufbereitung und das Lager.": "Transport, waste disposal and sterile goods logistics in one section: transport and food trolleys, basket trolleys for internal material flow, linen and waste trolleys for disposal, plus packing tables and rack systems for sterile processing and the store.",
  "Ein Baukasten für alle Regalsysteme: Körbe, Ablagen, Abwurfbeutelhalter und Trockner werden in dieselben Schienen und Gestelle eingehängt – ob als Wandschiene, Standregal oder fahrbarer Wagen. Die Entsorgungswagen gibt es in zwei Bauweisen: komplett aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe (WZ, WZB, MB) oder in Möbelbauweise mit Aluminium-Profilrahmen und farbigen Füllungen nach RAL (WMW, WCB).": "One modular system for all racks: baskets, shelves, waste bag holders and dryers hook into the same rails and frames – whether as a wall slat, a free-standing rack or a mobile trolley. The waste trolleys come in two constructions: entirely of stainless steel 0H18N9 (austenitic, 1.4301) for the highest hygiene level (WZ, WZB, MB) or in furniture construction with an aluminium profile frame and coloured panels in RAL (WMW, WCB).",
  "Ausstattung, die im MRT-Raum verbleiben kann: Liege, Tritte, Infusionsständer, Wagen und Sichtschutz – komplett aus nicht-magnetischen Werkstoffen, damit Arbeitsabläufe nicht am Zonenübergang enden.": "Equipment that can stay inside the MRI room: couch, foot stools, IV stand, trolleys and screens – made entirely of non-magnetic materials, so that workflows do not end at the zone boundary.",
  "Wichtiger Hinweis: Alle Produkte dieses Bereichs sind für Magnetfeldstärken bis 3 Tesla zugelassen. Für Systeme mit höherer Feldstärke sprechen Sie uns bitte an.": "Important note: all products in this section are approved for magnetic field strengths of up to 3 tesla. For systems with a higher field strength, please contact us.",
  "Modell verfügbar": "model available",
  "Produkte verfügbar": "products available",
  "Medizinische Einrichtung": "Medical furnishing",
  "Ausstattung und Einrichtung für klinische Bereiche – vom Untersuchungsplatz bis zur Sterilgutlogistik. Geliefert von COINFYCARE (Liegen, Stühle, Sichtschutz) und TECHMED (Wagen und Tische, Transport und Entsorgung, Stations- und Ambulanzausstattung, MRT-Ausstattung). Klicken Sie einen Bereich an, um die Modelle aufzuklappen.": "Equipment and furnishing for clinical areas – from the examination station to sterile goods logistics. Supplied by COINFYCARE (couches, chairs, privacy screens) and TECHMED (carts and tables, transport and waste disposal, ward and outpatient equipment, MRI equipment). Click a section to expand the models.",
  "Untersuchungsliegen": "Examination couches",
  "Untersuchungs- und Behandlungsliegen für Praxis und Klinik – nach Bauart gegliedert.": "Examination and treatment couches for practice and clinic – organised by design type.",
  "Fix": "Fixed",
  "Hydraulisch": "Hydraulic",
  "Elektrisch": "Electric",
  "Chiropraktische Liegen": "Chiropractic couches",
  "Medizinische Stühle": "Medical chairs",
  "Behandlungs-, Blutabnahme- und Arbeitsstühle sowie Hocker für den medizinischen Einsatz.": "Treatment, blood-collection and work chairs as well as stools for medical use.",
  "Sichtschutz": "Privacy screens",
  "Sicht- und Trennwandsysteme für diskrete, flexibel teilbare Raumbereiche.": "Privacy and partition systems for discreet, flexibly divisible room areas.",
  "Heilbehelfe &amp; Hilfsmittel": "Medical aids &amp; assistive devices",
  "Mobilität, Pflege und Alltagshilfen – von Rollstühlen und Elektromobilen über Gehhilfen bis zu Anti-Dekubitus-Systemen und Sauerstoffversorgung. Geliefert vom Hersteller MOBIAK. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.": "Mobility, care and everyday aids – from wheelchairs and mobility scooters through walking aids to anti-decubitus systems and oxygen supply. Supplied by manufacturer MOBIAK. Click a section to expand the models.",
  "Rollstühle": "Wheelchairs",
  "Elektrische Rollstühle &amp; Scooter": "Electric wheelchairs &amp; scooters",
  "Gehhilfen": "Walking aids",
  "Rollatoren": "Rollators",
  "Gehböcke / Walker": "Walking frames / walkers",
  "Anti-Dekubitus-Produkte": "Anti-decubitus products",
  "Sauerstoffkonzentratoren": "Oxygen concentrators",
  "Herstellerunabhängige Produktbeschaffung": "Manufacturer-independent product procurement",
  "Sie suchen ein Produkt, das nicht in unserem Katalog enthalten ist? Dank unserer Herstellerunabhängigkeit sind wir nicht an bestimmte Marken gebunden und können Produkte verschiedenster Hersteller für Sie beschaffen.": "Looking for a product that is not in our catalogue? Thanks to our manufacturer independence we are not tied to particular brands and can procure products from a wide range of manufacturers for you.",
  "Alles beschaffbar": "Anything procurable",
  "Ob Standardartikel, Spezialgerät oder schwer erhältliches Ersatzteil – wir identifizieren die passende Bezugsquelle und liefern zuverlässig. Kein Sortiment setzt uns Grenzen: Sie nennen den Bedarf, wir finden die Lösung.": "Whether a standard item, a specialised device or a hard-to-find spare part – we identify the right source and deliver reliably. No range limits us: you name the need, we find the solution.",
  "Komplette Bereichsausstattung": "Complete area equipping",
  "Von der Praxis bis zur Klinikabteilung statten wir ganze Bereiche aus – abgestimmt auf Arbeitsabläufe, Hygieneanforderungen und Budget. Grundausstattung, Mobiliar und High-End-Technik aus einer Hand.": "From the practice to the hospital department we equip entire areas – tailored to workflows, hygiene requirements and budget. Basic equipment, furniture and high-end technology from a single source.",
  "Herstellerunabhängig": "Manufacturer-independent",
  "Wir sind an keine Marke gebunden. So wählen wir stets das Produkt, das technisch, wirtschaftlich und qualitativ am besten zu Ihrer Anforderung passt – objektiv und in Ihrem Interesse.": "We are not tied to any brand. This way we always choose the product that best fits your requirement technically, economically and in terms of quality – objectively and in your interest.",
  "Projekt- &amp; Komplettservice": "Project &amp; complete service",
  "Ein Ansprechpartner für den gesamten Beschaffungsprozess: Bedarfsanalyse, Angebot, Einkauf, Logistik und Lieferung – auf Wunsch inklusive Installation und Einschulung. Termintreu, transparent und aus einer Hand.": "A single point of contact for the entire procurement process: needs analysis, quotation, purchasing, logistics and delivery – including installation and training on request. On schedule, transparent and from a single source.",
  "Sie haben einen konkreten Bedarf oder planen ein Projekt? Beschreiben Sie uns Ihr Vorhaben – wir erstellen Ihnen ein individuelles, unverbindliches Angebot.": "Do you have a specific need or are you planning a project? Describe your plans to us – we will prepare an individual, no-obligation quote for you.",
  "Projekt anfragen": "Request a project",
  "Downloads &amp; Unterlagen": "Downloads &amp; documents",
  "Zur Kontaktseite": "To the contact page",
  "Chiropraktisch": "Chiropractic",
  "Herstellerkataloge": "Manufacturer catalogues",
  "Innenmaterial": "Inner material",
  "Persönliche Schutzausrüstung": "Personal protective equipment",
  "Schnittbildgebung": "Cross-sectional imaging",
  "ROTHBAND · PDF": "ROTHBAND · PDF",
  "OUTLAST®": "OUTLAST®",
  "Hier finden Sie unsere Produktkataloge und Unterlagen zu unseren Produkten des Strahlenschutzes. Neue Dokumente ergänzen wir laufend.": "Here you will find our product catalogues and documents for our radiation-protection products. We add new documents on an ongoing basis.",
  "Persönliche Schutzausrüstung und Aufbewahrung": "Personal protective equipment and storage",
  "Innenmaterial der persönlichen Schutzausrüstung": "Inner material of the personal protective equipment",
  "KENEX · PDF": "KENEX · PDF",
  "Hier finden Sie unsere Produktkataloge und Farbkarten sowie die technischen Datenblätter zu unseren Produkten der Medizinischen Einrichtung. Der COINFYCARE-Katalog deckt die Bereiche 01–03 ab, der TECH-MED-Katalog samt Farbkarten die Bereiche 04–09 einschließlich Schienensysteme. Neue Dokumente ergänzen wir laufend.": "Here you will find our product catalogues and colour cards as well as the technical data sheets for our medical-furnishing products. The COINFYCARE catalogue covers sections 01–03, while the TECH-MED catalogue and its colour cards cover sections 04–09 including the rail systems. We add new documents on an ongoing basis.",
  "Produktkatalog": "Product catalogue",
  "Produktkataloge & Farbkarten": "Product catalogues & colour cards",
  "Produktkatalog · Bereiche 01–03": "Product catalogue · Sections 01–03",
  "Produktkatalog · Bereiche 04–09": "Product catalogue · Sections 04–09",
  "Farbkarten · Bereiche 04–09": "Colour cards · Sections 04–09",
  "COINFYCARE · PDF": "COINFYCARE · PDF",
  "TECH-MED · PDF": "TECH-MED · PDF",
  "Die Unterlagen zu unseren Produkten des Strahlenschutzes senden wir Ihnen gerne auf Anfrage zu.": "We are happy to send you the documents for our radiation-protection products on request.",
  "Die Unterlagen zu unseren Produkten der Medizinischen Einrichtung senden wir Ihnen gerne auf Anfrage zu.": "We are happy to send you the documents for our medical-furnishing products on request.",
  "Die Unterlagen zu unseren Heilbehelfen und Hilfsmitteln senden wir Ihnen gerne auf Anfrage zu.": "We are happy to send you the documents for our medical aids and assistive devices on request.",
  "Personalisierung": "Personalisation",
  "Optionale Extras": "Optional extras",
  "Stickerei": "Embroidery",
  "Individuelle Textstickerei direkt auf der Schürze – z. B. Name, Abteilung oder Einsatzbereich.": "Individual text embroidery directly on the apron – e.g. name, department or area of use.",
  "Aufgesetzte Tasche": "Patch pocket",
  "Praktische Außentasche für Dosimeter, Stift oder Kleinteile.": "Practical outer pocket for a dosimeter, pen or small items.",
  "Taschen-Stickerei": "Pocket embroidery",
  "Bestickung direkt auf der Tasche – etwa mit Abteilungs- oder Klinikname.": "Embroidery directly on the pocket – e.g. with the department or clinic name.",
  "Austauschbares Namensschild": "Interchangeable name tag",
  "Per Klett wechselbares Namensschild – jederzeit flexibel anpassbar.": "Name tag changeable via hook-and-loop fastener – flexibly adaptable at any time.",
  "Transparente Ausweistasche": "Transparent ID pocket",
  "Klarsichttasche für Dienstausweis oder Dosimeter-Karte.": "Clear pocket for a staff ID or dosimeter card.",
  "Innentasche": "Inner pocket",
  "Verdeckte Innentasche für persönliche Kleinteile.": "Concealed inner pocket for personal small items.",
  "Outlast®-Klimatechnologie": "Outlast® climate technology",
  "Temperaturregulierendes Innenfutter für spürbar angenehmeres Tragen.": "Temperature-regulating lining for noticeably more comfortable wear.",
  "Rock-Tasche": "Skirt pocket",
  "Zusätzliche Tasche am Rockteil des Zweiteilers.": "Additional pocket on the skirt part of the two-piece set.",
  "Innengurt": "Inner belt",
  "Integrierter Stützgurt entlastet den Rücken und verbessert den Sitz.": "An integrated support belt relieves the back and improves the fit.",
  "Unifarben": "Solid colours",
  "Muster": "Patterns",
  "Einfassung": "Binding",
  "Royalblau": "Royal blue", "Marineblau": "Navy blue", "Orange": "Orange", "Rosé": "Rosé",
  "Bordeaux": "Burgundy", "Beere": "Berry", "Rot": "Red", "Violett": "Violet", "Grau": "Grey",
  "Hellgrün": "Light green", "Waldgrün": "Forest green", "Khaki": "Khaki", "Schwarz": "Black", "Gelb": "Yellow",
  "Zebra": "Zebra", "Karo": "Tartan", "Sterne": "Stars", "Safari": "Safari", "Wirbel": "Swirls",
  "Blüten Pink": "Blossom pink", "Blüten Violett": "Blossom violet", "Feuerwerk": "Fireworks",
  "Flammen": "Flames", "Kindermotiv": "Children's motif", "Farbkleckse": "Paint splashes",
  "Camouflage Pink": "Camouflage pink", "Camouflage Grau": "Camouflage grey", "Camouflage Blau": "Camouflage blue",
  "Blau": "Blue", "Grün": "Green", "Dunkelpink": "Dark pink", "Neonpink": "Neon pink", "Petrol": "Teal",
 },
 "pl": {
  "Produkte": "Produkty",
  "Unsere Produkte": "Nasze produkty",
  "Wir vermitteln und liefern zertifizierte Medizinprodukte in mehreren Kategorien: Strahlenschutz, Medizinische Einrichtung und Heilbehelfe &amp; Hilfsmittel. Darüber hinaus beschaffen wir herstellerunabhängig nahezu jedes Produkt und statten ganze Bereiche projektbasiert aus. Klicken Sie eine Kategorie an, um die einzelnen Bereiche zu entdecken.": "Pośredniczymy i dostarczamy certyfikowane wyroby medyczne w kilku kategoriach: ochrona radiologiczna, wyposażenie medyczne oraz środki pomocnicze i wyroby wspomagające. Ponadto zaopatrujemy niemal każdy produkt niezależnie od producenta i wyposażamy całe obszary w oparciu o projekty. Kliknij kategorię, aby odkryć poszczególne obszary.",
  "Strahlenschutz": "Ochrona radiologiczna",
  "Persönliche Strahlenschutz-Bekleidung „Made in UK\" vom Hersteller ROTHBAND – ergänzt um passende Aufbewahrung sowie mobile, deckenmontierte und tischmontierte Röntgenschutzsysteme von KENEX. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.": "Osobista odzież ochronna przed promieniowaniem „Made in UK“ od producenta ROTHBAND – uzupełniona o odpowiednie przechowywanie oraz mobilne, sufitowe i montowane na stole systemy osłon rentgenowskich firmy KENEX. Kliknij obszar, aby rozwinąć modele.",
  "Hersteller": "Producent",
  "Hersteller ROTHBAND – Website in neuem Tab öffnen": "Producent ROTHBAND – otwórz stronę w nowej karcie",
  "Hersteller KENEX – Website in neuem Tab öffnen": "Producent KENEX – otwórz stronę w nowej karcie",
  "Hersteller COINFYCARE – Website in neuem Tab öffnen": "Producent COINFYCARE – otwórz stronę w nowej karcie",
  "Hersteller TECHMED – Website in neuem Tab öffnen": "Producent TECHMED – otwórz stronę w nowej karcie",
  "Medizinische Wagen": "Wózki medyczne",
  "Geräte- &amp; Versorgungswagen": "Wózki pod aparaturę i zaopatrzeniowe",
  "Behandlungs-, Instrumenten- &amp; Stationstische": "Stoliki zabiegowe, narzędziowe i oddziałowe",
  "Transport, Entsorgung &amp; Sterilgutlogistik": "Transport, utylizacja i logistyka materiałów sterylnych",
  "Stations- und Ambulanzausstattung": "Wyposażenie oddziałów i ambulatoriów",
  "MRT-Ausstattung (nicht-magnetisch)": "Wyposażenie do MRI (niemagnetyczne)",
  "Die Modelle zu diesem Bereich werden derzeit aufbereitet und in Kürze ergänzt.": "Modele w tym obszarze są obecnie przygotowywane i zostaną wkrótce dodane.",
  "Hersteller MOBIAK – Website in neuem Tab öffnen": "Producent MOBIAK – otwórz stronę w nowej karcie",
  "Persönlicher Strahlenschutz": "Osobista ochrona radiologiczna",
  "Strahlenschutzbekleidung für den direkten Personenschutz – Schürzen, Zweiteiler, Schilddrüsenschutz und ergänzendes Zubehör. Fokus auf Ergonomie, Gewichtsverteilung, Schutzleistung und Tragekomfort.": "Odzież ochronna przed promieniowaniem do bezpośredniej ochrony osób – fartuchy, komplety dwuczęściowe, osłony tarczycy i uzupełniające akcesoria. Nacisk na ergonomię, rozkład masy, skuteczność ochrony i komfort noszenia.",
  "Front-Schürzen": "Fartuchy przednie",
  "Umhang-/Tabard-Schürzen": "Fartuchy typu tabard",
  "Mantel-/Wickelschürzen": "Fartuchy płaszczowe / zawijane",
  "Zweiteiler – Oberteil &amp; Rock": "Komplet dwuczęściowy – góra i spódnica",
  "Schilddrüsenschutz": "Osłony tarczycy",
  "Zubehör": "Akcesoria",
  "Strahlenschutzbrillen": "Okulary ochronne przed promieniowaniem",
  "Röntgenschutzbrillen für den Schutz der Augen bei Durchleuchtung, interventioneller Bildgebung und Radiologie – in zahlreichen Rahmenformen, mit seitlichem Schutz und wahlweise mit Sehstärke. Bleigläser 0,75 mm Pb, Seitenschutz 0,50 mm Pb.": "Okulary ochronne rentgenowskie do ochrony oczu podczas fluoroskopii, obrazowania interwencyjnego i radiologii – w licznych kształtach oprawek, z ochroną boczną i opcjonalnie z korekcją. Szkła ołowiowe 0,75 mm Pb, ochrona boczna 0,50 mm Pb.",
  "Personalisierung &amp; Optionen": "Personalizacja i opcje",
  "Jede Schürze lässt sich individuell anpassen – für eine bessere Zuordnung, mehr Tragekomfort und praktische Details im Klinikalltag. Alle Optionen sind mit den Modellen aus „Persönlicher Strahlenschutz\" kombinierbar.": "Każdy fartuch można indywidualnie dostosować – dla lepszej identyfikacji, większego komfortu noszenia i praktycznych detali w codziennej pracy klinicznej. Wszystkie opcje można łączyć z modelami z kategorii „Osobista ochrona radiologiczna“.",
  "Farboptionen": "Opcje kolorystyczne",
  "Alle Schürzen und Zubehörteile sind in zahlreichen Farben, Mustern und Einfassungen erhältlich – für ein individuelles, gut erkennbares Erscheinungsbild. Das Stoffsortiment wird von ROTHBAND laufend erweitert.": "Wszystkie fartuchy i akcesoria są dostępne w licznych kolorach, wzorach i lamówkach – dla indywidualnego, dobrze rozpoznawalnego wyglądu. Asortyment tkanin jest stale poszerzany przez ROTHBAND.",
  "Aufbewahrung": "Przechowywanie",
  "Ständer, Schwenkarme und Bügel zur sicheren, platzsparenden Aufbewahrung von Strahlenschutzschürzen.": "Stojaki, ramiona obrotowe i wieszaki do bezpiecznego, oszczędzającego miejsce przechowywania fartuchów ochronnych przed promieniowaniem.",
  "Mobiler Strahlenschutz": "Mobilna ochrona radiologiczna",
  "Fahrbare, frei positionierbare Röntgenschutzsysteme für flexible Einsätze im OP und in der interventionellen Radiologie – vom Hersteller KENEX.": "Jezdne, dowolnie pozycjonowane systemy osłon rentgenowskich do elastycznego zastosowania na sali operacyjnej i w radiologii interwencyjnej – od producenta KENEX.",
  "Deckenmontierter Strahlenschutz": "Sufitowa ochrona radiologiczna",
  "Aufgehängte Überkopf-Schutzschilde und komplette Aufhängungssysteme (Deckenschienen, Säulen, Arme, Monitor-Aufhängung) – zur deutlichen Reduktion der Streustrahlung im Arbeitsbereich. Vom Hersteller KENEX.": "Podwieszane osłony nadgłowowe i kompletne systemy zawieszenia (szyny sufitowe, kolumny, ramiona, zawieszenie monitora) – w celu znacznego ograniczenia promieniowania rozproszonego w obszarze roboczym. Od producenta KENEX.",
  "Überkopf-Schutzschilde": "Osłony nadgłowowe",
  "Aufhängungssysteme": "Systemy zawieszenia",
  "Tischmontierter Strahlenschutz": "Ochrona radiologiczna montowana na stole",
  "Am Untersuchungstisch montierte Schutzschilde für die interventionelle Radiologie – Unterkörper-, Kopfende- und Aufsatz-Schilde sowie passende Aufbewahrung. Vom Hersteller KENEX.": "Osłony montowane na stole badań do radiologii interwencyjnej – osłony na dolną część ciała, na wezgłowie i nakładane oraz odpowiednie przechowywanie. Od producenta KENEX.",
  "Unterkörper-Tischschilde": "Osłony stołowe na dolną część ciała",
  "Kopfende-Tischschilde": "Osłony stołowe na wezgłowie",
  "Aufsatz- &amp; Fußende-Schilde": "Osłony nakładane i na podnóżek",
  "Aufbewahrung &amp; Zubehör": "Przechowywanie i akcesoria",
  "Modelle verfügbar": "dostępnych modeli",
  "Fahrbare Wagen für Anästhesie, Notfall, Station und Behandlung – wahlweise mit geschlossenem Stahlkorpus oder als modulare Aluminium-Plattform, die Sie Schublade für Schublade auf Ihren Ablauf zuschneiden.": "Wózki jezdne do anestezjologii, sytuacji nagłych, oddziału i zabiegów – z zamkniętym korpusem stalowym albo jako modułowa platforma aluminiowa, którą szuflada po szufladzie dopasujesz do swojego procesu.",
  "Ausstattung für Bettenstation und Ambulanz: Nachtkästchen, Bettbeistelltische, Infusionsständer, Auftritte und Injektionsstühle sowie teleskopierbare Wandarme für Infusionen und Sichtschutz – überwiegend aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) oder pulverbeschichtetem Stahl und auf tägliche Wischdesinfektion ausgelegt.": "Wyposażenie oddziałów łóżkowych i ambulatoriów: szafki przyłóżkowe, stoliki przyłóżkowe, stojaki infuzyjne, podesty i fotele do iniekcji oraz teleskopowe ramiona ścienne do infuzji i parawanowania – głównie ze stali nierdzewnej 0H18N9 (austenityczna, 1.4301) lub stali malowanej proszkowo, przystosowane do codziennej dezynfekcji przez przecieranie.",
  "Farbgebung nach TECH-MED-Farbkarte: Fronten, Türen und Polster sind in mehreren RAL- und Bezugsfarben erhältlich – so lassen sich Stationen und Bereiche auf einen Blick unterscheiden. Materialkürzel: ST = pulverbeschichteter Stahl · KO = Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) · ABS = ABS-Kunststoff · HPL = wasserfeste Schichtstoffplatte.": "Kolorystyka według karty kolorów TECH-MED: fronty, drzwi i tapicerka dostępne są w wielu kolorach RAL i tkanin – dzięki temu oddziały i obszary można rozróżnić na pierwszy rzut oka. Oznaczenia materiałów: ST = stal malowana proszkowo · KO = stal nierdzewna 0H18N9 (austenityczna, 1.4301) · ABS = tworzywo ABS · HPL = wodoodporna płyta laminowana.",
  "Fahrbare Geräteträger und Versorgungswagen für Diagnostik, Behandlung und Stationsalltag: schlanke Aluminium-Säulenwagen, die Sie Ebene für Ebene bestücken, und Behandlungswagen mit Edelstahlplatte für Verbandwechsel, Blutabnahme und Medikamentenverteilung.": "Mobilne wózki pod aparaturę i wózki zaopatrzeniowe do diagnostyki, zabiegów i codziennej pracy oddziału: smukłe wózki kolumnowe z aluminium, które wyposażasz poziom po poziomie, oraz wózki zabiegowe z blatem ze stali nierdzewnej do zmiany opatrunków, pobierania krwi i dystrybucji leków.",
  "Zwei Bausysteme, ein Zubehörprogramm: Bei den Säulenwagen (ECO, TOP, MOD, K-1, K-1 LUX, APAR) sitzen alle Ebenen auf gemeinsamen Aluminiumsäulen und lassen sich in der Höhe frei versetzen – Steckdosenleiste, Normschiene, Zubehörkorb, Monitorhalter und Infusionsständer sind über alle Baureihen hinweg identisch und frei kombinierbar. Die Stationswagen K-3, MB-3 und WL sind auf tägliche Wischdesinfektion ausgelegt; Fronten und Säulenblenden gibt es farbig nach TECH-MED-Farbkarte.": "Dwa systemy konstrukcyjne, jeden program wyposażenia: w wózkach kolumnowych (ECO, TOP, MOD, K-1, K-1 LUX, APAR) wszystkie poziomy osadzone są na wspólnych kolumnach aluminiowych i można je dowolnie przestawiać na wysokość – listwa zasilająca, szyna medyczna, koszyk na akcesoria, uchwyt monitora i stojak infuzyjny są identyczne we wszystkich seriach i dowolnie łączone. Wózki oddziałowe K-3, MB-3 i WL przystosowano do codziennej dezynfekcji przez przecieranie; fronty i osłony kolumn dostępne są w kolorach według karty kolorów TECH-MED.",
  "Behandlungstische und Instrumententische für Eingriffsraum, Ambulanz und OP: fahrbare Behandlungstische mit vertiefter Arbeitsplatte und Anbauzubehör sowie höhenverstellbare Instrumententische aus Edelstahl – manuell, hydraulisch oder elektrisch.": "Wózki zabiegowe i stoliki narzędziowe do gabinetu zabiegowego, ambulatorium i bloku operacyjnego: mobilne wózki zabiegowe z wgłębionym blatem i wyposażeniem dodatkowym oraz stoliki narzędziowe ze stali nierdzewnej z regulacją wysokości – ręczną, hydrauliczną lub elektryczną.",
  "Materialausführungen: KO = komplett aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe · ST = komplett aus pulverbeschichtetem Stahl, farbig nach TECH-MED-Farbkarte. Bei den Behandlungstischen STKO bestimmt die gewählte Plattenlänge die Gesamtlänge des Tisches; bei den Instrumententischen verändert die Rollenausführung die Bauhöhe.": "Wersje materiałowe: KO = w całości ze stali nierdzewnej 0H18N9 (austenityczna, 1.4301), najwyższy poziom higieny · ST = w całości ze stali malowanej proszkowo, w kolorach według karty kolorów TECH-MED. W wózkach zabiegowych STKO wybrana długość blatu określa całkowitą długość wózka; w stolikach narzędziowych rodzaj kółek zmienia wysokość stolika.",
  "Transport, Entsorgung und Sterilgutlogistik in einem Bereich: Transport- und Speisenwagen, Korbwagen für den innerbetrieblichen Materialfluss, Wäsche- und Abfallwagen für die Entsorgung sowie Packtische und Regalsysteme für die Sterilgutaufbereitung und das Lager.": "Transport, utylizacja i logistyka materiałów sterylnych w jednym obszarze: wózki transportowe i do przewozu posiłków, wózki koszowe do wewnętrznego przepływu materiałów, wózki na bieliznę i odpady oraz stoły pakowe i systemy regałowe do sterylizatorni i magazynu.",
  "Ein Baukasten für alle Regalsysteme: Körbe, Ablagen, Abwurfbeutelhalter und Trockner werden in dieselben Schienen und Gestelle eingehängt – ob als Wandschiene, Standregal oder fahrbarer Wagen. Die Entsorgungswagen gibt es in zwei Bauweisen: komplett aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe (WZ, WZB, MB) oder in Möbelbauweise mit Aluminium-Profilrahmen und farbigen Füllungen nach RAL (WMW, WCB).": "Jeden system modułowy dla wszystkich regałów: kosze, półki, uchwyty worków i suszarki zawiesza się w tych samych szynach i stelażach – czy to jako szyna ścienna, regał wolnostojący czy wózek jezdny. Wózki utylizacyjne dostępne są w dwóch konstrukcjach: w całości ze stali nierdzewnej 0H18N9 (austenityczna, 1.4301) dla najwyższego poziomu higieny (WZ, WZB, MB) albo w konstrukcji meblowej z ramą z profili aluminiowych i kolorowymi wypełnieniami RAL (WMW, WCB).",
  "Einheitlich aufgebaut: 500 mm Korpustiefe, 1000 mm Arbeitshöhe, vertiefte Arbeitsplatte mit drei Aufkantungen und Ø 125 mm Rollen mit zwei Feststellern. Fronten und Griffe sind farbig nach TECH-MED-Farbkarte erhältlich – so lassen sich Stationen auf einen Blick unterscheiden. Das Zubehörprogramm ist über alle Baureihen hinweg identisch und frei kombinierbar.": "Jednolita konstrukcja: głębokość korpusu 500 mm, wysokość robocza 1000 mm, wgłębiony blat z trzema krawędziami oraz kółka Ø 125 mm z dwiema blokadami. Fronty i uchwyty dostępne są w kolorach według karty kolorów TECH-MED – dzięki temu oddziały rozróżnia się na pierwszy rzut oka. Program akcesoriów jest identyczny dla wszystkich serii i dowolnie łączony.",
  "Materialausführungen: ABS = Stahlkorpus mit Arbeitsplatte aus ABS-Kunststoff · ST = Korpus und Arbeitsplatte aus pulverbeschichtetem Stahl · KO = Korpus und Arbeitsplatte aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe.": "Wersje materiałowe: ABS = korpus stalowy z blatem z tworzywa ABS · ST = korpus i blat ze stali malowanej proszkowo · KO = korpus i blat ze stali nierdzewnej 0H18N9 (austenityczna, 1.4301) dla najwyższego poziomu higieny.",
  "Ausstattung, die im MRT-Raum verbleiben kann: Liege, Tritte, Infusionsständer, Wagen und Sichtschutz – komplett aus nicht-magnetischen Werkstoffen, damit Arbeitsabläufe nicht am Zonenübergang enden.": "Wyposażenie, które może pozostać w pomieszczeniu MRI: leżanka, podesty, stojak infuzyjny, wózki i parawany – w całości z materiałów niemagnetycznych, aby praca nie kończyła się na granicy strefy.",
  "Wichtiger Hinweis: Alle Produkte dieses Bereichs sind für Magnetfeldstärken bis 3 Tesla zugelassen. Für Systeme mit höherer Feldstärke sprechen Sie uns bitte an.": "Ważna informacja: wszystkie produkty w tym obszarze są dopuszczone do natężenia pola magnetycznego do 3 tesli. W przypadku systemów o wyższym natężeniu prosimy o kontakt.",
  "Modell verfügbar": "dostępny model",
  "Produkte verfügbar": "dostępnych produktów",
  "Medizinische Einrichtung": "Wyposażenie medyczne",
  "Ausstattung und Einrichtung für klinische Bereiche – vom Untersuchungsplatz bis zur Sterilgutlogistik. Geliefert von COINFYCARE (Liegen, Stühle, Sichtschutz) und TECHMED (Wagen und Tische, Transport und Entsorgung, Stations- und Ambulanzausstattung, MRT-Ausstattung). Klicken Sie einen Bereich an, um die Modelle aufzuklappen.": "Wyposażenie i umeblowanie obszarów klinicznych – od stanowiska badań po logistykę materiałów sterylnych. Dostarczane przez COINFYCARE (leżanki, krzesła, parawany) oraz TECHMED (wózki i stoliki, transport i utylizacja, wyposażenie oddziałów i ambulatoriów, wyposażenie do MRI). Kliknij obszar, aby rozwinąć modele.",
  "Untersuchungsliegen": "Leżanki do badań",
  "Untersuchungs- und Behandlungsliegen für Praxis und Klinik – nach Bauart gegliedert.": "Leżanki do badań i zabiegów dla gabinetu i kliniki – podzielone według typu konstrukcji.",
  "Fix": "Stałe",
  "Hydraulisch": "Hydrauliczne",
  "Elektrisch": "Elektryczne",
  "Chiropraktische Liegen": "Leżanki chiropraktyczne",
  "Medizinische Stühle": "Krzesła medyczne",
  "Behandlungs-, Blutabnahme- und Arbeitsstühle sowie Hocker für den medizinischen Einsatz.": "Krzesła zabiegowe, do pobierania krwi i robocze oraz taborety do zastosowań medycznych.",
  "Sichtschutz": "Parawany",
  "Sicht- und Trennwandsysteme für diskrete, flexibel teilbare Raumbereiche.": "Systemy parawanów i ścianek działowych do dyskretnego, elastycznego dzielenia przestrzeni.",
  "Heilbehelfe &amp; Hilfsmittel": "Środki pomocnicze i wyroby wspomagające",
  "Mobilität, Pflege und Alltagshilfen – von Rollstühlen und Elektromobilen über Gehhilfen bis zu Anti-Dekubitus-Systemen und Sauerstoffversorgung. Geliefert vom Hersteller MOBIAK. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.": "Mobilność, opieka i pomoce codzienne – od wózków inwalidzkich i skuterów elektrycznych, przez pomoce do chodzenia, po systemy przeciwodleżynowe i zaopatrzenie w tlen. Dostarczane przez producenta MOBIAK. Kliknij obszar, aby rozwinąć modele.",
  "Rollstühle": "Wózki inwalidzkie",
  "Elektrische Rollstühle &amp; Scooter": "Elektryczne wózki inwalidzkie i skutery",
  "Gehhilfen": "Pomoce do chodzenia",
  "Rollatoren": "Balkoniki (rollatory)",
  "Gehböcke / Walker": "Podpórki / balkoniki",
  "Anti-Dekubitus-Produkte": "Produkty przeciwodleżynowe",
  "Sauerstoffkonzentratoren": "Koncentratory tlenu",
  "Herstellerunabhängige Produktbeschaffung": "Zaopatrzenie w produkty niezależne od producentów",
  "Sie suchen ein Produkt, das nicht in unserem Katalog enthalten ist? Dank unserer Herstellerunabhängigkeit sind wir nicht an bestimmte Marken gebunden und können Produkte verschiedenster Hersteller für Sie beschaffen.": "Szukasz produktu, którego nie ma w naszym katalogu? Dzięki niezależności od producentów nie jesteśmy związani z konkretnymi markami i możemy pozyskać dla Ciebie produkty najróżniejszych producentów.",
  "Alles beschaffbar": "Wszystko do pozyskania",
  "Ob Standardartikel, Spezialgerät oder schwer erhältliches Ersatzteil – wir identifizieren die passende Bezugsquelle und liefern zuverlässig. Kein Sortiment setzt uns Grenzen: Sie nennen den Bedarf, wir finden die Lösung.": "Czy to artykuł standardowy, urządzenie specjalistyczne czy trudno dostępna część zamienna – identyfikujemy właściwe źródło i dostarczamy niezawodnie. Żaden asortyment nas nie ogranicza: Ty określasz potrzebę, my znajdujemy rozwiązanie.",
  "Komplette Bereichsausstattung": "Kompletne wyposażenie obszaru",
  "Von der Praxis bis zur Klinikabteilung statten wir ganze Bereiche aus – abgestimmt auf Arbeitsabläufe, Hygieneanforderungen und Budget. Grundausstattung, Mobiliar und High-End-Technik aus einer Hand.": "Od gabinetu po oddział kliniczny wyposażamy całe obszary – dostosowane do przepływów pracy, wymagań higienicznych i budżetu. Wyposażenie podstawowe, meble i technologia klasy premium z jednej ręki.",
  "Herstellerunabhängig": "Niezależni od producentów",
  "Wir sind an keine Marke gebunden. So wählen wir stets das Produkt, das technisch, wirtschaftlich und qualitativ am besten zu Ihrer Anforderung passt – objektiv und in Ihrem Interesse.": "Nie jesteśmy związani z żadną marką. Dzięki temu zawsze wybieramy produkt, który technicznie, ekonomicznie i jakościowo najlepiej odpowiada Twoim wymaganiom – obiektywnie i w Twoim interesie.",
  "Projekt- &amp; Komplettservice": "Usługa projektowa i kompleksowa",
  "Ein Ansprechpartner für den gesamten Beschaffungsprozess: Bedarfsanalyse, Angebot, Einkauf, Logistik und Lieferung – auf Wunsch inklusive Installation und Einschulung. Termintreu, transparent und aus einer Hand.": "Jeden partner do kontaktu w całym procesie zaopatrzenia: analiza potrzeb, oferta, zakup, logistyka i dostawa – na życzenie wraz z instalacją i przeszkoleniem. Terminowo, przejrzyście i z jednej ręki.",
  "Sie haben einen konkreten Bedarf oder planen ein Projekt? Beschreiben Sie uns Ihr Vorhaben – wir erstellen Ihnen ein individuelles, unverbindliches Angebot.": "Masz konkretną potrzebę lub planujesz projekt? Opisz nam swoje zamierzenie – przygotujemy dla Ciebie indywidualną, niezobowiązującą ofertę.",
  "Projekt anfragen": "Zapytaj o projekt",
  "Downloads &amp; Unterlagen": "Pliki do pobrania i dokumenty",
  "Zur Kontaktseite": "Do strony kontaktowej",
  "Chiropraktisch": "Chiropraktyczne",
  "Herstellerkataloge": "Katalogi producenta",
  "Innenmaterial": "Materiał wewnętrzny",
  "Persönliche Schutzausrüstung": "Środki ochrony indywidualnej",
  "Schnittbildgebung": "Obrazowanie przekrojowe",
  "ROTHBAND · PDF": "ROTHBAND · PDF",
  "OUTLAST®": "OUTLAST®",
  "Hier finden Sie unsere Produktkataloge und Unterlagen zu unseren Produkten des Strahlenschutzes. Neue Dokumente ergänzen wir laufend.": "Tutaj znajdą Państwo nasze katalogi produktów oraz dokumenty dotyczące naszych produktów ochrony radiologicznej. Nowe dokumenty dodajemy na bieżąco.",
  "Persönliche Schutzausrüstung und Aufbewahrung": "Środki ochrony osobistej i przechowywanie",
  "Innenmaterial der persönlichen Schutzausrüstung": "Materiał wewnętrzny środków ochrony osobistej",
  "KENEX · PDF": "KENEX · PDF",
  "Hier finden Sie unsere Produktkataloge und Farbkarten sowie die technischen Datenblätter zu unseren Produkten der Medizinischen Einrichtung. Der COINFYCARE-Katalog deckt die Bereiche 01–03 ab, der TECH-MED-Katalog samt Farbkarten die Bereiche 04–09 einschließlich Schienensysteme. Neue Dokumente ergänzen wir laufend.": "Tutaj znajdą Państwo nasze katalogi produktów i wzorniki kolorów oraz karty techniczne naszych produktów wyposażenia medycznego. Katalog COINFYCARE obejmuje obszary 01–03, a katalog TECH-MED wraz z wzornikami kolorów – obszary 04–09, w tym systemy szynowe. Nowe dokumenty dodajemy na bieżąco.",
  "Produktkatalog": "Katalog produktów",
  "Produktkataloge & Farbkarten": "Katalogi produktów i wzorniki kolorów",
  "Produktkatalog · Bereiche 01–03": "Katalog produktów · Obszary 01–03",
  "Produktkatalog · Bereiche 04–09": "Katalog produktów · Obszary 04–09",
  "Farbkarten · Bereiche 04–09": "Wzorniki kolorów · Obszary 04–09",
  "COINFYCARE · PDF": "COINFYCARE · PDF",
  "TECH-MED · PDF": "TECH-MED · PDF",
  "Die Unterlagen zu unseren Produkten des Strahlenschutzes senden wir Ihnen gerne auf Anfrage zu.": "Dokumenty dotyczące naszych produktów ochrony radiologicznej chętnie prześlemy na życzenie.",
  "Die Unterlagen zu unseren Produkten der Medizinischen Einrichtung senden wir Ihnen gerne auf Anfrage zu.": "Dokumenty dotyczące naszych produktów wyposażenia medycznego chętnie prześlemy na życzenie.",
  "Die Unterlagen zu unseren Heilbehelfen und Hilfsmitteln senden wir Ihnen gerne auf Anfrage zu.": "Dokumenty dotyczące naszych środków pomocniczych i wyrobów wspomagających chętnie prześlemy na życzenie.",
  "Personalisierung": "Personalizacja",
  "Optionale Extras": "Opcjonalne dodatki",
  "Stickerei": "Haft",
  "Individuelle Textstickerei direkt auf der Schürze – z. B. Name, Abteilung oder Einsatzbereich.": "Indywidualny haft tekstowy bezpośrednio na fartuchu – np. imię, oddział lub obszar zastosowania.",
  "Aufgesetzte Tasche": "Kieszeń naszywana",
  "Praktische Außentasche für Dosimeter, Stift oder Kleinteile.": "Praktyczna kieszeń zewnętrzna na dozymetr, długopis lub drobiazgi.",
  "Taschen-Stickerei": "Haft na kieszeni",
  "Bestickung direkt auf der Tasche – etwa mit Abteilungs- oder Klinikname.": "Haft bezpośrednio na kieszeni – np. z nazwą oddziału lub kliniki.",
  "Austauschbares Namensschild": "Wymienna plakietka z nazwiskiem",
  "Per Klett wechselbares Namensschild – jederzeit flexibel anpassbar.": "Plakietka z nazwiskiem wymieniana na rzep – elastycznie dostosowywalna w każdej chwili.",
  "Transparente Ausweistasche": "Przezroczysta kieszeń na identyfikator",
  "Klarsichttasche für Dienstausweis oder Dosimeter-Karte.": "Przezroczysta kieszeń na identyfikator służbowy lub kartę dozymetru.",
  "Innentasche": "Kieszeń wewnętrzna",
  "Verdeckte Innentasche für persönliche Kleinteile.": "Ukryta kieszeń wewnętrzna na osobiste drobiazgi.",
  "Outlast®-Klimatechnologie": "Technologia klimatyczna Outlast®",
  "Temperaturregulierendes Innenfutter für spürbar angenehmeres Tragen.": "Podszewka regulująca temperaturę dla zauważalnie przyjemniejszego noszenia.",
  "Rock-Tasche": "Kieszeń w spódnicy",
  "Zusätzliche Tasche am Rockteil des Zweiteilers.": "Dodatkowa kieszeń przy spódnicy kompletu dwuczęściowego.",
  "Innengurt": "Pas wewnętrzny",
  "Integrierter Stützgurt entlastet den Rücken und verbessert den Sitz.": "Zintegrowany pas podtrzymujący odciąża plecy i poprawia dopasowanie.",
  "Unifarben": "Kolory jednolite",
  "Muster": "Wzory",
  "Einfassung": "Lamówka",
  "Royalblau": "Królewski niebieski", "Marineblau": "Granatowy", "Orange": "Pomarańczowy", "Rosé": "Różany",
  "Bordeaux": "Bordowy", "Beere": "Jagodowy", "Rot": "Czerwony", "Violett": "Fioletowy", "Grau": "Szary",
  "Hellgrün": "Jasnozielony", "Waldgrün": "Zielony leśny", "Khaki": "Khaki", "Schwarz": "Czarny", "Gelb": "Żółty",
  "Zebra": "Zebra", "Karo": "Krata", "Sterne": "Gwiazdy", "Safari": "Safari", "Wirbel": "Zawirowania",
  "Blüten Pink": "Kwiaty różowe", "Blüten Violett": "Kwiaty fioletowe", "Feuerwerk": "Fajerwerki",
  "Flammen": "Płomienie", "Kindermotiv": "Motyw dziecięcy", "Farbkleckse": "Plamy farby",
  "Camouflage Pink": "Moro różowe", "Camouflage Grau": "Moro szare", "Camouflage Blau": "Moro niebieskie",
  "Blau": "Niebieski", "Grün": "Zielony", "Dunkelpink": "Ciemnoróżowy", "Neonpink": "Neonowy róż", "Petrol": "Petrol",
 },
 "ro": {
  "Produkte": "Produse",
  "Unsere Produkte": "Produsele noastre",
  "Wir vermitteln und liefern zertifizierte Medizinprodukte in mehreren Kategorien: Strahlenschutz, Medizinische Einrichtung und Heilbehelfe &amp; Hilfsmittel. Darüber hinaus beschaffen wir herstellerunabhängig nahezu jedes Produkt und statten ganze Bereiche projektbasiert aus. Klicken Sie eine Kategorie an, um die einzelnen Bereiche zu entdecken.": "Intermediem și livrăm produse medicale certificate în mai multe categorii: protecție radiologică, mobilier medical și mijloace ajutătoare &amp; dispozitive de asistență. În plus, achiziționăm aproape orice produs independent de producător și dotăm zone întregi pe bază de proiect. Faceți clic pe o categorie pentru a descoperi secțiunile individuale.",
  "Strahlenschutz": "Protecție radiologică",
  "Persönliche Strahlenschutz-Bekleidung „Made in UK\" vom Hersteller ROTHBAND – ergänzt um passende Aufbewahrung sowie mobile, deckenmontierte und tischmontierte Röntgenschutzsysteme von KENEX. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.": "Îmbrăcăminte personală de protecție radiologică „Made in UK“ de la producătorul ROTHBAND – completată de soluții de depozitare adecvate, precum și de sisteme de protecție cu raze X mobile, montate pe tavan și pe masă de la KENEX. Faceți clic pe o secțiune pentru a extinde modelele.",
  "Hersteller": "Producător",
  "Hersteller ROTHBAND – Website in neuem Tab öffnen": "Producător ROTHBAND – deschide site-ul într-o filă nouă",
  "Hersteller KENEX – Website in neuem Tab öffnen": "Producător KENEX – deschide site-ul într-o filă nouă",
  "Hersteller COINFYCARE – Website in neuem Tab öffnen": "Producător COINFYCARE – deschide site-ul într-o filă nouă",
  "Hersteller TECHMED – Website in neuem Tab öffnen": "Producător TECHMED – deschide site-ul într-o filă nouă",
  "Medizinische Wagen": "Cărucioare medicale",
  "Geräte- &amp; Versorgungswagen": "Cărucioare pentru aparatură și aprovizionare",
  "Behandlungs-, Instrumenten- &amp; Stationstische": "Mese de tratament, pentru instrumentar și de secție",
  "Transport, Entsorgung &amp; Sterilgutlogistik": "Transport, eliminarea deșeurilor și logistica materialelor sterile",
  "Stations- und Ambulanzausstattung": "Dotări pentru secții și ambulatoriu",
  "MRT-Ausstattung (nicht-magnetisch)": "Dotări pentru RMN (nemagnetice)",
  "Die Modelle zu diesem Bereich werden derzeit aufbereitet und in Kürze ergänzt.": "Modelele pentru această secțiune sunt în curs de pregătire și vor fi adăugate în curând.",
  "Hersteller MOBIAK – Website in neuem Tab öffnen": "Producător MOBIAK – deschide site-ul într-o filă nouă",
  "Persönlicher Strahlenschutz": "Protecție radiologică personală",
  "Strahlenschutzbekleidung für den direkten Personenschutz – Schürzen, Zweiteiler, Schilddrüsenschutz und ergänzendes Zubehör. Fokus auf Ergonomie, Gewichtsverteilung, Schutzleistung und Tragekomfort.": "Îmbrăcăminte de protecție radiologică pentru protecția directă a persoanei – șorțuri, seturi din două piese, protecții pentru tiroidă și accesorii complementare. Accent pe ergonomie, distribuția greutății, performanța de protecție și confortul purtării.",
  "Front-Schürzen": "Șorțuri frontale",
  "Umhang-/Tabard-Schürzen": "Șorțuri tip tabard",
  "Mantel-/Wickelschürzen": "Șorțuri tip halat / înfășurare",
  "Zweiteiler – Oberteil &amp; Rock": "Set din două piese – bluză &amp; fustă",
  "Schilddrüsenschutz": "Protecții pentru tiroidă",
  "Zubehör": "Accesorii",
  "Strahlenschutzbrillen": "Ochelari de protecție radiologică",
  "Röntgenschutzbrillen für den Schutz der Augen bei Durchleuchtung, interventioneller Bildgebung und Radiologie – in zahlreichen Rahmenformen, mit seitlichem Schutz und wahlweise mit Sehstärke. Bleigläser 0,75 mm Pb, Seitenschutz 0,50 mm Pb.": "Ochelari de protecție împotriva razelor X pentru protejarea ochilor în timpul fluoroscopiei, imagisticii intervenționale și radiologiei – în numeroase forme de rame, cu protecție laterală și opțional cu dioptrii. Sticlă cu plumb 0,75 mm Pb, protecție laterală 0,50 mm Pb.",
  "Personalisierung &amp; Optionen": "Personalizare și opțiuni",
  "Jede Schürze lässt sich individuell anpassen – für eine bessere Zuordnung, mehr Tragekomfort und praktische Details im Klinikalltag. Alle Optionen sind mit den Modellen aus „Persönlicher Strahlenschutz\" kombinierbar.": "Fiecare șorț poate fi personalizat individual – pentru o identificare mai bună, un confort sporit la purtare și detalii practice în activitatea clinică zilnică. Toate opțiunile pot fi combinate cu modelele din „Protecție radiologică personală“.",
  "Farboptionen": "Opțiuni de culoare",
  "Alle Schürzen und Zubehörteile sind in zahlreichen Farben, Mustern und Einfassungen erhältlich – für ein individuelles, gut erkennbares Erscheinungsbild. Das Stoffsortiment wird von ROTHBAND laufend erweitert.": "Toate șorțurile și accesoriile sunt disponibile în numeroase culori, modele și borduri – pentru un aspect individual, ușor de recunoscut. Gama de materiale este extinsă continuu de ROTHBAND.",
  "Aufbewahrung": "Depozitare",
  "Ständer, Schwenkarme und Bügel zur sicheren, platzsparenden Aufbewahrung von Strahlenschutzschürzen.": "Suporturi, brațe pivotante și umerașe pentru depozitarea sigură și economică a șorțurilor de protecție radiologică.",
  "Mobiler Strahlenschutz": "Protecție radiologică mobilă",
  "Fahrbare, frei positionierbare Röntgenschutzsysteme für flexible Einsätze im OP und in der interventionellen Radiologie – vom Hersteller KENEX.": "Sisteme de protecție cu raze X mobile, poziționabile liber, pentru utilizare flexibilă în sala de operație și în radiologia intervențională – de la producătorul KENEX.",
  "Deckenmontierter Strahlenschutz": "Protecție radiologică montată pe tavan",
  "Aufgehängte Überkopf-Schutzschilde und komplette Aufhängungssysteme (Deckenschienen, Säulen, Arme, Monitor-Aufhängung) – zur deutlichen Reduktion der Streustrahlung im Arbeitsbereich. Vom Hersteller KENEX.": "Ecrane de protecție suspendate deasupra capului și sisteme complete de suspensie (șine de tavan, coloane, brațe, suspensie pentru monitor) – pentru reducerea semnificativă a radiației împrăștiate în zona de lucru. De la producătorul KENEX.",
  "Überkopf-Schutzschilde": "Ecrane de protecție deasupra capului",
  "Aufhängungssysteme": "Sisteme de suspensie",
  "Tischmontierter Strahlenschutz": "Protecție radiologică montată pe masă",
  "Am Untersuchungstisch montierte Schutzschilde für die interventionelle Radiologie – Unterkörper-, Kopfende- und Aufsatz-Schilde sowie passende Aufbewahrung. Vom Hersteller KENEX.": "Ecrane de protecție montate pe masa de examinare pentru radiologia intervențională – ecrane pentru partea inferioară a corpului, pentru capătul de la cap și tip supliment, precum și depozitare adecvată. De la producătorul KENEX.",
  "Unterkörper-Tischschilde": "Ecrane de masă pentru partea inferioară a corpului",
  "Kopfende-Tischschilde": "Ecrane de masă pentru capătul de la cap",
  "Aufsatz- &amp; Fußende-Schilde": "Ecrane tip supliment &amp; pentru capătul de la picioare",
  "Aufbewahrung &amp; Zubehör": "Depozitare și accesorii",
  "Ausstattung für Bettenstation und Ambulanz: Nachtkästchen, Bettbeistelltische, Infusionsständer, Auftritte und Injektionsstühle sowie teleskopierbare Wandarme für Infusionen und Sichtschutz – überwiegend aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) oder pulverbeschichtetem Stahl und auf tägliche Wischdesinfektion ausgelegt.": "Dotări pentru secțiile cu paturi și ambulatoriu: noptiere, mese pentru pat, stative pentru perfuzii, taburete cu trepte și scaune pentru injecții, precum și brațe telescopice de perete pentru perfuzii și paravanare – majoritatea din oțel inoxidabil 0H18N9 (austenitic, 1.4301) sau oțel vopsit electrostatic, concepute pentru dezinfecția zilnică prin ștergere.",
  "Farbgebung nach TECH-MED-Farbkarte: Fronten, Türen und Polster sind in mehreren RAL- und Bezugsfarben erhältlich – so lassen sich Stationen und Bereiche auf einen Blick unterscheiden. Materialkürzel: ST = pulverbeschichteter Stahl · KO = Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) · ABS = ABS-Kunststoff · HPL = wasserfeste Schichtstoffplatte.": "Culori conform paletarului TECH-MED: fronturile, ușile și tapițeria sunt disponibile în mai multe culori RAL și de material – astfel secțiile și zonele se pot deosebi dintr-o privire. Coduri de material: ST = oțel vopsit electrostatic · KO = oțel inoxidabil 0H18N9 (austenitic, 1.4301) · ABS = plastic ABS · HPL = placă laminată rezistentă la apă.",
  "Fahrbare Geräteträger und Versorgungswagen für Diagnostik, Behandlung und Stationsalltag: schlanke Aluminium-Säulenwagen, die Sie Ebene für Ebene bestücken, und Behandlungswagen mit Edelstahlplatte für Verbandwechsel, Blutabnahme und Medikamentenverteilung.": "Cărucioare mobile pentru aparatură și cărucioare de aprovizionare pentru diagnostic, tratament și activitatea zilnică din secție: cărucioare zvelte cu coloane din aluminiu, pe care le dotați nivel cu nivel, și cărucioare de tratament cu blat din oțel inoxidabil pentru schimbarea pansamentelor, recoltarea sângelui și distribuirea medicamentelor.",
  "Zwei Bausysteme, ein Zubehörprogramm: Bei den Säulenwagen (ECO, TOP, MOD, K-1, K-1 LUX, APAR) sitzen alle Ebenen auf gemeinsamen Aluminiumsäulen und lassen sich in der Höhe frei versetzen – Steckdosenleiste, Normschiene, Zubehörkorb, Monitorhalter und Infusionsständer sind über alle Baureihen hinweg identisch und frei kombinierbar. Die Stationswagen K-3, MB-3 und WL sind auf tägliche Wischdesinfektion ausgelegt; Fronten und Säulenblenden gibt es farbig nach TECH-MED-Farbkarte.": "Două sisteme constructive, un singur program de accesorii: la cărucioarele cu coloane (ECO, TOP, MOD, K-1, K-1 LUX, APAR) toate nivelurile sunt fixate pe coloane comune din aluminiu și pot fi repoziționate liber pe înălțime – prelungitorul cu prize, șina medicală, coșul pentru accesorii, suportul de monitor și stativul pentru perfuzii sunt identice la toate seriile și se pot combina liber. Cărucioarele de secție K-3, MB-3 și WL sunt concepute pentru dezinfecția zilnică prin ștergere; fronturile și măștile coloanelor sunt disponibile colorat, conform paletarului TECH-MED.",
  "Behandlungstische und Instrumententische für Eingriffsraum, Ambulanz und OP: fahrbare Behandlungstische mit vertiefter Arbeitsplatte und Anbauzubehör sowie höhenverstellbare Instrumententische aus Edelstahl – manuell, hydraulisch oder elektrisch.": "Cărucioare de tratament și mese pentru instrumentar pentru sala de proceduri, ambulatoriu și blocul operator: cărucioare mobile de tratament cu blat adâncit și accesorii, precum și mese pentru instrumentar din oțel inoxidabil, reglabile pe înălțime – manual, hidraulic sau electric.",
  "Materialausführungen: KO = komplett aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe · ST = komplett aus pulverbeschichtetem Stahl, farbig nach TECH-MED-Farbkarte. Bei den Behandlungstischen STKO bestimmt die gewählte Plattenlänge die Gesamtlänge des Tisches; bei den Instrumententischen verändert die Rollenausführung die Bauhöhe.": "Variante de material: KO = integral din oțel inoxidabil 0H18N9 (austenitic, 1.4301), pentru cel mai înalt nivel de igienă · ST = integral din oțel vopsit electrostatic, colorat conform paletarului TECH-MED. La cărucioarele de tratament STKO, lungimea aleasă a blatului determină lungimea totală a căruciorului; la mesele pentru instrumentar, tipul de roți modifică înălțimea.",
  "Transport, Entsorgung und Sterilgutlogistik in einem Bereich: Transport- und Speisenwagen, Korbwagen für den innerbetrieblichen Materialfluss, Wäsche- und Abfallwagen für die Entsorgung sowie Packtische und Regalsysteme für die Sterilgutaufbereitung und das Lager.": "Transport, eliminarea deșeurilor și logistica materialelor sterile într-o singură secțiune: cărucioare de transport și pentru hrană, cărucioare cu coșuri pentru fluxul intern de materiale, cărucioare pentru lenjerie și deșeuri, precum și mese de ambalare și sisteme de rafturi pentru sterilizare și depozit.",
  "Ein Baukasten für alle Regalsysteme: Körbe, Ablagen, Abwurfbeutelhalter und Trockner werden in dieselben Schienen und Gestelle eingehängt – ob als Wandschiene, Standregal oder fahrbarer Wagen. Die Entsorgungswagen gibt es in zwei Bauweisen: komplett aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe (WZ, WZB, MB) oder in Möbelbauweise mit Aluminium-Profilrahmen und farbigen Füllungen nach RAL (WMW, WCB).": "Un singur sistem modular pentru toate rafturile: coșurile, polițele, suporturile pentru saci și uscătoarele se agață în aceleași șine și cadre – fie ca șină de perete, raft independent sau cărucior mobil. Cărucioarele de eliminare a deșeurilor există în două construcții: integral din oțel inoxidabil 0H18N9 (austenitic, 1.4301) pentru cel mai înalt nivel de igienă (WZ, WZB, MB) sau în construcție de mobilier, cu cadru din profile de aluminiu și panouri colorate RAL (WMW, WCB).",
  "Modelle verfügbar": "modele disponibile",
  "Fahrbare Wagen für Anästhesie, Notfall, Station und Behandlung – wahlweise mit geschlossenem Stahlkorpus oder als modulare Aluminium-Plattform, die Sie Schublade für Schublade auf Ihren Ablauf zuschneiden.": "Cărucioare mobile pentru anestezie, urgență, secție și tratament – fie cu corp închis din oțel, fie ca platformă modulară din aluminiu, pe care o adaptați sertar cu sertar fluxului dumneavoastră.",
  "Einheitlich aufgebaut: 500 mm Korpustiefe, 1000 mm Arbeitshöhe, vertiefte Arbeitsplatte mit drei Aufkantungen und Ø 125 mm Rollen mit zwei Feststellern. Fronten und Griffe sind farbig nach TECH-MED-Farbkarte erhältlich – so lassen sich Stationen auf einen Blick unterscheiden. Das Zubehörprogramm ist über alle Baureihen hinweg identisch und frei kombinierbar.": "Construcție unitară: adâncimea corpului 500 mm, înălțime de lucru 1000 mm, blat adâncit cu trei margini ridicate și roți Ø 125 mm cu două frâne. Fronturile și mânerele sunt disponibile colorate conform paletei TECH-MED, astfel încât secțiile se disting dintr-o privire. Programul de accesorii este identic pentru toate seriile și se combină liber.",
  "Materialausführungen: ABS = Stahlkorpus mit Arbeitsplatte aus ABS-Kunststoff · ST = Korpus und Arbeitsplatte aus pulverbeschichtetem Stahl · KO = Korpus und Arbeitsplatte aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe.": "Variante de material: ABS = corp din oțel cu blat din plastic ABS · ST = corp și blat din oțel vopsit electrostatic · KO = corp și blat din oțel inoxidabil 0H18N9 (austenitic, 1.4301) pentru cel mai înalt nivel de igienă.",
  "Ausstattung, die im MRT-Raum verbleiben kann: Liege, Tritte, Infusionsständer, Wagen und Sichtschutz – komplett aus nicht-magnetischen Werkstoffen, damit Arbeitsabläufe nicht am Zonenübergang enden.": "Dotări care pot rămâne în camera RMN: canapea, taburete, stativ pentru perfuzii, cărucioare și paravane – realizate integral din materiale nemagnetice, astfel încât fluxul de lucru să nu se oprească la limita zonei.",
  "Wichtiger Hinweis: Alle Produkte dieses Bereichs sind für Magnetfeldstärken bis 3 Tesla zugelassen. Für Systeme mit höherer Feldstärke sprechen Sie uns bitte an.": "Notă importantă: toate produsele din această secțiune sunt aprobate pentru intensități ale câmpului magnetic de până la 3 tesla. Pentru sisteme cu intensitate mai mare, vă rugăm să ne contactați.",
  "Modell verfügbar": "model disponibil",
  "Produkte verfügbar": "produse disponibile",
  "Medizinische Einrichtung": "Mobilier medical",
  "Ausstattung und Einrichtung für klinische Bereiche – vom Untersuchungsplatz bis zur Sterilgutlogistik. Geliefert von COINFYCARE (Liegen, Stühle, Sichtschutz) und TECHMED (Wagen und Tische, Transport und Entsorgung, Stations- und Ambulanzausstattung, MRT-Ausstattung). Klicken Sie einen Bereich an, um die Modelle aufzuklappen.": "Echipamente și mobilier pentru zonele clinice – de la postul de examinare până la logistica materialelor sterile. Livrate de COINFYCARE (canapele, scaune, paravane) și TECHMED (cărucioare și mese, transport și eliminarea deșeurilor, dotări pentru secții și ambulatoriu, dotări pentru RMN). Faceți clic pe o secțiune pentru a extinde modelele.",
  "Untersuchungsliegen": "Canapele de examinare",
  "Untersuchungs- und Behandlungsliegen für Praxis und Klinik – nach Bauart gegliedert.": "Canapele de examinare și tratament pentru cabinet și clinică – organizate după tipul constructiv.",
  "Fix": "Fixe",
  "Hydraulisch": "Hidraulice",
  "Elektrisch": "Electrice",
  "Chiropraktische Liegen": "Canapele chiropractice",
  "Medizinische Stühle": "Scaune medicale",
  "Behandlungs-, Blutabnahme- und Arbeitsstühle sowie Hocker für den medizinischen Einsatz.": "Scaune de tratament, de recoltare a sângelui și de lucru, precum și taburete pentru uz medical.",
  "Sichtschutz": "Paravane",
  "Sicht- und Trennwandsysteme für diskrete, flexibel teilbare Raumbereiche.": "Sisteme de paravane și pereți despărțitori pentru zone discrete, divizabile flexibil.",
  "Heilbehelfe &amp; Hilfsmittel": "Mijloace ajutătoare &amp; dispozitive de asistență",
  "Mobilität, Pflege und Alltagshilfen – von Rollstühlen und Elektromobilen über Gehhilfen bis zu Anti-Dekubitus-Systemen und Sauerstoffversorgung. Geliefert vom Hersteller MOBIAK. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.": "Mobilitate, îngrijire și ajutoare cotidiene – de la scaune rulante și scutere electrice, la dispozitive de mers, sisteme anti-decubit și alimentare cu oxigen. Livrat de producătorul MOBIAK. Faceți clic pe o secțiune pentru a extinde modelele.",
  "Rollstühle": "Scaune rulante",
  "Elektrische Rollstühle &amp; Scooter": "Scaune rulante electrice &amp; scutere",
  "Gehhilfen": "Dispozitive de mers",
  "Rollatoren": "Rollatoare",
  "Gehböcke / Walker": "Cadre de mers / walkere",
  "Anti-Dekubitus-Produkte": "Produse anti-decubit",
  "Sauerstoffkonzentratoren": "Concentratoare de oxigen",
  "Herstellerunabhängige Produktbeschaffung": "Achiziție de produse independentă de producători",
  "Sie suchen ein Produkt, das nicht in unserem Katalog enthalten ist? Dank unserer Herstellerunabhängigkeit sind wir nicht an bestimmte Marken gebunden und können Produkte verschiedenster Hersteller für Sie beschaffen.": "Căutați un produs care nu se află în catalogul nostru? Datorită independenței față de producători, nu suntem legați de anumite mărci și putem achiziționa pentru dumneavoastră produse de la cei mai diverși producători.",
  "Alles beschaffbar": "Orice se poate achiziționa",
  "Ob Standardartikel, Spezialgerät oder schwer erhältliches Ersatzteil – wir identifizieren die passende Bezugsquelle und liefern zuverlässig. Kein Sortiment setzt uns Grenzen: Sie nennen den Bedarf, wir finden die Lösung.": "Fie că este vorba de un articol standard, un dispozitiv special sau o piesă de schimb greu de găsit – identificăm sursa potrivită și livrăm în mod fiabil. Niciun sortiment nu ne limitează: dumneavoastră precizați necesarul, noi găsim soluția.",
  "Komplette Bereichsausstattung": "Dotarea completă a zonei",
  "Von der Praxis bis zur Klinikabteilung statten wir ganze Bereiche aus – abgestimmt auf Arbeitsabläufe, Hygieneanforderungen und Budget. Grundausstattung, Mobiliar und High-End-Technik aus einer Hand.": "De la cabinet până la secția de spital, dotăm zone întregi – adaptate fluxurilor de lucru, cerințelor de igienă și bugetului. Echipamente de bază, mobilier și tehnologie high-end dintr-o singură sursă.",
  "Herstellerunabhängig": "Independent de producători",
  "Wir sind an keine Marke gebunden. So wählen wir stets das Produkt, das technisch, wirtschaftlich und qualitativ am besten zu Ihrer Anforderung passt – objektiv und in Ihrem Interesse.": "Nu suntem legați de nicio marcă. Astfel, alegem întotdeauna produsul care se potrivește cel mai bine cerinței dumneavoastră din punct de vedere tehnic, economic și calitativ – obiectiv și în interesul dumneavoastră.",
  "Projekt- &amp; Komplettservice": "Serviciu de proiect &amp; complet",
  "Ein Ansprechpartner für den gesamten Beschaffungsprozess: Bedarfsanalyse, Angebot, Einkauf, Logistik und Lieferung – auf Wunsch inklusive Installation und Einschulung. Termintreu, transparent und aus einer Hand.": "Un singur punct de contact pentru întregul proces de achiziție: analiza necesarului, ofertă, achiziție, logistică și livrare – la cerere, inclusiv instalare și instruire. La termen, transparent și dintr-o singură sursă.",
  "Sie haben einen konkreten Bedarf oder planen ein Projekt? Beschreiben Sie uns Ihr Vorhaben – wir erstellen Ihnen ein individuelles, unverbindliches Angebot.": "Aveți o nevoie concretă sau planificați un proiect? Descrieți-ne intenția dumneavoastră – vă întocmim o ofertă individuală, fără angajament.",
  "Projekt anfragen": "Solicitați un proiect",
  "Downloads &amp; Unterlagen": "Descărcări și documente",
  "Zur Kontaktseite": "Către pagina de contact",
  "Chiropraktisch": "Chiropractice",
  "Herstellerkataloge": "Cataloage producător",
  "Innenmaterial": "Material interior",
  "Persönliche Schutzausrüstung": "Echipament de protecție individuală",
  "Schnittbildgebung": "Imagistică secțională",
  "ROTHBAND · PDF": "ROTHBAND · PDF",
  "OUTLAST®": "OUTLAST®",
  "Hier finden Sie unsere Produktkataloge und Unterlagen zu unseren Produkten des Strahlenschutzes. Neue Dokumente ergänzen wir laufend.": "Aici găsiți cataloagele noastre de produse și documentele pentru produsele noastre de protecție radiologică. Adăugăm continuu documente noi.",
  "Persönliche Schutzausrüstung und Aufbewahrung": "Echipament individual de protecție și depozitare",
  "Innenmaterial der persönlichen Schutzausrüstung": "Material interior al echipamentului individual de protecție",
  "KENEX · PDF": "KENEX · PDF",
  "Hier finden Sie unsere Produktkataloge und Farbkarten sowie die technischen Datenblätter zu unseren Produkten der Medizinischen Einrichtung. Der COINFYCARE-Katalog deckt die Bereiche 01–03 ab, der TECH-MED-Katalog samt Farbkarten die Bereiche 04–09 einschließlich Schienensysteme. Neue Dokumente ergänzen wir laufend.": "Aici găsiți cataloagele noastre de produse și cartelele de culori, precum și fișele tehnice ale produselor noastre de mobilier medical. Catalogul COINFYCARE acoperă secțiunile 01–03, iar catalogul TECH-MED împreună cu cartelele de culori acoperă secțiunile 04–09, inclusiv sistemele de șine. Adăugăm continuu documente noi.",
  "Produktkatalog": "Catalog de produse",
  "Produktkataloge & Farbkarten": "Cataloage de produse și cartele de culori",
  "Produktkatalog · Bereiche 01–03": "Catalog de produse · Secțiunile 01–03",
  "Produktkatalog · Bereiche 04–09": "Catalog de produse · Secțiunile 04–09",
  "Farbkarten · Bereiche 04–09": "Cartele de culori · Secțiunile 04–09",
  "COINFYCARE · PDF": "COINFYCARE · PDF",
  "TECH-MED · PDF": "TECH-MED · PDF",
  "Die Unterlagen zu unseren Produkten des Strahlenschutzes senden wir Ihnen gerne auf Anfrage zu.": "Vă trimitem cu plăcere, la cerere, documentele pentru produsele noastre de protecție radiologică.",
  "Die Unterlagen zu unseren Produkten der Medizinischen Einrichtung senden wir Ihnen gerne auf Anfrage zu.": "Vă trimitem cu plăcere, la cerere, documentele pentru produsele noastre de mobilier medical.",
  "Die Unterlagen zu unseren Heilbehelfen und Hilfsmitteln senden wir Ihnen gerne auf Anfrage zu.": "Vă trimitem cu plăcere, la cerere, documentele pentru mijloacele noastre ajutătoare și dispozitivele de asistență.",
  "Personalisierung": "Personalizare",
  "Optionale Extras": "Extraopțiuni",
  "Stickerei": "Broderie",
  "Individuelle Textstickerei direkt auf der Schürze – z. B. Name, Abteilung oder Einsatzbereich.": "Broderie text individuală direct pe șorț – de ex. nume, secție sau domeniu de utilizare.",
  "Aufgesetzte Tasche": "Buzunar aplicat",
  "Praktische Außentasche für Dosimeter, Stift oder Kleinteile.": "Buzunar exterior practic pentru dozimetru, pix sau obiecte mici.",
  "Taschen-Stickerei": "Broderie pe buzunar",
  "Bestickung direkt auf der Tasche – etwa mit Abteilungs- oder Klinikname.": "Broderie direct pe buzunar – de ex. cu numele secției sau al clinicii.",
  "Austauschbares Namensschild": "Ecuson interschimbabil",
  "Per Klett wechselbares Namensschild – jederzeit flexibel anpassbar.": "Ecuson schimbabil cu scai – adaptabil flexibil în orice moment.",
  "Transparente Ausweistasche": "Buzunar transparent pentru legitimație",
  "Klarsichttasche für Dienstausweis oder Dosimeter-Karte.": "Buzunar transparent pentru legitimația de serviciu sau cardul de dozimetru.",
  "Innentasche": "Buzunar interior",
  "Verdeckte Innentasche für persönliche Kleinteile.": "Buzunar interior ascuns pentru obiecte personale mici.",
  "Outlast®-Klimatechnologie": "Tehnologie climatică Outlast®",
  "Temperaturregulierendes Innenfutter für spürbar angenehmeres Tragen.": "Căptușeală care reglează temperatura pentru o purtare vizibil mai confortabilă.",
  "Rock-Tasche": "Buzunar la fustă",
  "Zusätzliche Tasche am Rockteil des Zweiteilers.": "Buzunar suplimentar la partea de fustă a setului din două piese.",
  "Innengurt": "Centură interioară",
  "Integrierter Stützgurt entlastet den Rücken und verbessert den Sitz.": "Centura de susținere integrată descarcă spatele și îmbunătățește potrivirea.",
  "Unifarben": "Culori uni",
  "Muster": "Modele",
  "Einfassung": "Bordură",
  "Royalblau": "Albastru regal", "Marineblau": "Bleumarin", "Orange": "Portocaliu", "Rosé": "Roz pal",
  "Bordeaux": "Bordo", "Beere": "Fruct de pădure", "Rot": "Roșu", "Violett": "Violet", "Grau": "Gri",
  "Hellgrün": "Verde deschis", "Waldgrün": "Verde pădure", "Khaki": "Kaki", "Schwarz": "Negru", "Gelb": "Galben",
  "Zebra": "Zebră", "Karo": "Carouri", "Sterne": "Stele", "Safari": "Safari", "Wirbel": "Spirale",
  "Blüten Pink": "Flori roz", "Blüten Violett": "Flori violet", "Feuerwerk": "Artificii",
  "Flammen": "Flăcări", "Kindermotiv": "Motiv pentru copii", "Farbkleckse": "Pete de vopsea",
  "Camouflage Pink": "Camuflaj roz", "Camouflage Grau": "Camuflaj gri", "Camouflage Blau": "Camuflaj albastru",
  "Blau": "Albastru", "Grün": "Verde", "Dunkelpink": "Roz închis", "Neonpink": "Roz neon", "Petrol": "Petrol",
 },
}

# Statische Chrome-Strings (Voll-String-Ersetzung auf der Seite; längste zuerst)
_PROD_CHROME = [
  "Wir vermitteln und liefern zertifizierte Medizinprodukte in mehreren Kategorien: Strahlenschutz, Medizinische Einrichtung und Heilbehelfe &amp; Hilfsmittel. Darüber hinaus beschaffen wir herstellerunabhängig nahezu jedes Produkt und statten ganze Bereiche projektbasiert aus. Klicken Sie eine Kategorie an, um die einzelnen Bereiche zu entdecken.",
  "Persönliche Strahlenschutz-Bekleidung „Made in UK\" vom Hersteller ROTHBAND – ergänzt um passende Aufbewahrung sowie mobile, deckenmontierte und tischmontierte Röntgenschutzsysteme von KENEX. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.",
  "Strahlenschutzbekleidung für den direkten Personenschutz – Schürzen, Zweiteiler, Schilddrüsenschutz und ergänzendes Zubehör. Fokus auf Ergonomie, Gewichtsverteilung, Schutzleistung und Tragekomfort.",
  "Röntgenschutzbrillen für den Schutz der Augen bei Durchleuchtung, interventioneller Bildgebung und Radiologie – in zahlreichen Rahmenformen, mit seitlichem Schutz und wahlweise mit Sehstärke. Bleigläser 0,75 mm Pb, Seitenschutz 0,50 mm Pb.",
  "Jede Schürze lässt sich individuell anpassen – für eine bessere Zuordnung, mehr Tragekomfort und praktische Details im Klinikalltag. Alle Optionen sind mit den Modellen aus „Persönlicher Strahlenschutz\" kombinierbar.",
  "Alle Schürzen und Zubehörteile sind in zahlreichen Farben, Mustern und Einfassungen erhältlich – für ein individuelles, gut erkennbares Erscheinungsbild. Das Stoffsortiment wird von ROTHBAND laufend erweitert.",
  "Ständer, Schwenkarme und Bügel zur sicheren, platzsparenden Aufbewahrung von Strahlenschutzschürzen.",
  "Fahrbare, frei positionierbare Röntgenschutzsysteme für flexible Einsätze im OP und in der interventionellen Radiologie – vom Hersteller KENEX.",
  "Aufgehängte Überkopf-Schutzschilde und komplette Aufhängungssysteme (Deckenschienen, Säulen, Arme, Monitor-Aufhängung) – zur deutlichen Reduktion der Streustrahlung im Arbeitsbereich. Vom Hersteller KENEX.",
  "Am Untersuchungstisch montierte Schutzschilde für die interventionelle Radiologie – Unterkörper-, Kopfende- und Aufsatz-Schilde sowie passende Aufbewahrung. Vom Hersteller KENEX.",
  "Ausstattung und Einrichtung für klinische Bereiche – vom Untersuchungsplatz bis zur Sterilgutlogistik. Geliefert von COINFYCARE (Liegen, Stühle, Sichtschutz) und TECHMED (Wagen und Tische, Transport und Entsorgung, Stations- und Ambulanzausstattung, MRT-Ausstattung). Klicken Sie einen Bereich an, um die Modelle aufzuklappen.",
  "Untersuchungs- und Behandlungsliegen für Praxis und Klinik – nach Bauart gegliedert.",
  "Behandlungs-, Blutabnahme- und Arbeitsstühle sowie Hocker für den medizinischen Einsatz.",
  "Sicht- und Trennwandsysteme für diskrete, flexibel teilbare Raumbereiche.",
  "Mobilität, Pflege und Alltagshilfen – von Rollstühlen und Elektromobilen über Gehhilfen bis zu Anti-Dekubitus-Systemen und Sauerstoffversorgung. Geliefert vom Hersteller MOBIAK. Klicken Sie einen Bereich an, um die Modelle aufzuklappen.",
  "Sie suchen ein Produkt, das nicht in unserem Katalog enthalten ist? Dank unserer Herstellerunabhängigkeit sind wir nicht an bestimmte Marken gebunden und können Produkte verschiedenster Hersteller für Sie beschaffen.",
  "Ob Standardartikel, Spezialgerät oder schwer erhältliches Ersatzteil – wir identifizieren die passende Bezugsquelle und liefern zuverlässig. Kein Sortiment setzt uns Grenzen: Sie nennen den Bedarf, wir finden die Lösung.",
  "Von der Praxis bis zur Klinikabteilung statten wir ganze Bereiche aus – abgestimmt auf Arbeitsabläufe, Hygieneanforderungen und Budget. Grundausstattung, Mobiliar und High-End-Technik aus einer Hand.",
  "Wir sind an keine Marke gebunden. So wählen wir stets das Produkt, das technisch, wirtschaftlich und qualitativ am besten zu Ihrer Anforderung passt – objektiv und in Ihrem Interesse.",
  "Ein Ansprechpartner für den gesamten Beschaffungsprozess: Bedarfsanalyse, Angebot, Einkauf, Logistik und Lieferung – auf Wunsch inklusive Installation und Einschulung. Termintreu, transparent und aus einer Hand.",
  "Sie haben einen konkreten Bedarf oder planen ein Projekt? Beschreiben Sie uns Ihr Vorhaben – wir erstellen Ihnen ein individuelles, unverbindliches Angebot.",
  "Hersteller ROTHBAND – Website in neuem Tab öffnen",
  "Hersteller KENEX – Website in neuem Tab öffnen",
  "Hersteller COINFYCARE – Website in neuem Tab öffnen",
  "Hersteller TECHMED – Website in neuem Tab öffnen",
  "Medizinische Wagen",
  "Geräte- &amp; Versorgungswagen",
  "Behandlungs-, Instrumenten- &amp; Stationstische",
  "Transport, Entsorgung &amp; Sterilgutlogistik",
  "Stations- und Ambulanzausstattung",
  "MRT-Ausstattung (nicht-magnetisch)",
  "Die Modelle zu diesem Bereich werden derzeit aufbereitet und in Kürze ergänzt.",
  "Hersteller MOBIAK – Website in neuem Tab öffnen",
  "Herstellerunabhängige Produktbeschaffung",
  "Tischmontierter Strahlenschutz",
  "Deckenmontierter Strahlenschutz",
  "Persönlicher Strahlenschutz",
  "Mobiler Strahlenschutz",
  "Aufsatz- &amp; Fußende-Schilde",
  "Unterkörper-Tischschilde",
  "Kopfende-Tischschilde",
  "Aufbewahrung &amp; Zubehör",
  "Personalisierung &amp; Optionen",
  "Elektrische Rollstühle &amp; Scooter",
  "Anti-Dekubitus-Produkte",
  "Sauerstoffkonzentratoren",
  "Herstellerunabhängig",
  "Komplette Bereichsausstattung",
  "Projekt- &amp; Komplettservice",
  "Umhang-/Tabard-Schürzen",
  "Mantel-/Wickelschürzen",
  "Zweiteiler – Oberteil &amp; Rock",
  "Chiropraktische Liegen",
  "Überkopf-Schutzschilde",
  "Strahlenschutzbrillen",
  "Aufhängungssysteme",
  "Medizinische Einrichtung",
  "Medizinische Stühle",
  "Heilbehelfe &amp; Hilfsmittel",
  "Untersuchungsliegen",
  "Schilddrüsenschutz",
  "Alles beschaffbar",
  "Gehböcke / Walker",
  "Front-Schürzen",
  "Unsere Produkte",
  "Modelle verfügbar",
  "Fahrbare Wagen für Anästhesie, Notfall, Station und Behandlung – wahlweise mit geschlossenem Stahlkorpus oder als modulare Aluminium-Plattform, die Sie Schublade für Schublade auf Ihren Ablauf zuschneiden.",
  "Einheitlich aufgebaut: 500 mm Korpustiefe, 1000 mm Arbeitshöhe, vertiefte Arbeitsplatte mit drei Aufkantungen und Ø 125 mm Rollen mit zwei Feststellern. Fronten und Griffe sind farbig nach TECH-MED-Farbkarte erhältlich – so lassen sich Stationen auf einen Blick unterscheiden. Das Zubehörprogramm ist über alle Baureihen hinweg identisch und frei kombinierbar.",
  "Materialausführungen: ABS = Stahlkorpus mit Arbeitsplatte aus ABS-Kunststoff · ST = Korpus und Arbeitsplatte aus pulverbeschichtetem Stahl · KO = Korpus und Arbeitsplatte aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe.",
  "Ausstattung für Bettenstation und Ambulanz: Nachtkästchen, Bettbeistelltische, Infusionsständer, Auftritte und Injektionsstühle sowie teleskopierbare Wandarme für Infusionen und Sichtschutz – überwiegend aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) oder pulverbeschichtetem Stahl und auf tägliche Wischdesinfektion ausgelegt.",
  "Farbgebung nach TECH-MED-Farbkarte: Fronten, Türen und Polster sind in mehreren RAL- und Bezugsfarben erhältlich – so lassen sich Stationen und Bereiche auf einen Blick unterscheiden. Materialkürzel: ST = pulverbeschichteter Stahl · KO = Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) · ABS = ABS-Kunststoff · HPL = wasserfeste Schichtstoffplatte.",
  "Fahrbare Geräteträger und Versorgungswagen für Diagnostik, Behandlung und Stationsalltag: schlanke Aluminium-Säulenwagen, die Sie Ebene für Ebene bestücken, und Behandlungswagen mit Edelstahlplatte für Verbandwechsel, Blutabnahme und Medikamentenverteilung.",
  "Zwei Bausysteme, ein Zubehörprogramm: Bei den Säulenwagen (ECO, TOP, MOD, K-1, K-1 LUX, APAR) sitzen alle Ebenen auf gemeinsamen Aluminiumsäulen und lassen sich in der Höhe frei versetzen – Steckdosenleiste, Normschiene, Zubehörkorb, Monitorhalter und Infusionsständer sind über alle Baureihen hinweg identisch und frei kombinierbar. Die Stationswagen K-3, MB-3 und WL sind auf tägliche Wischdesinfektion ausgelegt; Fronten und Säulenblenden gibt es farbig nach TECH-MED-Farbkarte.",
  "Behandlungstische und Instrumententische für Eingriffsraum, Ambulanz und OP: fahrbare Behandlungstische mit vertiefter Arbeitsplatte und Anbauzubehör sowie höhenverstellbare Instrumententische aus Edelstahl – manuell, hydraulisch oder elektrisch.",
  "Materialausführungen: KO = komplett aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe · ST = komplett aus pulverbeschichtetem Stahl, farbig nach TECH-MED-Farbkarte. Bei den Behandlungstischen STKO bestimmt die gewählte Plattenlänge die Gesamtlänge des Tisches; bei den Instrumententischen verändert die Rollenausführung die Bauhöhe.",
  "Transport, Entsorgung und Sterilgutlogistik in einem Bereich: Transport- und Speisenwagen, Korbwagen für den innerbetrieblichen Materialfluss, Wäsche- und Abfallwagen für die Entsorgung sowie Packtische und Regalsysteme für die Sterilgutaufbereitung und das Lager.",
  "Ein Baukasten für alle Regalsysteme: Körbe, Ablagen, Abwurfbeutelhalter und Trockner werden in dieselben Schienen und Gestelle eingehängt – ob als Wandschiene, Standregal oder fahrbarer Wagen. Die Entsorgungswagen gibt es in zwei Bauweisen: komplett aus Edelstahl 0H18N9 (austenitischer Edelstahl 1.4301) für die höchste Hygienestufe (WZ, WZB, MB) oder in Möbelbauweise mit Aluminium-Profilrahmen und farbigen Füllungen nach RAL (WMW, WCB).",
  "Ausstattung, die im MRT-Raum verbleiben kann: Liege, Tritte, Infusionsständer, Wagen und Sichtschutz – komplett aus nicht-magnetischen Werkstoffen, damit Arbeitsabläufe nicht am Zonenübergang enden.",
  "Wichtiger Hinweis: Alle Produkte dieses Bereichs sind für Magnetfeldstärken bis 3 Tesla zugelassen. Für Systeme mit höherer Feldstärke sprechen Sie uns bitte an.",
  "Modell verfügbar",
  "Produkte verfügbar",
  "Strahlenschutz",
  "Aufbewahrung",
  "Rollstühle",
  "Rollatoren",
  "Gehhilfen",
  "Sichtschutz",
  "Hydraulisch",
  "Elektrisch",
  "Hersteller",
  "Produkte",
  "Zubehör",
]

def _body_produkte(lang):
    if lang == "de":
        return _inject_flyer(BODY_PRODUKTE, "de")
    body = BODY_PRODUKTE
    # 1) Produktkarten- und Bausteine je Sprache neu erzeugen und tauschen
    swaps = []
    for sub in ("front", "tabard", "wrap", "zweiteiler", "schild", "zubehoer", "brillen", "aufbewahrung"):
        swaps.append((_ss_cards(sub), _ss_cards(sub, lang)))
    swaps.append((_kenex_cards("mobil"), _kenex_cards("mobil", lang=lang)))
    for s in ("ueberkopf", "aufhaengung"):
        swaps.append((_kenex_cards("decken", s), _kenex_cards("decken", s, lang)))
    for s in ("unterkoerper", "kopfende", "top", "aufbewahrung"):
        swaps.append((_kenex_cards("tisch", s), _kenex_cards("tisch", s, lang)))
    for c in ("fix", "hydraulisch", "elektrisch", "chiro", "stuehle", "sichtschutz", "mrt", "wagen", "station", "gvw", "btisch", "trans"):
        swaps.append((_cards(c), _cards(c, lang)))
    swaps.append((_hb_cards("rollstuehle"), _hb_cards("rollstuehle", lang=lang)))
    swaps.append((_hb_cards("erollstuehle"), _hb_cards("erollstuehle", lang=lang)))
    swaps.append((_hb_cards("gehhilfen", "rollatoren"), _hb_cards("gehhilfen", "rollatoren", lang)))
    swaps.append((_hb_cards("gehhilfen", "walker"), _hb_cards("gehhilfen", "walker", lang)))
    swaps.append((_hb_cards("antidekubitus"), _hb_cards("antidekubitus", lang=lang)))
    swaps.append((_hb_cards("oxygen"), _hb_cards("oxygen", lang=lang)))
    swaps.append((_optionen_html(), _optionen_html(lang)))
    swaps.append((_farben_html(), _farben_html(lang)))
    swaps.append((_downloads_cat_cards("06", "downloads-strahlenschutz", _DL_LEAD_SS, DL_SS),
                  _downloads_cat_cards("06", "downloads-strahlenschutz", _DL_LEAD_SS, DL_SS, lang=lang)))
    swaps.append((_downloads_datasheets("10", "downloads-medizinische-einrichtung", _DL_LEAD_MED, DL_MED_CATS, catalog=DL_MED_CATALOG),
                  _downloads_datasheets("10", "downloads-medizinische-einrichtung", _DL_LEAD_MED, DL_MED_CATS, catalog=DL_MED_CATALOG, lang=lang)))
    swaps.append((_downloads_category("06", "downloads-heilbehelfe", "", [], note=_DL_NOTE_ANFRAGE_HB),
                  _downloads_category("06", "downloads-heilbehelfe", "", [], note=_DL_NOTE_ANFRAGE_HB, lang=lang)))
    for de_block, tr_block in swaps:
        if de_block and de_block in body:
            body = body.replace(de_block, tr_block)
        elif de_block:
            print(f"  WARN [PROD {lang}] Kartenblock nicht gefunden (len={len(de_block)})")
    # 2) statische Chrome-Texte übersetzen (längste zuerst)
    for de_s in sorted(_PROD_CHROME, key=len, reverse=True):
        body = body.replace(de_s, _puit(lang, de_s))
    # "Fix" nur im Akkordeon-Titel ersetzen (sonst würde es "Fixed" im Download-Block treffen)
    body = body.replace('<span class="m-ac-title">Fix</span>',
                        f'<span class="m-ac-title">{_puit(lang, "Fix")}</span>')
    # 3) Asset-Pfade root-absolut, Kontakt-Link sprachspezifisch
    body = body.replace("assets/", "/assets/")
    body = body.replace('href="kontakt.html"', f'href="/{lang}/kontakt.html"')
    return _inject_flyer(body, lang)

BODY_PRODUKTE_EN = _body_produkte("en")
BODY_PRODUKTE_PL = _body_produkte("pl")
BODY_PRODUKTE_RO = _body_produkte("ro")
# DE-Seite nutzt BODY_PRODUKTE direkt – Flyer-Reihe erst jetzt einsetzen,
# damit EN/PL/RO oben noch vom Marker ausgehen konnten.
BODY_PRODUKTE = _inject_flyer(BODY_PRODUKTE, "de")

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
          <input type="text" name="_honey" class="m-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <input type="hidden" name="_subject" value="Neue Anfrage über medeqon.com">
          <input type="hidden" name="_template" value="table">
          <div class="m-turnstile"><div class="cf-turnstile" data-sitekey="__TURNSTILE_SITEKEY__" data-theme="light" data-language="auto"></div></div>
          <button class="m-btn" type="submit" id="k-submit">Anfrage senden</button>
          <div class="m-form-status" id="formStatus" role="status" aria-live="polite"></div>
          <noscript><p class="sub">Bitte aktivieren Sie JavaScript oder schreiben Sie uns direkt an office@medeqon.com.</p></noscript>
        </form>
        <p class="m-form-note">Mit dem Absenden dieses Kontaktformulars verarbeiten wir Ihre personenbezogenen Daten (Name, E-Mail, Telefonnummer und Nachricht), um Ihre Anfrage zu beantworten. Rechtsgrundlage ist die (vor-)vertragliche Kommunikation gemäß Art. 6 Abs. 1 lit. b DSGVO. Weitere Informationen finden Sie in unserer <a href="datenschutz.html">Datenschutzerklärung</a>.</p>
      </div>

      <aside class="m-caside">
        <div>
          <span class="k">Direkt</span>
          <a href="mailto:office@medeqon.com">office@medeqon.com</a>
          <a href="tel:+4313580045">+43 1 3580045</a>
        </div>
        <div>
          <span class="k">Büro</span>
          <p>Bergstraße 42/5/3<br>2102 Hagenbrunn · Österreich<br>Mo – Fr · und nach Vereinbarung</p>
        </div>
      </aside>
    </div>
  </div>
</section>

<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<script>
(function(){
  var f=document.getElementById("kontaktForm");
  if(!f) return;
  var s=document.getElementById("formStatus");
  var btn=document.getElementById("k-submit");
  var ENDPOINT="https://formsubmit.co/ajax/office@medeqon.com";
  var t0=Date.now();
  f.addEventListener("submit", function(e){
    e.preventDefault();
    if(f._honey.value){ return; }
    if(Date.now()-t0 < 1500){ return; }
    if(!f.checkValidity()){ f.reportValidity(); return; }
    var tk=f.querySelector('[name="cf-turnstile-response"]');
    if(!tk || !tk.value){
      s.className="m-form-status is-err";
      s.textContent="Bitte bestätigen Sie im Sicherheits-Check, dass Sie kein Roboter sind.";
      return;
    }
    btn.disabled=true;
    s.className="m-form-status is-sending"; s.textContent="Anfrage wird gesendet …";
    var fd=new FormData(f); fd.delete("cf-turnstile-response");
    fetch(ENDPOINT,{method:"POST",headers:{"Accept":"application/json"},body:fd})
      .then(function(r){ return r.json().catch(function(){return {};}); })
      .then(function(){
        s.className="m-form-status is-ok";
        s.textContent="Vielen Dank! Ihre Anfrage wurde gesendet – wir melden uns zeitnah bei Ihnen.";
        f.reset();
        if(window.turnstile){ turnstile.reset(); }
      })
      .catch(function(){
        s.className="m-form-status is-err";
        s.innerHTML='Beim Senden ist ein Fehler aufgetreten. Bitte schreiben Sie uns direkt an <a href="mailto:office@medeqon.com">office@medeqon.com</a>.';
      })
      .then(function(){ btn.disabled=false; });
  });
})();
</script>'''

# ================= Referenzen (persönliche Referenzen G. Scherzer) =================
import re as _re

# ---- i18n-Datendicts (Projektnamen/-umfang) + statische UI-Übersetzungen ----
_REF_TR = {}
for _L in ("en", "pl", "ro"):
    _dj = json.loads((ROOT / "i18n" / f"ref_{_L}.json").read_text(encoding="utf-8"))
    _m = {}
    _m.update(_dj.get("project_names", {}))
    _m.update(_dj.get("project_scope", {}))
    _REF_TR[_L] = _m

_UIT_MISS = set()

def _reft(lang, s):
    """Daten-Übersetzung (Projektnamen/-umfang). Warnt bei fehlender Übersetzung."""
    if lang == "de" or not s:
        return s
    v = _REF_TR.get(lang, {}).get(s)
    if v is None:
        print(f"  WARN [REF {lang}] Projektdaten nicht übersetzt: {s[:60]!r}")
        return s
    return v

def _uit(lang, s):
    """UI-Übersetzung (Labels/Überschriften/Beschreibungen). Fallback = Original."""
    if lang == "de" or not s:
        return s
    m = _REFUI.get(lang, {})
    if s in m:
        return m[s]
    _UIT_MISS.add((lang, s))
    return s

def _ap(lang, path):
    """Asset-Pfad root-absolut für übersetzte Seiten."""
    if lang == "de" or not path:
        return path
    return path if path.startswith("/") else "/" + path

_REFUI = {
 "en": {
  "Referenzen": "References",
  "Ausgewählte Projekte aus der langjährigen Erfahrung unseres Teams.": "Selected projects drawn from our team's many years of experience.",
  "Kompetenz aus Projekten": "Expertise from projects",
  "Wissen aus Forschung": "Knowledge from research",
  "Vertrauen durch Erfahrung": "Trust through experience",
  "Projektreferenzen": "Project references",
  "Realisierte Projekte": "Completed projects",
  "Unsere Referenzen spiegeln langjährige Erfahrung, technisches Know-how und individuelle Lösungen wider. Gemeinsam mit unseren Kunden realisieren wir Projekte, die höchsten fachlichen und qualitativen Ansprüchen gerecht werden.": "Our references reflect many years of experience, technical know-how and individual solutions. Together with our clients we deliver projects that meet the highest professional and quality standards.",
  "Wählen Sie oben eine Kategorie, um die zugehörigen Projekte anzuzeigen.": "Select a category above to display the associated projects.",
  "Wählen Sie oben eine Kategorie, um die Beiträge anzuzeigen.": "Select a category above to display the entries.",
  "Akademisches und Wissenschaft": "Academic & science",
  "Wissenschaft &amp; Forschung": "Science &amp; research",
  "Wissenschaft und Forschung sind fester Bestandteil unseres Selbstverständnisses. Durch die Mitwirkung an Forschungsprojekten, wissenschaftlichen Beiträgen und dem fachlichen Austausch leisten wir einen aktiven Beitrag zur Weiterentwicklung moderner Medizintechnik und evidenzbasierter Lösungen.": "Science and research are an integral part of who we are. Through our involvement in research projects, scientific contributions and professional exchange, we actively contribute to the advancement of modern medical technology and evidence-based solutions.",
  "Consulting und Lehre": "Consulting &amp; teaching",
  "Consulting &amp; Lehre": "Consulting &amp; teaching",
  "Herstellerunabhängige Beratung mit technischem Know-how – individuell, praxisnah und lösungsorientiert – sowie akademische Lehr- und Betreuungstätigkeit.": "Manufacturer-independent consulting with technical know-how – individual, practical and solution-oriented – as well as academic teaching and supervision.",
  "Ihr Projekt in erfahrenen Händen": "Your project in experienced hands",
  "Projekt besprechen": "Discuss your project",
  "Schließen": "Close",
  "Vorheriges Bild": "Previous image",
  "Nächstes Bild": "Next image",
  "Alle": "All",
  "Bilder": "images",
  "Details ansehen": "View details",
  "AKH Wien · Persönlich": "AKH Vienna · Personal",
  "AKH Wien · Leitung": "AKH Vienna · Management",
  "Österreich": "Austria",
  "Schweiz": "Switzerland",
  "Internationale Projekte": "International projects",
  "Konferenzen": "Conferences",
  "Publikationen": "Publications",
  "Wissenschaftliche Beiträge": "Scientific contributions",
  "Consulting": "Consulting",
  "Lehre": "Teaching",
  "Vortrag": "Talk",
  "Plenarbeitrag": "Plenary contribution",
  "Promotion": "Doctorate",
  "Internationale Beratung": "International consulting",
  "Lehrvortrag": "Lecture",
  "Fachvorträge": "Expert talks",
  "Akademischer Berater": "Academic advisor",
  "1 Jahr": "1 year", "2 Jahre": "2 years", "2,5 Jahre": "2.5 years",
  "3 Jahre": "3 years", "4 Jahr": "4 years", "4 Jahre": "4 years", "5 Jahre": "5 years",
  "Oral Presentation &middot; The European Health Economics Association (EuHEA), 14.–16. Juli 2016.": "Oral Presentation &middot; The European Health Economics Association (EuHEA), 14–16 July 2016.",
  "Poster Presentation &middot; 9th European Public Health Conference „Health for All – All for Health“, 9.–12. November 2016, ACV, Wien.": "Poster Presentation &middot; 9th European Public Health Conference „Health for All – All for Health“, 9–12 November 2016, ACV, Vienna.",
  "Plenary Contribution &middot; 3rd WHO Global Forum on Medical Devices, 12.05.2017.": "Plenary Contribution &middot; 3rd WHO Global Forum on Medical Devices, 12 May 2017.",
  "Doktorarbeit (PhD)": "Doctoral thesis (PhD)",
  "„Leading health care facilities in times of armed conflict: what are the constraints for medical equipment management?“ – Dissertation zur Medizintechnik-Beschaffung unter Extrembedingungen.": "„Leading health care facilities in times of armed conflict: what are the constraints for medical equipment management?“ – Doctoral dissertation on medical technology procurement under extreme conditions.",
  "Qualitätssicherung in der Planung": "Quality assurance in design",
  "Zur VKMB": "To VKMB",
  "Im Auftrag der VKMB begleiten wir die Medizintechnik-Planung beratend und sichern gemeinsam mit dem Team des Kunden die Qualität der erstellten Planungsunterlagen. Ein unabhängiger zweiter Blick auf Vollständigkeit, technische Plausibilität und Betriebstauglichkeit – damit Entscheidungen auf belastbaren Grundlagen fallen und Korrekturen dort erfolgen, wo sie noch nichts kosten: in der Planung.": "On behalf of VKMB we provide consulting support for Medical Technology Design and, together with the client's team, ensure the quality of the planning documents produced. An independent second opinion on completeness, technical plausibility and suitability for daily operation – so that decisions rest on solid ground and corrections are made where they still cost nothing: during design.",
  "Beratung zum „Compendium on innovative medical technologies“ sowie Plenarbeitrag beim 3rd WHO Global Forum on Medical Devices zu Medizintechnik in Konfliktsituationen.": "Consulting on the „Compendium on innovative medical technologies“ as well as a plenary contribution at the 3rd WHO Global Forum on Medical Devices on medical technology in conflict situations.",
  "Zur WHO-Publikation": "To the WHO publication",
  "Lehrvortrag zu den europäischen und rechtlichen Grundlagen der Medizintechnik.": "Lecture on the European and legal foundations of medical technology.",
  "Aktive Mitarbeit und Fachvorträge für den Österreichischen Verband der Krankenhaustechniker:innen.": "Active involvement and expert talks for the Austrian Association of Hospital Technicians.",
  "Zum ÖVKT": "To ÖVKT",
  "Zum Medizintechnik-Cluster": "To the Medical Technology Cluster",
  "Betreuung einer Masterarbeit": "Supervision of a master's thesis",
  "Academic Advisor für die Masterarbeit „Enablers and barriers in medical device export to Syria“ (qualitative Studie) an der University of Copenhagen, November 2016 – Dezember 2017.": "Academic advisor for the master's thesis „Enablers and barriers in medical device export to Syria“ (qualitative study) at the University of Copenhagen, November 2016 – December 2017.",
 },
 "pl": {
  "Referenzen": "Referencje",
  "Ausgewählte Projekte aus der langjährigen Erfahrung unseres Teams.": "Wybrane projekty z wieloletniego doświadczenia naszego zespołu.",
  "Kompetenz aus Projekten": "Kompetencje z projektów",
  "Wissen aus Forschung": "Wiedza z badań",
  "Vertrauen durch Erfahrung": "Zaufanie dzięki doświadczeniu",
  "Projektreferenzen": "Referencje projektowe",
  "Realisierte Projekte": "Zrealizowane projekty",
  "Unsere Referenzen spiegeln langjährige Erfahrung, technisches Know-how und individuelle Lösungen wider. Gemeinsam mit unseren Kunden realisieren wir Projekte, die höchsten fachlichen und qualitativen Ansprüchen gerecht werden.": "Nasze referencje odzwierciedlają wieloletnie doświadczenie, wiedzę techniczną i indywidualne rozwiązania. Wspólnie z naszymi klientami realizujemy projekty spełniające najwyższe wymagania merytoryczne i jakościowe.",
  "Wählen Sie oben eine Kategorie, um die zugehörigen Projekte anzuzeigen.": "Wybierz kategorię powyżej, aby wyświetlić powiązane projekty.",
  "Wählen Sie oben eine Kategorie, um die Beiträge anzuzeigen.": "Wybierz kategorię powyżej, aby wyświetlić wpisy.",
  "Akademisches und Wissenschaft": "Środowisko akademickie i nauka",
  "Wissenschaft &amp; Forschung": "Nauka i badania",
  "Wissenschaft und Forschung sind fester Bestandteil unseres Selbstverständnisses. Durch die Mitwirkung an Forschungsprojekten, wissenschaftlichen Beiträgen und dem fachlichen Austausch leisten wir einen aktiven Beitrag zur Weiterentwicklung moderner Medizintechnik und evidenzbasierter Lösungen.": "Nauka i badania są nieodłączną częścią naszej tożsamości. Poprzez udział w projektach badawczych, publikacjach naukowych i wymianie fachowej aktywnie przyczyniamy się do rozwoju nowoczesnej techniki medycznej i rozwiązań opartych na dowodach.",
  "Consulting und Lehre": "Doradztwo i dydaktyka",
  "Consulting &amp; Lehre": "Doradztwo i dydaktyka",
  "Herstellerunabhängige Beratung mit technischem Know-how – individuell, praxisnah und lösungsorientiert – sowie akademische Lehr- und Betreuungstätigkeit.": "Niezależne od producentów doradztwo z wiedzą techniczną – indywidualne, praktyczne i zorientowane na rozwiązania – oraz akademicka działalność dydaktyczna i opiekuńcza.",
  "Ihr Projekt in erfahrenen Händen": "Twój projekt w doświadczonych rękach",
  "Projekt besprechen": "Omów projekt",
  "Schließen": "Zamknij",
  "Vorheriges Bild": "Poprzedni obraz",
  "Nächstes Bild": "Następny obraz",
  "Alle": "Wszystkie",
  "Bilder": "zdjęcia",
  "Details ansehen": "Zobacz szczegóły",
  "AKH Wien · Persönlich": "AKH Wiedeń · Osobiste",
  "AKH Wien · Leitung": "AKH Wiedeń · Kierownictwo",
  "Österreich": "Austria",
  "Schweiz": "Szwajcaria",
  "Internationale Projekte": "Projekty międzynarodowe",
  "Konferenzen": "Konferencje",
  "Publikationen": "Publikacje",
  "Wissenschaftliche Beiträge": "Wkład naukowy",
  "Consulting": "Doradztwo",
  "Lehre": "Dydaktyka",
  "Vortrag": "Wykład",
  "Plenarbeitrag": "Wystąpienie plenarne",
  "Promotion": "Doktorat",
  "Internationale Beratung": "Doradztwo międzynarodowe",
  "Lehrvortrag": "Wykład",
  "Fachvorträge": "Wykłady specjalistyczne",
  "Akademischer Berater": "Doradca akademicki",
  "1 Jahr": "1 rok", "2 Jahre": "2 lata", "2,5 Jahre": "2,5 roku",
  "3 Jahre": "3 lata", "4 Jahr": "4 lata", "4 Jahre": "4 lata", "5 Jahre": "5 lat",
  "Oral Presentation &middot; The European Health Economics Association (EuHEA), 14.–16. Juli 2016.": "Prezentacja ustna &middot; The European Health Economics Association (EuHEA), 14–16 lipca 2016.",
  "Poster Presentation &middot; 9th European Public Health Conference „Health for All – All for Health“, 9.–12. November 2016, ACV, Wien.": "Prezentacja posteru &middot; 9th European Public Health Conference „Health for All – All for Health“, 9–12 listopada 2016, ACV, Wiedeń.",
  "Plenary Contribution &middot; 3rd WHO Global Forum on Medical Devices, 12.05.2017.": "Wystąpienie plenarne &middot; 3rd WHO Global Forum on Medical Devices, 12 maja 2017.",
  "Doktorarbeit (PhD)": "Praca doktorska (PhD)",
  "„Leading health care facilities in times of armed conflict: what are the constraints for medical equipment management?“ – Dissertation zur Medizintechnik-Beschaffung unter Extrembedingungen.": "„Leading health care facilities in times of armed conflict: what are the constraints for medical equipment management?“ – Rozprawa doktorska na temat zaopatrzenia w technikę medyczną w warunkach ekstremalnych.",
  "Qualitätssicherung in der Planung": "Zapewnienie jakości w projektowaniu",
  "Zur VKMB": "Do VKMB",
  "Im Auftrag der VKMB begleiten wir die Medizintechnik-Planung beratend und sichern gemeinsam mit dem Team des Kunden die Qualität der erstellten Planungsunterlagen. Ein unabhängiger zweiter Blick auf Vollständigkeit, technische Plausibilität und Betriebstauglichkeit – damit Entscheidungen auf belastbaren Grundlagen fallen und Korrekturen dort erfolgen, wo sie noch nichts kosten: in der Planung.": "Na zlecenie VKMB wspieramy doradczo projektowanie techniki medycznej i wspólnie z zespołem klienta zapewniamy jakość opracowanych dokumentów projektowych. Niezależne, drugie spojrzenie na kompletność, wiarygodność techniczną i przydatność eksploatacyjną – aby decyzje opierały się na solidnych podstawach, a korekty następowały tam, gdzie jeszcze nic nie kosztują: na etapie projektowania.",
  "Beratung zum „Compendium on innovative medical technologies“ sowie Plenarbeitrag beim 3rd WHO Global Forum on Medical Devices zu Medizintechnik in Konfliktsituationen.": "Doradztwo dotyczące „Compendium on innovative medical technologies“ oraz wystąpienie plenarne na 3rd WHO Global Forum on Medical Devices na temat techniki medycznej w sytuacjach konfliktu.",
  "Zur WHO-Publikation": "Do publikacji WHO",
  "Lehrvortrag zu den europäischen und rechtlichen Grundlagen der Medizintechnik.": "Wykład na temat europejskich i prawnych podstaw techniki medycznej.",
  "Aktive Mitarbeit und Fachvorträge für den Österreichischen Verband der Krankenhaustechniker:innen.": "Aktywna współpraca i wykłady specjalistyczne dla Austriackiego Stowarzyszenia Techników Szpitalnych.",
  "Zum ÖVKT": "Do ÖVKT",
  "Zum Medizintechnik-Cluster": "Do klastra techniki medycznej",
  "Betreuung einer Masterarbeit": "Opieka nad pracą magisterską",
  "Academic Advisor für die Masterarbeit „Enablers and barriers in medical device export to Syria“ (qualitative Studie) an der University of Copenhagen, November 2016 – Dezember 2017.": "Opiekun naukowy pracy magisterskiej „Enablers and barriers in medical device export to Syria“ (badanie jakościowe) na University of Copenhagen, listopad 2016 – grudzień 2017.",
 },
 "ro": {
  "Referenzen": "Referințe",
  "Ausgewählte Projekte aus der langjährigen Erfahrung unseres Teams.": "Proiecte selectate din experiența îndelungată a echipei noastre.",
  "Kompetenz aus Projekten": "Competență din proiecte",
  "Wissen aus Forschung": "Cunoaștere din cercetare",
  "Vertrauen durch Erfahrung": "Încredere prin experiență",
  "Projektreferenzen": "Referințe de proiect",
  "Realisierte Projekte": "Proiecte realizate",
  "Unsere Referenzen spiegeln langjährige Erfahrung, technisches Know-how und individuelle Lösungen wider. Gemeinsam mit unseren Kunden realisieren wir Projekte, die höchsten fachlichen und qualitativen Ansprüchen gerecht werden.": "Referințele noastre reflectă experiența îndelungată, know-how-ul tehnic și soluțiile individuale. Împreună cu clienții noștri realizăm proiecte care îndeplinesc cele mai înalte exigențe profesionale și de calitate.",
  "Wählen Sie oben eine Kategorie, um die zugehörigen Projekte anzuzeigen.": "Selectați o categorie de mai sus pentru a afișa proiectele aferente.",
  "Wählen Sie oben eine Kategorie, um die Beiträge anzuzeigen.": "Selectați o categorie de mai sus pentru a afișa intrările.",
  "Akademisches und Wissenschaft": "Mediu academic și știință",
  "Wissenschaft &amp; Forschung": "Știință și cercetare",
  "Wissenschaft und Forschung sind fester Bestandteil unseres Selbstverständnisses. Durch die Mitwirkung an Forschungsprojekten, wissenschaftlichen Beiträgen und dem fachlichen Austausch leisten wir einen aktiven Beitrag zur Weiterentwicklung moderner Medizintechnik und evidenzbasierter Lösungen.": "Știința și cercetarea fac parte integrantă din identitatea noastră. Prin implicarea în proiecte de cercetare, contribuții științifice și schimb profesional, contribuim activ la dezvoltarea tehnologiei medicale moderne și a soluțiilor bazate pe dovezi.",
  "Consulting und Lehre": "Consultanță și predare",
  "Consulting &amp; Lehre": "Consultanță și predare",
  "Herstellerunabhängige Beratung mit technischem Know-how – individuell, praxisnah und lösungsorientiert – sowie akademische Lehr- und Betreuungstätigkeit.": "Consultanță independentă de producători, cu know-how tehnic – individuală, practică și orientată spre soluții – precum și activitate academică de predare și îndrumare.",
  "Ihr Projekt in erfahrenen Händen": "Proiectul dvs. în mâini experimentate",
  "Projekt besprechen": "Discutați proiectul",
  "Schließen": "Închide",
  "Vorheriges Bild": "Imaginea anterioară",
  "Nächstes Bild": "Imaginea următoare",
  "Alle": "Toate",
  "Bilder": "imagini",
  "Details ansehen": "Vedeți detalii",
  "AKH Wien · Persönlich": "AKH Viena · Personal",
  "AKH Wien · Leitung": "AKH Viena · Coordonare",
  "Österreich": "Austria",
  "Schweiz": "Elveția",
  "Internationale Projekte": "Proiecte internaționale",
  "Konferenzen": "Conferințe",
  "Publikationen": "Publicații",
  "Wissenschaftliche Beiträge": "Contribuții științifice",
  "Consulting": "Consultanță",
  "Lehre": "Predare",
  "Vortrag": "Prezentare",
  "Plenarbeitrag": "Contribuție plenară",
  "Promotion": "Doctorat",
  "Internationale Beratung": "Consultanță internațională",
  "Lehrvortrag": "Prelegere",
  "Fachvorträge": "Prezentări de specialitate",
  "Akademischer Berater": "Consilier academic",
  "1 Jahr": "1 an", "2 Jahre": "2 ani", "2,5 Jahre": "2,5 ani",
  "3 Jahre": "3 ani", "4 Jahr": "4 ani", "4 Jahre": "4 ani", "5 Jahre": "5 ani",
  "Oral Presentation &middot; The European Health Economics Association (EuHEA), 14.–16. Juli 2016.": "Prezentare orală &middot; The European Health Economics Association (EuHEA), 14–16 iulie 2016.",
  "Poster Presentation &middot; 9th European Public Health Conference „Health for All – All for Health“, 9.–12. November 2016, ACV, Wien.": "Prezentare poster &middot; 9th European Public Health Conference „Health for All – All for Health“, 9–12 noiembrie 2016, ACV, Viena.",
  "Plenary Contribution &middot; 3rd WHO Global Forum on Medical Devices, 12.05.2017.": "Contribuție plenară &middot; 3rd WHO Global Forum on Medical Devices, 12 mai 2017.",
  "Doktorarbeit (PhD)": "Teză de doctorat (PhD)",
  "„Leading health care facilities in times of armed conflict: what are the constraints for medical equipment management?“ – Dissertation zur Medizintechnik-Beschaffung unter Extrembedingungen.": "„Leading health care facilities in times of armed conflict: what are the constraints for medical equipment management?“ – Teză de doctorat privind achiziția de tehnologie medicală în condiții extreme.",
  "Qualitätssicherung in der Planung": "Asigurarea calității în proiectare",
  "Zur VKMB": "Către VKMB",
  "Im Auftrag der VKMB begleiten wir die Medizintechnik-Planung beratend und sichern gemeinsam mit dem Team des Kunden die Qualität der erstellten Planungsunterlagen. Ein unabhängiger zweiter Blick auf Vollständigkeit, technische Plausibilität und Betriebstauglichkeit – damit Entscheidungen auf belastbaren Grundlagen fallen und Korrekturen dort erfolgen, wo sie noch nichts kosten: in der Planung.": "La solicitarea VKMB oferim consultanță pentru proiectarea tehnologiei medicale și, împreună cu echipa clientului, asigurăm calitatea documentațiilor de proiectare elaborate. O a doua opinie independentă privind exhaustivitatea, plauzibilitatea tehnică și adecvarea pentru exploatare – astfel încât deciziile să se bazeze pe fundamente solide, iar corecțiile să aibă loc acolo unde încă nu costă nimic: în faza de proiectare.",
  "Beratung zum „Compendium on innovative medical technologies“ sowie Plenarbeitrag beim 3rd WHO Global Forum on Medical Devices zu Medizintechnik in Konfliktsituationen.": "Consultanță privind „Compendium on innovative medical technologies“, precum și o contribuție plenară la 3rd WHO Global Forum on Medical Devices privind tehnologia medicală în situații de conflict.",
  "Zur WHO-Publikation": "Către publicația OMS",
  "Lehrvortrag zu den europäischen und rechtlichen Grundlagen der Medizintechnik.": "Prelegere despre bazele europene și juridice ale tehnologiei medicale.",
  "Aktive Mitarbeit und Fachvorträge für den Österreichischen Verband der Krankenhaustechniker:innen.": "Colaborare activă și prezentări de specialitate pentru Asociația Austriacă a Tehnicienilor de Spital.",
  "Zum ÖVKT": "Către ÖVKT",
  "Zum Medizintechnik-Cluster": "Către clusterul de tehnologie medicală",
  "Betreuung einer Masterarbeit": "Îndrumarea unei lucrări de master",
  "Academic Advisor für die Masterarbeit „Enablers and barriers in medical device export to Syria“ (qualitative Studie) an der University of Copenhagen, November 2016 – Dezember 2017.": "Consilier academic pentru lucrarea de master „Enablers and barriers in medical device export to Syria“ (studiu calitativ) la University of Copenhagen, noiembrie 2016 – decembrie 2017.",
 },
}

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

# --- Filterbares Projektkarten-Raster ---
_REF_FLABEL = {"oesterreich": "Österreich",
               "schweiz": "Schweiz",
               "international": "Internationale Projekte"}
# AKH-Wien-Gruppen (persönlich + Leitung) zu einer Kategorie "Österreich" zusammenfassen
_REF_GID_MAP = {"akh-persoenlich": "oesterreich", "akh-leitung": "oesterreich"}
def _ref_gid(g):
    return _REF_GID_MAP.get(g["id"], g["id"])
def _ref_filter_defs():
    order = []; counts = {}
    for g in _ref_data["groups"]:
        gid = _ref_gid(g)
        if gid not in counts:
            order.append(gid); counts[gid] = 0
        counts[gid] += len(g["projects"])
    return [(gid, _REF_FLABEL.get(gid, gid), counts[gid]) for gid in order]

def _ref_card(p, gid, client, lang="de"):
    n = _ref_eurnum(p.get("kosten", ""))
    name = _reft(lang, p["name"])
    umfang = _reft(lang, p.get("umfang", ""))
    chips = []
    if p.get("lph"):   chips.append(f'<span class="m-refc-chip">{_html.escape(p["lph"])}</span>')
    if p.get("dauer"): chips.append(f'<span class="m-refc-chip">{_html.escape(_uit(lang, p["dauer"]))}</span>')
    imgs = [_ap(lang, i) for i in (p.get("imgs") or [])]
    if imgs:
        data_imgs = _html.escape(json.dumps(imgs), quote=True)
        data_full = _html.escape(umfang, quote=True)
        cnt = len(imgs)
        countbadge = (f'<span class="m-refc-cover-n">{cnt} {_uit(lang, "Bilder")}</span>' if cnt > 1 else '')
        cover = (
            '            <div class="m-refc-cover">\n'
            f'              <img src="{imgs[0]}" alt="{_html.escape(name)}" loading="lazy">\n'
            f'              {countbadge}\n'
            '            </div>\n')
        return (
f'          <article class="m-refc has-img is-clickable" data-group="{gid}" data-imgs="{data_imgs}" data-full="{data_full}" tabindex="0" role="button" aria-label="{_html.escape(name)} – {_uit(lang, "Details ansehen")}">\n'
+ cover +
'            <div class="m-refc-head">\n'
f'              <span class="m-refc-client">{_html.escape(client)}</span>\n'
f'              <span class="m-refc-vol">{_ref_vol(n)}</span>\n'
'            </div>\n'
f'            <h3 class="m-refc-name">{_html.escape(name)}</h3>\n'
f'            <p class="m-refc-desc">{_html.escape(umfang)}</p>\n'
f'            <div class="m-refc-foot">{"".join(chips)}</div>\n'
'          </article>')
    return (
f'          <article class="m-refc" data-group="{gid}">\n'
'            <div class="m-refc-head">\n'
f'              <span class="m-refc-client">{_html.escape(client)}</span>\n'
f'              <span class="m-refc-vol">{_ref_vol(n)}</span>\n'
'            </div>\n'
f'            <h3 class="m-refc-name">{_html.escape(name)}</h3>\n'
f'            <p class="m-refc-desc{" m-refc-desc--full" if p.get("full") else ""}">{_html.escape(umfang)}</p>\n'
f'            <div class="m-refc-foot">{"".join(chips)}</div>\n'
'          </article>')

_ref_cards_html = "\n".join(
    _ref_card(p, _ref_gid(g), g["client"]) for g in _ref_data["groups"] for p in g["projects"])

_ref_counts = {g["id"]: len(g["projects"]) for g in _ref_data["groups"]}
_ref_total = sum(_ref_counts.values())

def _ref_fbtn(fid, label, count, active=False):
    act = " is-active" if active else ""
    return (f'        <button class="m-ref-fbtn{act}" data-filter="{fid}">{_html.escape(label)}'
            f'<span class="m-ref-fbtn-n">{count}</span></button>')

def _ref_cards_html_for(lang):
    return "\n".join(
        _ref_card(p, _ref_gid(g), g["client"], lang)
        for g in _ref_data["groups"] for p in g["projects"])

def _ref_filter_html_for(lang):
    return "\n".join(
        [_ref_fbtn("all", _uit(lang, "Alle"), _ref_total, active=False)]
        + [_ref_fbtn(gid, _uit(lang, label), cnt) for gid, label, cnt in _ref_filter_defs()])

_ref_filter_html = "\n".join(
    [_ref_fbtn("all", "Alle", _ref_total, active=False)]
    + [_ref_fbtn(gid, label, cnt) for gid, label, cnt in _ref_filter_defs()])

# --- medeqon-Icons für Wissenschaft & Forschung (Linien-Stil, blauer Punkt) ---
_ICON_INK = "#0F1B2C"; _ICON_DOT = "#004AAD"
_WISS_ICONS = {
    # Konferenzen – Mikrofon am Rednerpult, blauer Punkt als Highlight
    "konferenzen": (
        '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Konferenzen">'
        f'<rect x="19.5" y="7.5" width="9" height="17" rx="4.5" stroke="{_ICON_INK}" stroke-width="2.4"/>'
        f'<path d="M13.5 21a10.5 10.5 0 0 0 21 0" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<path d="M24 31.5V39" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<path d="M18 39h12" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<circle cx="24" cy="12.6" r="2.7" fill="{_ICON_DOT}"/>'
        '</svg>'),
    # Publikationen – Dokument mit Textzeilen, blauer Punkt als Schluss-Punkt
    "publikationen": (
        '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Publikationen">'
        f'<path d="M13 8h14l8 8v24H13z" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linejoin="round"/>'
        f'<path d="M27 8v8h8" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linejoin="round"/>'
        f'<path d="M18 23h12" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<path d="M18 28.5h12" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<path d="M18 34h6" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<circle cx="29" cy="34" r="2.3" fill="{_ICON_DOT}"/>'
        '</svg>'),
    # Wissenschaftliche Beiträge – Doktorhut, blauer Punkt als Quasten-Perle
    "beitraege": (
        '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Wissenschaftliche Beiträge">'
        f'<path d="M24 10 40 17 24 24 8 17Z" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linejoin="round"/>'
        f'<path d="M15 20.5v6c0 2.6 18 2.6 18 0v-6" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linejoin="round"/>'
        f'<path d="M40 17v10" stroke="{_ICON_INK}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<circle cx="40" cy="29.4" r="2.7" fill="{_ICON_DOT}"/>'
        '</svg>'),
}

# --- Generisches Filter-Karten-Raster (Wissenschaft, Consulting) ---
def _grid_card(gid, it, hidden=False, lang="de"):
    badge = _uit(lang, it.get("badge", "")); title = _uit(lang, it["title"]); desc = _uit(lang, it["desc"])
    img = _ap(lang, it.get("img")); link = it.get("link")
    icon = None; icon_key = None
    if not img:
        icon_key = it.get("icon") or gid
        icon = _WISS_ICONS.get(icon_key)
    has_media = bool(img or icon)
    cls = ("m-refc has-img" if has_media else "m-refc") + (" is-hidden" if hidden else "")
    if img:
        szcls = (" m-refc-img--" + it["imgsize"]) if it.get("imgsize") else ""
        imghtml = f'            <div class="m-refc-img{szcls}"><img src="{img}" alt="{_html.escape(it.get("imgalt", title))}" loading="lazy"></div>\n'
    elif icon:
        imghtml = f'            <div class="m-refc-icon m-refc-icon--{icon_key}">{icon}</div>\n'
    else:
        imghtml = ''
    bg = f'<span class="m-refc-client">{_html.escape(badge)}</span>' if badge else ''
    head = ('            <div class="m-refc-head">' + bg + '</div>\n') if bg else ''
    linkhtml = ''
    if link:
        url, label = link
        linkhtml = f'            <a class="m-refc-link" href="{url}" target="_blank" rel="noopener">{_html.escape(_uit(lang, label))} &#8599;</a>\n'
    return (
f'          <article class="{cls}" data-group="{gid}">\n'
+ imghtml + head +
f'            <h3 class="m-refc-name">{_html.escape(title)}</h3>\n'
f'            <p class="m-refc-desc m-refc-desc--full">{desc}</p>\n'
+ linkhtml +
'          </article>')

def _filter_block(groups, add_all=True, all_label="Alle", collapsed=False,
                  hint="Wählen Sie oben eine Kategorie, um die Beiträge anzuzeigen.", lang="de"):
    total = sum(len(items) for _, _, items in groups)
    chips = []
    if add_all:
        chips.append(_ref_fbtn("all", _uit(lang, all_label), total, active=(not collapsed)))
    for idx, (gid, label, items) in enumerate(groups):
        chips.append(_ref_fbtn(gid, _uit(lang, label), len(items),
                               active=(not collapsed and not add_all and idx == 0)))
    if collapsed:
        active_gid = "\0"  # kein Treffer -> alle Karten verborgen
    else:
        active_gid = None if add_all else (groups[0][0] if groups else None)
    cards = [_grid_card(gid, it, hidden=(active_gid is not None and gid != active_gid), lang=lang)
             for gid, label, items in groups for it in items]
    root_cls = "m-filterable is-collapsed" if collapsed else "m-filterable"
    return ('    <div class="' + root_cls + '">\n'
            '      <div class="m-ref-filter">\n' + "\n".join(chips) + '\n      </div>\n'
            '      <div class="m-ref-grid">\n' + "\n".join(cards) + '\n      </div>\n'
            '    </div>')

def _pub_desc(authors, venue, doi=None, isbn=None):
    d = _html.escape(authors) + " &middot; " + _html.escape(venue)
    if doi:
        d += (f'. <a class="m-refc-ilink" href="https://doi.org/{doi}" target="_blank" '
              f'rel="noopener">DOI: {_html.escape(doi)}</a>')
    elif isbn:
        d += ". ISBN " + _html.escape(isbn)
    else:
        d += "."
    return d

_CONF_ITEMS = [
    {"badge": "Vortrag",
     "title": "War and Public Health: The Effects of War on the Public Health System by the Example of the Syrian Civil Conflict",
     "desc": "Oral Presentation &middot; The European Health Economics Association (EuHEA), 14.–16. Juli 2016."},
    {"badge": "Poster",
     "title": "Public health and armed conflict: what are the constraints for medical equipment management?",
     "desc": "Poster Presentation &middot; 9th European Public Health Conference „Health for All – All for Health“, 9.–12. November 2016, ACV, Wien."},
    {"badge": "Plenarbeitrag",
     "title": "Medical Equipment used in Armed Conflict Situations",
     "desc": "Plenary Contribution &middot; 3rd WHO Global Forum on Medical Devices, 12.05.2017."},
]

_PUB_ITEMS = [
    {"badge": "2017", "title": "Managing work-related stress in humanitarian fieldwork: aid worker and resilience resources",
     "desc": _pub_desc("Schmidt G.", "International Journal of Emergency Management, Vol. 13, No. 4, S. 382–397")},
    {"badge": "2016", "title": "War and public health: effects of the Syrian civil war on the public health system",
     "desc": _pub_desc("Schmidt G.", "Defence Review, Vol. 144, Special Issue 2016/1, S. 129–136")},
    {"badge": "2016", "title": "The complications of emergency management in the Syrian civil war",
     "desc": _pub_desc("Schmidt G.", "Defence Review, Vol. 144, Special Issue 2016/2, S. 144–153")},
    {"badge": "2016", "title": "Hospitals and war: medical departments and personnel",
     "desc": _pub_desc("Schmidt G. und Schmidt E.", "Int. J. Behavioural and Healthcare Research, Vol. 6, No. 1, S. 1–14", doi="10.1504/IJBHR.2016.10002015")},
    {"badge": "2016", "title": "Safety Considerations on MRI Systems for Firefighters and Paramedics",
     "desc": _pub_desc("Schmidt G.", "International Journal of Hospital Research, Vol. 5, No. 1, S. 7–12", doi="10.15171/ijhr.2016.02")},
    {"badge": "2016", "title": "Private sector involvement in times of armed conflict: what are the constraints for trading medical equipment?",
     "desc": _pub_desc("Schmidt G.", "Journal of Emergency Management, Vol. 14, No. 6, S. 413–421", doi="10.5055/jem.2016.0305")},
    {"badge": "2014", "title": "Einsatzkräfte an der Magnetresonanztomographie: Erste Bestandsaufnahme. Erkennen von Gefahren und sicheres Vorgehen im Notfall",
     "desc": _pub_desc("Schmidt G.", "104 S., Saarbrücken: AV Akademiker Verlag", isbn="978-3-639-67516-0")},
]

_WISS_GROUPS = [
    ("konferenzen", "Konferenzen", _CONF_ITEMS),
    ("publikationen", "Publikationen", _PUB_ITEMS),
    ("beitraege", "Wissenschaftliche Beiträge", [
        {"badge": "Promotion", "title": "Doktorarbeit (PhD)",
         "desc": "„Leading health care facilities in times of armed conflict: what are the constraints for medical equipment management?“ – Dissertation zur Medizintechnik-Beschaffung unter Extrembedingungen."},
    ]),
]

_CONS_GROUPS = [
    ("consulting", "Consulting", [
        {"badge": "Qualitätssicherung in der Planung", "title": "VKMB",
         "desc": "Im Auftrag der VKMB begleiten wir die Medizintechnik-Planung beratend und sichern gemeinsam mit dem Team des Kunden die Qualität der erstellten Planungsunterlagen. Ein unabhängiger zweiter Blick auf Vollständigkeit, technische Plausibilität und Betriebstauglichkeit – damit Entscheidungen auf belastbaren Grundlagen fallen und Korrekturen dort erfolgen, wo sie noch nichts kosten: in der Planung.",
         "img": "assets/ref/vkmb-logo.png",
         "imgalt": "VAMED-KMB Krankenhausmanagement und Betriebsführungsges.m.b.H. (VKMB)",
         "link": ("https://vkmb.com/", "Zur VKMB")},
        {"badge": "Internationale Beratung", "title": "World Health Organization (WHO)",
         "desc": "Beratung zum „Compendium on innovative medical technologies“ sowie Plenarbeitrag beim 3rd WHO Global Forum on Medical Devices zu Medizintechnik in Konfliktsituationen.",
         "img": "assets/ref/who-logo.png", "imgalt": "World Health Organization",
         "link": ("https://www.who.int/publications/i/item/9789240095212", "Zur WHO-Publikation")},
    ]),
    ("lehre", "Lehre", [
        {"badge": "Lehrvortrag", "title": "Kepler Universitätsklinikum Linz",
         "desc": "Lehrvortrag zu den europäischen und rechtlichen Grundlagen der Medizintechnik.",
         "img": "assets/ref/kepler-logo.png", "imgalt": "Kepler Universitätsklinikum Linz", "imgsize": "lg",
         "link": ("https://www.biz-up.at/cluster-kooperationen/medizintechnik-cluster", "Zum Medizintechnik-Cluster")},
        {"badge": "Fachvorträge", "title": "ÖVKT",
         "desc": "Aktive Mitarbeit und Fachvorträge für den Österreichischen Verband der Krankenhaustechniker:innen.",
         "img": "assets/ref/oevkt-logo.jpg", "imgalt": "Österreichischer Verband der Krankenhaustechniker:innen (ÖVKT)", "imgsize": "md",
         "link": ("https://www.oevkt.at/neu/index.php", "Zum ÖVKT")},
        {"badge": "Akademischer Berater", "title": "Betreuung einer Masterarbeit", "icon": "beitraege",
         "desc": "Academic Advisor für die Masterarbeit „Enablers and barriers in medical device export to Syria“ (qualitative Studie) an der University of Copenhagen, November 2016 – Dezember 2017."},
    ]),
]

BODY_REFERENZEN = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Referenzen</span>
    <h1>Referenzen<span class="end-dot">.</span></h1>
    <p class="lede">Ausgewählte Projekte aus der langjährigen Erfahrung unseres Teams.</p>
  </div>
</section>

<section class="m-section m-refstats-bg" style="background-image:url(assets/slogan-bg.jpg)">
  <div class="m-shell">
    <p class="m-ref-slogan">
      <span>Kompetenz aus Projekten<i>.</i></span>
      <span>Wissen aus Forschung<i>.</i></span>
      <span>Vertrauen durch Erfahrung<i>.</i></span>
    </p>
  </div>
</section>

<section class="m-section" id="projektreferenzen">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Projektreferenzen</span>
      <h2 class="m-bigH">Realisierte Projekte<span class="end-dot">.</span></h2>
      <div class="sub">Unsere Referenzen spiegeln langjährige Erfahrung, technisches Know-how und individuelle Lösungen wider. Gemeinsam mit unseren Kunden realisieren wir Projekte, die höchsten fachlichen und qualitativen Ansprüchen gerecht werden.</div>
    </div>
    <div class="m-filterable is-collapsed">
      <div class="m-ref-filter">
''' + _ref_filter_html + '''
      </div>
      <div class="m-ref-grid">
''' + _ref_cards_html + '''
      </div>
    </div>
  </div>
</section>

<section class="m-section alt">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Akademisches und Wissenschaft</span>
      <h2 class="m-bigH">Wissenschaft &amp; Forschung<span class="end-dot">.</span></h2>
      <div class="sub">Wissenschaft und Forschung sind fester Bestandteil unseres Selbstverständnisses. Durch die Mitwirkung an Forschungsprojekten, wissenschaftlichen Beiträgen und dem fachlichen Austausch leisten wir einen aktiven Beitrag zur Weiterentwicklung moderner Medizintechnik und evidenzbasierter Lösungen.</div>
    </div>
''' + _filter_block(_WISS_GROUPS, add_all=True, collapsed=True) + '''
  </div>
</section>

<section class="m-section alt2">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Consulting und Lehre</span>
      <h2 class="m-bigH">Consulting &amp; Lehre<span class="end-dot">.</span></h2>
      <div class="sub">Herstellerunabhängige Beratung mit technischem Know-how – individuell, praxisnah und lösungsorientiert – sowie akademische Lehr- und Betreuungstätigkeit.</div>
    </div>
''' + _filter_block(_CONS_GROUPS, add_all=True, collapsed=True) + '''
  </div>
</section>

<div class="m-lb" id="refLightbox" hidden aria-hidden="true">
  <div class="m-lb-backdrop" data-lb-close></div>
  <div class="m-lb-panel" role="dialog" aria-modal="true" aria-labelledby="lbTitle">
    <button class="m-lb-x" data-lb-close aria-label="Schließen">&times;</button>
    <div class="m-lb-media">
      <img class="m-lb-img" src="" alt="">
      <button class="m-lb-nav m-lb-prev" aria-label="Vorheriges Bild">&#8249;</button>
      <button class="m-lb-nav m-lb-next" aria-label="Nächstes Bild">&#8250;</button>
      <div class="m-lb-dots"></div>
    </div>
    <div class="m-lb-body">
      <span class="m-lb-client"></span>
      <h3 class="m-lb-title" id="lbTitle"></h3>
      <p class="m-lb-desc"></p>
      <div class="m-lb-foot"></div>
    </div>
  </div>
</div>

<script>
document.querySelectorAll('.m-filterable').forEach(function(root){
  var btns=root.querySelectorAll('.m-ref-fbtn'),cards=root.querySelectorAll('.m-refc');
  btns.forEach(function(b){b.addEventListener('click',function(){
    var f=b.getAttribute('data-filter');
    // Nochmaliges Klicken auf die bereits aktive Kategorie -> wieder zuklappen
    if(b.classList.contains('is-active') && !root.classList.contains('is-collapsed')){
      root.classList.add('is-collapsed');
      btns.forEach(function(x){x.classList.remove('is-active');});
      cards.forEach(function(c){c.classList.add('is-hidden');});
      return;
    }
    root.classList.remove('is-collapsed');
    btns.forEach(function(x){x.classList.toggle('is-active',x===b);});
    cards.forEach(function(c){c.classList.toggle('is-hidden',!(f==='all'||c.getAttribute('data-group')===f));});
  });});
});
(function(){
  var lb=document.getElementById('refLightbox'); if(!lb) return;
  var img=lb.querySelector('.m-lb-img'), dots=lb.querySelector('.m-lb-dots'),
      prev=lb.querySelector('.m-lb-prev'), next=lb.querySelector('.m-lb-next'),
      media=lb.querySelector('.m-lb-media'),
      elClient=lb.querySelector('.m-lb-client'), elTitle=lb.querySelector('.m-lb-title'),
      elDesc=lb.querySelector('.m-lb-desc'), elFoot=lb.querySelector('.m-lb-foot');
  var imgs=[], idx=0, lastFocus=null;
  function show(i){
    idx=(i+imgs.length)%imgs.length;
    img.src=imgs[idx]; img.alt=elTitle.textContent+' – Bild '+(idx+1);
    dots.querySelectorAll('button').forEach(function(d,k){d.classList.toggle('is-on',k===idx);});
  }
  function open(card){
    try{imgs=JSON.parse(card.getAttribute('data-imgs'))||[];}catch(e){imgs=[];}
    if(!imgs.length) return;
    var cl=card.querySelector('.m-refc-client'), nm=card.querySelector('.m-refc-name'),
        ft=card.querySelector('.m-refc-foot');
    elClient.textContent=cl?cl.textContent:'';
    elTitle.textContent=nm?nm.textContent:'';
    elDesc.textContent=card.getAttribute('data-full')||'';
    elFoot.innerHTML=ft?ft.innerHTML:'';
    dots.innerHTML='';
    var multi=imgs.length>1;
    media.classList.toggle('is-single',!multi);
    if(multi){imgs.forEach(function(_,k){var d=document.createElement('button');
      d.type='button'; d.setAttribute('aria-label','Bild '+(k+1));
      d.addEventListener('click',function(){show(k);}); dots.appendChild(d);});}
    lastFocus=document.activeElement;
    lb.hidden=false; lb.setAttribute('aria-hidden','false');
    document.body.style.overflow='hidden';
    show(0);
    lb.querySelector('.m-lb-x').focus();
  }
  function close(){
    lb.hidden=true; lb.setAttribute('aria-hidden','true');
    document.body.style.overflow=''; img.src='';
    if(lastFocus&&lastFocus.focus) lastFocus.focus();
  }
  document.querySelectorAll('.m-refc.is-clickable').forEach(function(card){
    card.addEventListener('click',function(){open(card);});
    card.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();open(card);}});
  });
  lb.querySelectorAll('[data-lb-close]').forEach(function(x){x.addEventListener('click',close);});
  prev.addEventListener('click',function(){show(idx-1);});
  next.addEventListener('click',function(){show(idx+1);});
  document.addEventListener('keydown',function(e){
    if(lb.hidden) return;
    if(e.key==='Escape') close();
    else if(e.key==='ArrowLeft') show(idx-1);
    else if(e.key==='ArrowRight') show(idx+1);
  });
})();
</script>

<section class="m-cta-banner" style="background-image:url(assets/cta-banner.jpg)">
  <div class="m-shell">
    <div class="m-cta-banner-copy">
      <div class="line"></div>
      <h2>Ihr Projekt in erfahrenen Händen<span class="end-dot">.</span></h2>
      <a class="m-cta-link" href="kontakt.html">Projekt besprechen</a>
    </div>
  </div>
</section>'''

_REF_CHROME = [
    "Unsere Referenzen spiegeln langjährige Erfahrung, technisches Know-how und individuelle Lösungen wider. Gemeinsam mit unseren Kunden realisieren wir Projekte, die höchsten fachlichen und qualitativen Ansprüchen gerecht werden.",
    "Wissenschaft und Forschung sind fester Bestandteil unseres Selbstverständnisses. Durch die Mitwirkung an Forschungsprojekten, wissenschaftlichen Beiträgen und dem fachlichen Austausch leisten wir einen aktiven Beitrag zur Weiterentwicklung moderner Medizintechnik und evidenzbasierter Lösungen.",
    "Herstellerunabhängige Beratung mit technischem Know-how – individuell, praxisnah und lösungsorientiert – sowie akademische Lehr- und Betreuungstätigkeit.",
    "Ausgewählte Projekte aus der langjährigen Erfahrung unseres Teams.",
    "Wählen Sie oben eine Kategorie, um die zugehörigen Projekte anzuzeigen.",
    "Akademisches und Wissenschaft",
    "Wissenschaft &amp; Forschung",
    "Consulting &amp; Lehre",
    "Consulting und Lehre",
    "Ihr Projekt in erfahrenen Händen",
    "Kompetenz aus Projekten",
    "Vertrauen durch Erfahrung",
    "Wissen aus Forschung",
    "Projektreferenzen",
    "Realisierte Projekte",
    "Projekt besprechen",
    "Vorheriges Bild",
    "Nächstes Bild",
    "Schließen",
    "Referenzen",
]
_REF_JSWORD = {"en": "Image", "pl": "Obraz", "ro": "Imaginea"}

def _body_referenzen(lang):
    if lang == "de":
        return BODY_REFERENZEN
    body = BODY_REFERENZEN
    # 1) Daten-Blöcke gegen sprachspezifische Varianten tauschen
    body = body.replace(_ref_filter_html, _ref_filter_html_for(lang))
    body = body.replace(_ref_cards_html, _ref_cards_html_for(lang))
    body = body.replace(_filter_block(_WISS_GROUPS, add_all=True, collapsed=True),
                        _filter_block(_WISS_GROUPS, add_all=True, collapsed=True, lang=lang))
    body = body.replace(_filter_block(_CONS_GROUPS, add_all=True, collapsed=True),
                        _filter_block(_CONS_GROUPS, add_all=True, collapsed=True, lang=lang))
    # 2) statische Seiten-Texte übersetzen (längste zuerst → keine Teilkollisionen)
    for de_s in sorted(_REF_CHROME, key=len, reverse=True):
        body = body.replace(de_s, _uit(lang, de_s))
    # 3) Asset-Pfade root-absolut, Kontakt-Link sprachspezifisch, JS-Wort „Bild"
    body = body.replace("url(assets/", "url(/assets/")
    body = body.replace('href="kontakt.html"', f'href="/{lang}/kontakt.html"')
    jw = _REF_JSWORD[lang]
    body = body.replace("' – Bild '+(idx+1)", f"' – {jw} '+(idx+1)")
    body = body.replace("'Bild '+(k+1)", f"'{jw} '+(k+1)")
    return body

BODY_REFERENZEN_EN = _body_referenzen("en")
BODY_REFERENZEN_PL = _body_referenzen("pl")
BODY_REFERENZEN_RO = _body_referenzen("ro")

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
BODY_AGB_EN = load_content("agb.en");           BODY_AGB_PL = load_content("agb.pl");           BODY_AGB_RO = load_content("agb.ro")
BODY_DATENSCHUTZ_EN = load_content("datenschutz.en"); BODY_DATENSCHUTZ_PL = load_content("datenschutz.pl"); BODY_DATENSCHUTZ_RO = load_content("datenschutz.ro")
BODY_IMPRESSUM_EN = load_content("impressum.en"); BODY_IMPRESSUM_PL = load_content("impressum.pl"); BODY_IMPRESSUM_RO = load_content("impressum.ro")

# ---- Karriere / Offene Positionen ---------------------------------------
# Neue Stelle ausschreiben: einfach ein Dict in _JOBS ergänzen. Ist die Liste
# leer, zeigt die Seite automatisch „aktuell keine Positionen offen".
#   {"title": "Medizintechniker:in (m/w/d)",
#    "type": "Vollzeit", "location": "Wien / Hagenbrunn",
#    "intro": "Kurzbeschreibung der Rolle …",
#    "tasks": ["Aufgabe 1", "Aufgabe 2"],
#    "profile": ["Anforderung 1", "Anforderung 2"]},
_JOBS = []

_KARRIERE_MAIL = "office@medeqon.com"

def _job_mail(subject):
    return ("mailto:" + _KARRIERE_MAIL + "?subject="
            + _urlparse.quote(subject))

def _job_html(job):
    title = _html.escape(job["title"])
    meta = []
    for key in ("type", "location"):
        if job.get(key):
            meta.append(f'<span class="m-job-chip">{_html.escape(job[key])}</span>')
    meta_html = ('<span class="m-job-meta">' + "".join(meta) + '</span>') if meta else ''
    lead = f'          <p class="m-ac-lead">{_html.escape(job["intro"])}</p>\n' if job.get("intro") else ''
    cols = []
    if job.get("tasks"):
        items = "\n".join(f'                <li>{_html.escape(t)}</li>' for t in job["tasks"])
        cols.append('            <div class="m-job-col">\n'
                    '              <h4 class="m-job-h">Ihre Aufgaben</h4>\n'
                    f'              <ul class="ring-list">\n{items}\n              </ul>\n'
                    '            </div>')
    if job.get("profile"):
        items = "\n".join(f'                <li>{_html.escape(t)}</li>' for t in job["profile"])
        cols.append('            <div class="m-job-col">\n'
                    '              <h4 class="m-job-h">Ihr Profil</h4>\n'
                    f'              <ul class="ring-list">\n{items}\n              </ul>\n'
                    '            </div>')
    cols_html = ('          <div class="m-job-cols">\n' + "\n".join(cols) + '\n          </div>\n') if cols else ''
    subject = job.get("mail_subject") or ("Bewerbung: " + job["title"])
    apply_html = (f'          <a class="m-btn" href="{_job_mail(subject)}">Jetzt bewerben'
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:17px;height:17px"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></a>\n')
    return (
'      <details class="m-ac">\n'
f'        <summary><span class="m-ac-title">{title}</span>{meta_html}' + CHEV + '</summary>\n'
'        <div class="m-ac-body">\n'
+ lead + cols_html + apply_html +
'        </div>\n'
'      </details>')

def _jobs_section():
    if _JOBS:
        return ('      <div class="m-ac-wrap">\n'
                + "\n".join(_job_html(j) for j in _JOBS) + '\n'
                '      </div>')
    return ('      <div class="m-jobs-empty">\n'
            '        <span class="m-jobs-empty-ic" aria-hidden="true">'
            '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="15" width="32" height="24" rx="3"/><path d="M18 15v-3a3 3 0 0 1 3-3h6a3 3 0 0 1 3 3v3"/><path d="M8 26h32"/><circle cx="24" cy="26" r="2.4" class="sig-fill"/></svg></span>\n'
            '        <p class="m-jobs-empty-lead">Aktuell sind keine Positionen ausgeschrieben.</p>\n'
            '        <p class="m-jobs-empty-sub">Wir freuen uns aber jederzeit über Ihre Initiativbewerbung &ndash; siehe unten.</p>\n'
            '      </div>')

BODY_KARRIERE = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Karriere</span>
    <h1>Werden Sie Teil von medeqon<span class="end-dot">.</span></h1>
    <p class="lede">Wir verbinden technisches Know-how mit persönlicher Betreuung und arbeiten an anspruchsvollen Projekten in der Medizintechnik. Wenn Sie Qualität, Verantwortung und den direkten Draht zu Kliniken und Herstellern schätzen, freuen wir uns, Sie kennenzulernen.</p>
  </div>
</section>

<section class="m-section" id="offene-positionen">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Offene Positionen</span>
      <h2 class="m-bigH">Aktuelle Stellenangebote<span class="end-dot">.</span></h2>
      <div class="sub">Hier finden Sie unsere derzeit ausgeschriebenen Positionen. Klicken Sie eine Stelle an, um Details zu Aufgaben und Profil zu sehen.</div>
    </div>
''' + _jobs_section() + '''
  </div>
</section>

<section class="m-section alt" id="initiativbewerbung">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Initiativbewerbung</span>
      <h2 class="m-bigH">Keine passende Stelle dabei?<span class="end-dot">.</span></h2>
      <div class="sub">Überzeugen Sie uns mit Ihrer Initiativbewerbung. Wir sind laufend an engagierten Menschen interessiert, die zu medeqon passen &ndash; unabhängig davon, ob gerade eine Stelle ausgeschrieben ist.</div>
    </div>
    <div class="m-dl-note">
      <p>Senden Sie uns Ihre Bewerbungsunterlagen (Lebenslauf, kurzes Motivationsschreiben) einfach per E-Mail an <a href="mailto:''' + _KARRIERE_MAIL + '''">''' + _KARRIERE_MAIL + '''</a>. Wir melden uns persönlich bei Ihnen.</p>
      <a class="m-dl-note-btn" href="''' + _job_mail("Initiativbewerbung") + '''">Initiativbewerbung senden</a>
    </div>
  </div>
</section>'''

BODY_INDEX_EN = '''<section class="m-hero-main">
  <div class="m-shell m-hero-grid">
    <div class="m-hero-copy">
      <h1 class="m-hero-title">Engineering for medical technology<span class="end-dot">.</span></h1>
      <p class="m-hero-sub">We design, supply and support medical solutions to the highest quality standards.</p>
    </div>
    <img class="m-hero-logo" src="/assets/medeqon-logo-white.png" alt="medeqon" width="1618" height="335">
  </div>
</section>

<section class="m-slogan" style="background-image:url(/assets/slogan-bg.jpg)">
  <div class="m-shell">
    <div class="line"></div>
    <p>Your partner across the entire life cycle of medical technology<span class="em">.</span></p>
  </div>
</section>

<section class="m-section alt">
  <div class="m-shell">
    <div class="m-secH">
      <h2 class="m-bigH">Shaping progress together<span class="end-dot">.</span></h2>
      <div class="sub">With our many years of experience in medical technology, we offer a comprehensive range of services tailored individually to your requirements. Whether initial concepts and feasibility studies, strategic procurement or the detailed design of your clinic – we support you competently and reliably in every project phase.</div>
    </div>
    <div class="m-svc2-grid">
      <a class="m-svc2" href="/en/leistungen.html">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 38 L38 38 L10 12 Z"/><path d="M10 27 L21 27"/><circle cx="38" cy="38" r="3.6" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">01</span>
        </div>
        <h3 class="m-svc2-title">Medical Technology Design<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">From idea to implementation – we deliver your medical technology projects. With clear structures and efficient project control we ensure on-time delivery, cost certainty and the highest quality.</p>
      </a>
      <a class="m-svc2" href="/en/leistungen.html">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 13 h26 a3 3 0 0 1 3 3 v13 a3 3 0 0 1 -3 3 H21 l-7 6 v-6 h-2 a3 3 0 0 1 -3 -3 V16 a3 3 0 0 1 3 -3 Z"/><circle cx="23" cy="22.5" r="3.4" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">02</span>
        </div>
        <h3 class="m-svc2-title">Consulting<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Strategies with substance – consulting backed by many years of experience in medical technology. Tailored solutions that optimise processes, reduce costs and deliver lasting results.</p>
      </a>
      <a class="m-svc2" href="/en/leistungen.html">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 8 L39 16 L39 32 L24 40 L9 32 L9 16 Z"/><path d="M9 16 L24 24 L39 16"/><path d="M24 24 L24 40"/><circle cx="24" cy="24" r="3.4" class="sig-fill"/></svg></span>
          <span class="m-svc2-num">03</span>
        </div>
        <h3 class="m-svc2-title">Procurement<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Quality that lasts. Solutions that pay off. Durable, low-maintenance medical products and individually tailored solutions – with personal advice and trusting, partnership-based collaboration.</p>
      </a>
      <a class="m-svc2" href="/en/leistungen.html">
        <div class="m-svc2-top">
          <span class="m-svc2-ico"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="21" cy="21" r="11"/><path d="M29 29 L39 39"/><path d="M16.5 21.5 l3.5 3.5 l6.5 -7.5" class="sig-stroke" stroke-width="3.2"/></svg></span>
          <span class="m-svc2-num">04</span>
        </div>
        <h3 class="m-svc2-title">Inspection<span class="end-dot">.</span></h3>
        <p class="m-svc2-desc">Reliable technical service – maximum safety. Flawless equipment, legally compliant inspections, minimal downtime.</p>
      </a>
    </div>
  </div>
</section>

<!--FLYER-->

<section class="m-section" id="tco">
  <div class="m-shell">
    <div class="m-tco-truecost">
      <div class="m-tco-intro">
        <span class="m-tag">Total Cost of Ownership</span>
        <h2 class="m-bigH">What does medical technology really cost<span class="end-dot">?</span></h2>
        <p class="m-tco-lead">The purchase price is only the tip of the iceberg. Over the entire life cycle, far higher costs arise – in operation, maintenance, consumables and staff. We know these total costs in detail and factor them into every decision from the outset.</p>
        <p class="m-tco-principle">Design early · Reduce total cost · Preserve value long-term<span class="em">.</span></p>
      </div>

      <figure class="m-tco-iceberg">
          <svg viewBox="0 0 680 620" role="img" aria-label="Iceberg model: above the waterline the visible acquisition cost, below it the hidden costs such as transport, installation, commissioning, operating costs, staff, consumables, maintenance, training and disposal." xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="icebergGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0" stop-color="#6AA0D6"/>
                <stop offset="0.5" stop-color="#1E63B3"/>
                <stop offset="1" stop-color="#003278"/>
              </linearGradient>
            </defs>
            <rect x="0" y="210" width="680" height="410" fill="#E8EEF7"/>
            <polygon points="296,209 320,146 342,106 362,90 384,108 406,148 424,209" fill="#D5E1F2"/>
            <polygon points="296,210 256,250 226,330 240,432 276,520 326,586 362,602 402,584 446,516 470,426 478,330 452,250 424,210" fill="url(#icebergGrad)"/>
            <line x1="30" y1="210" x2="650" y2="210" stroke="#004AAD" stroke-width="1.5"/>
            <circle cx="30" cy="210" r="4" fill="#fff" stroke="#004AAD" stroke-width="1.5"/>
            <text x="646" y="202" font-family="IBM Plex Mono, monospace" font-size="15" letter-spacing="1" fill="#6B7785" text-anchor="end">WATERLINE</text>
            <line x1="368" y1="112" x2="452" y2="92" stroke="#0F1B2C" stroke-width="1.3"/>
            <circle cx="368" cy="112" r="4" fill="#004AAD"/>
            <text x="460" y="84" font-family="IBM Plex Mono, monospace" font-size="12" letter-spacing="1" fill="#6B7785">THE TIP</text>
            <text x="460" y="107" font-family="Hanken Grotesk, sans-serif" font-size="19" font-weight="700" fill="#0F1B2C">Acquisition cost</text>
            <g fill="#fff" font-family="Hanken Grotesk, sans-serif" font-size="15.5" font-weight="600" text-anchor="middle">
              <text x="362" y="248">Transport</text>
              <text x="362" y="286">Installation</text>
              <text x="362" y="324">Commissioning</text>
              <text x="362" y="362">Operating costs</text>
              <text x="362" y="400">Staff costs</text>
              <text x="362" y="438">Consumables</text>
              <text x="362" y="476">Maintenance</text>
              <text x="362" y="514">Training</text>
              <text x="362" y="552">Disposal</text>
            </g>
            <g>
              <line x1="54" y1="130" x2="54" y2="192" stroke="#004AAD" stroke-width="2.5"/>
              <text x="70" y="148" font-family="IBM Plex Mono, monospace" font-size="15" letter-spacing="1" fill="#004AAD">VISIBLE</text>
              <text x="70" y="171" font-family="Hanken Grotesk, sans-serif" font-size="16" fill="#6B7785">what the price</text>
              <text x="70" y="190" font-family="Hanken Grotesk, sans-serif" font-size="16" fill="#6B7785">shows</text>
              <line x1="54" y1="250" x2="54" y2="454" stroke="#004AAD" stroke-width="2.5"/>
              <text x="70" y="300" font-family="IBM Plex Mono, monospace" font-size="15" letter-spacing="1" fill="#004AAD">HIDDEN</text>
              <text x="70" y="323" font-family="Hanken Grotesk, sans-serif" font-size="16" fill="#6B7785">what the device</text>
              <text x="70" y="343" font-family="Hanken Grotesk, sans-serif" font-size="16" fill="#6B7785">really costs</text>
            </g>
          </svg>
          <figcaption>The purchase price is only the tip of the iceberg.</figcaption>
        </figure>
    </div>

    <div class="m-tco-below">
      <div class="m-tco-split-bar">
        <span class="seg-acq" style="width:20%"><em>20&thinsp;%</em>Acquisition</span>
        <span class="seg-op" style="width:80%"><em>80&thinsp;%</em>Operation over the life cycle</span>
      </div>
      <p class="m-tco-split-cap">The purchase price typically accounts for only about a fifth of the total cost – most of it arises in ongoing operation: maintenance, consumables, energy and staff.</p>
    </div>
  </div>
</section>

<section class="m-section alt" id="mtd">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">Medical Technology Design</span>
      <h2 class="m-bigH">Early Medical Technology Design that pays off across the entire life cycle<span class="end-dot">.</span></h2>
      <div class="sub">We bring medical technology into the design from the very first concept phase – this reduces costs, creates schedule and cost certainty and anchors the requirements of later operation right from the start.</div>
    </div>

    <div class="m-tco-cards">
        <div class="m-tco-card m-tco-card--early">
          <span class="m-tco-card-cap">Early integration</span>
          <p>Requirements for function, operation, infrastructure and cost efficiency are considered from the outset.</p>
        </div>
        <div class="m-tco-card m-tco-card--warn">
          <span class="m-tco-card-cap">Without Medical Technology Design</span>
          <p>Higher costs and increased coordination effort in later project phases.</p>
        </div>
        <div class="m-tco-card m-tco-card--task">
          <span class="m-tco-card-cap">Our task</span>
          <p class="m-tco-card-title">Creating reliable foundations in the early phases<span class="em">.</span></p>
        </div>
      </div>

      <figure class="m-tco-chart">
        <div class="m-tco-chart-title">Cost efficiency through early design</div>
        <svg viewBox="0 0 720 400" role="img" aria-label="Diagram: project cost over 30 years – significantly lower life-cycle cost with early design." xmlns="http://www.w3.org/2000/svg">
          <line x1="64" y1="48" x2="64" y2="320" stroke="#0F1B2C" stroke-width="1.5"/>
          <line x1="64" y1="320" x2="612" y2="320" stroke="#0F1B2C" stroke-width="1.5"/>
          <path d="M64,320 C120,300 150,285 163,268 C210,238 235,222 262,198 C310,168 335,158 361,138 C408,110 432,98 460,84 C505,68 535,64 560,58 L560,141 C520,146 480,151 411,157 C350,162 330,173 262,179 C228,182 205,184 163,200 C138,214 108,252 64,320 Z" fill="#004AAD" fill-opacity="0.08"/>
          <path d="M64,320 C120,300 150,285 163,268 C210,238 235,222 262,198 C310,168 335,158 361,138 C408,110 432,98 460,84 C505,68 535,64 560,58" fill="none" stroke="#5B9BD5" stroke-width="4" stroke-linecap="round"/>
          <path d="M64,320 C108,252 138,214 163,200 C205,184 228,182 262,179 C330,173 350,162 411,157 C480,151 520,146 560,141" fill="none" stroke="#004AAD" stroke-width="4" stroke-linecap="round"/>
          <circle cx="560" cy="58" r="6" fill="#5B9BD5"/>
          <circle cx="560" cy="141" r="6" fill="#004AAD"/>
          <text x="576" y="51" font-family="Hanken Grotesk, sans-serif" font-size="16.5" font-weight="700" fill="#5B9BD5">Cost without</text>
          <text x="576" y="71" font-family="Hanken Grotesk, sans-serif" font-size="16.5" font-weight="700" fill="#5B9BD5">design</text>
          <text x="576" y="134" font-family="Hanken Grotesk, sans-serif" font-size="16.5" font-weight="700" fill="#004AAD">Cost with</text>
          <text x="576" y="154" font-family="Hanken Grotesk, sans-serif" font-size="16.5" font-weight="700" fill="#004AAD">design</text>
          <g stroke-linecap="round">
            <line x1="560" y1="66" x2="560" y2="133" stroke="#159A55" stroke-width="2.4"/>
            <polygon points="560,64 555,73 565,73" fill="#159A55"/>
            <polygon points="560,135 555,126 565,126" fill="#159A55"/>
          </g>
          <text x="551" y="106" text-anchor="end" font-family="Hanken Grotesk, sans-serif" font-size="15.5" font-weight="700" fill="#159A55">Savings</text>
          <g font-family="IBM Plex Mono, monospace" font-size="14" fill="#0F1B2C" text-anchor="middle">
            <text x="64" y="342">0</text><text x="155" y="342">5</text><text x="246" y="342">10</text>
            <text x="336" y="342">15</text><text x="427" y="342">20</text><text x="518" y="342">25</text><text x="560" y="342">30</text>
          </g>
          <text x="628" y="325" font-family="IBM Plex Mono, monospace" font-size="14" fill="#0F1B2C">Years</text>
          <text x="22" y="184" font-family="IBM Plex Mono, monospace" font-size="12.5" letter-spacing="1.5" fill="#0F1B2C" transform="rotate(-90 22 184)" text-anchor="middle">PROJECT COST</text>
          <rect x="64" y="356" width="99" height="24" rx="5" fill="#D5E1F2"/>
          <rect x="167" y="356" width="445" height="24" rx="5" fill="#E8EEF7"/>
          <text x="113" y="372" font-family="IBM Plex Mono, monospace" font-size="12.5" letter-spacing="1" fill="#004AAD" text-anchor="middle">DESIGN</text>
          <text x="389" y="372" font-family="IBM Plex Mono, monospace" font-size="12.5" letter-spacing="1" fill="#0F1B2C" text-anchor="middle">OPERATION</text>
        </svg>
        <figcaption>Design early. Lower life-cycle costs.</figcaption>
      </figure>

    <h3 class="m-mtd-subhead">Medical Technology Design as an integral process</h3>
    <div class="m-mtd-enable">
      <span class="m-mtd-enable-cap">What our Medical Technology Design enables</span>
      <div class="m-mtd-enable-items">
        <span>Fewer changes</span>
        <span>Cost certainty</span>
        <span>Schedule certainty</span>
        <span>Efficient collaboration</span>
        <span>Optimised operations</span>
      </div>
    </div>
    <figure class="m-mtd-figure">
      <img src="/assets/brands/integrated-design-model-en.png" alt="Integrated design model – BIM as the central coordination hub between architecture, medical technology, building services and operational organisation, shaped by budget, hygiene requirements, regulatory requirements and user needs." loading="lazy">
    </figure>
  </div>
</section>

<section class="m-section" id="bim">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">BIM</span>
      <h2 class="m-bigH">BIM-based design and standardised processes<span class="end-dot">.</span></h2>
      <div class="sub">Model-based working, in-house databases and repeatable results – the backbone of our Medical Technology Design.</div>
    </div>
    <div class="m-bim-grid">
      <figure class="m-bim-figure">
        <svg viewBox="-30 0 400 300" role="img" aria-label="BIM as the central coordination hub – connected with IFC, REVIT, BCF and data." xmlns="http://www.w3.org/2000/svg">
          <circle cx="160" cy="150" r="118" fill="none" stroke="#E8EEF7" stroke-width="1"/>
          <circle cx="160" cy="150" r="88" fill="none" stroke="#E8EEF7" stroke-width="1"/>
          <circle cx="160" cy="150" r="58" fill="none" stroke="#E8EEF7" stroke-width="1"/>
          <g stroke="#9DBCE3" stroke-width="1.5">
            <line x1="160" y1="150" x2="160" y2="40"/>
            <line x1="160" y1="150" x2="270" y2="150"/>
            <line x1="160" y1="150" x2="160" y2="260"/>
            <line x1="160" y1="150" x2="50" y2="150"/>
          </g>
          <circle cx="160" cy="150" r="50" fill="#004AAD"/>
          <text x="160" y="147" font-family="Hanken Grotesk, sans-serif" font-size="23" font-weight="700" fill="#fff" text-anchor="middle">BIM</text>
          <text x="160" y="167" font-family="Hanken Grotesk, sans-serif" font-size="11" font-weight="500" fill="#fff" text-anchor="middle">Coordination</text>
          <g fill="#fff" stroke="#004AAD" stroke-width="2">
            <circle cx="160" cy="40" r="17"/><circle cx="270" cy="150" r="17"/>
            <circle cx="160" cy="260" r="17"/><circle cx="50" cy="150" r="17"/>
          </g>
          <g fill="#004AAD" stroke="none">
            <circle cx="160" cy="40" r="3.2"/><circle cx="270" cy="150" r="3.2"/>
            <circle cx="160" cy="260" r="3.2"/><circle cx="50" cy="150" r="3.2"/>
          </g>
          <g font-family="Hanken Grotesk, sans-serif" font-size="14.5" font-weight="700" fill="#0F1B2C">
            <text x="160" y="20" text-anchor="middle">IFC</text>
            <text x="294" y="155" text-anchor="start">REVIT</text>
            <text x="160" y="297" text-anchor="middle">BCF</text>
            <text x="26" y="155" text-anchor="end">Data</text>
          </g>
        </svg>
      </figure>
      <div class="m-bim-points">
        <div class="m-bim-card">
          <span class="m-bim-cap">01 · Tool</span>
          <h3>Model-based approach</h3>
          <ul>
            <li>Autodesk Revit as standard tool</li>
            <li>Model-based design across all project phases</li>
            <li>Integration into architecture and building-services models</li>
          </ul>
        </div>
        <div class="m-bim-card">
          <span class="m-bim-cap">02 · Data</span>
          <h3>In-house databases</h3>
          <ul>
            <li>Equipment and connection database</li>
            <li>BIM family library</li>
          </ul>
        </div>
        <div class="m-bim-card">
          <span class="m-bim-cap">03 · Process</span>
          <h3>Standardised results</h3>
          <ul>
            <li>Structured room books and functional programmes</li>
            <li>Reviewed tender specifications</li>
            <li>Knowledge base from ongoing project work</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<!--PARTNER-->

<section class="m-cta-banner" style="background-image:url(/assets/cta-banner.jpg)">
  <div class="m-shell">
    <div class="m-cta-banner-copy">
      <div class="line"></div>
      <h2>Work with us<span class="end-dot">.</span></h2>
      <a class="m-cta-link" href="/en/kontakt.html">Get in touch</a>
    </div>
  </div>
</section>'''

def _tr(html, pairs, label=""):
    for a, b in pairs:
        if a not in html:
            print("  WARN [%s] Schlüssel nicht gefunden: %r" % (label, a[:60]))
        html = html.replace(a, b)
    return html

# Polnische Übersetzung der Startseite (Phrasen -> Polnisch)
_PL_MAP = [
    ("Engineering for medical technology", "Inżynieria techniki medycznej"),
    ("We design, supply and support medical solutions to the highest quality standards.",
     "Projektujemy, dostarczamy i wspieramy rozwiązania medyczne o najwyższych standardach jakości."),
    ("Your partner across the entire life cycle of medical technology",
     "Twój partner na każdym etapie cyklu życia techniki medycznej"),
    ("Shaping progress together", "Wspólnie kształtujemy postęp"),
    ("With our many years of experience in medical technology, we offer a comprehensive range of services tailored individually to your requirements. Whether initial concepts and feasibility studies, strategic procurement or the detailed design of your clinic – we support you competently and reliably in every project phase.",
     "Dzięki wieloletniemu doświadczeniu w technice medycznej oferujemy kompleksowy zakres usług, dopasowany indywidualnie do Państwa wymagań. Od pierwszych koncepcji i studiów wykonalności, przez strategiczne zaopatrzenie, po szczegółowe projektowanie Państwa kliniki – wspieramy Państwa kompetentnie i niezawodnie na każdym etapie projektu."),
    ('<h3 class="m-svc2-title">Medical Technology Design<span class="end-dot">',
     '<h3 class="m-svc2-title">Projektowanie techniki medycznej<span class="end-dot">'),
    ("From idea to implementation – we deliver your medical technology projects. With clear structures and efficient project control we ensure on-time delivery, cost certainty and the highest quality.",
     "Od pomysłu do realizacji – realizujemy Państwa projekty z zakresu techniki medycznej. Dzięki przejrzystym strukturom i sprawnemu zarządzaniu projektami zapewniamy terminowość, pewność kosztów i najwyższą jakość."),
    ('<h3 class="m-svc2-title">Consulting<span class="end-dot">',
     '<h3 class="m-svc2-title">Doradztwo<span class="end-dot">'),
    ("Strategies with substance – consulting backed by many years of experience in medical technology. Tailored solutions that optimise processes, reduce costs and deliver lasting results.",
     "Strategie z treścią – doradztwo oparte na wieloletnim doświadczeniu w technice medycznej. Rozwiązania szyte na miarę, które optymalizują procesy, obniżają koszty i przynoszą trwałe rezultaty."),
    ('<h3 class="m-svc2-title">Procurement<span class="end-dot">',
     '<h3 class="m-svc2-title">Zaopatrzenie<span class="end-dot">'),
    ("Quality that lasts. Solutions that pay off. Durable, low-maintenance medical products and individually tailored solutions – with personal advice and trusting, partnership-based collaboration.",
     "Jakość, która trwa. Rozwiązania, które się opłacają. Trwałe, wymagające niewielkiej konserwacji wyroby medyczne i indywidualnie dopasowane rozwiązania – z osobistym doradztwem i opartą na zaufaniu, partnerską współpracą."),
    ('<h3 class="m-svc2-title">Inspection<span class="end-dot">',
     '<h3 class="m-svc2-title">Kontrola techniczna<span class="end-dot">'),
    ("Reliable technical service – maximum safety. Flawless equipment, legally compliant inspections, minimal downtime.",
     "Niezawodny serwis techniczny – maksymalne bezpieczeństwo. Sprawny sprzęt, zgodne z prawem przeglądy, minimalne przestoje."),
    ("What does medical technology really cost", "Ile naprawdę kosztuje technika medyczna"),
    ("The purchase price is only the tip of the iceberg. Over the entire life cycle, far higher costs arise – in operation, maintenance, consumables and staff. We know these total costs in detail and factor them into every decision from the outset.",
     "Cena zakupu to tylko wierzchołek góry lodowej. W całym cyklu życia powstają znacznie wyższe koszty – w eksploatacji, konserwacji, materiałach zużywalnych i personelu. Znamy te całkowite koszty w szczegółach i uwzględniamy je w każdej decyzji od samego początku."),
    ("Design early · Reduce total cost · Preserve value long-term",
     "Wczesne projektowanie · Niższe koszty całkowite · Trwałe utrzymanie wartości"),
    ("Iceberg model: above the waterline the visible acquisition cost, below it the hidden costs such as transport, installation, commissioning, operating costs, staff, consumables, maintenance, training and disposal.",
     "Model góry lodowej: nad linią wody widoczny koszt zakupu, poniżej ukryte koszty, takie jak transport, instalacja, uruchomienie, koszty eksploatacji, personel, materiały zużywalne, konserwacja, szkolenia i utylizacja."),
    (">WATERLINE</text>", ">LINIA WODY</text>"),
    (">THE TIP</text>", ">WIERZCHOŁEK</text>"),
    (">Acquisition cost</text>", ">Koszt zakupu</text>"),
    (">Installation</text>", ">Instalacja</text>"),
    (">Commissioning</text>", ">Uruchomienie</text>"),
    (">Operating costs</text>", ">Koszty eksploatacji</text>"),
    (">Staff costs</text>", ">Koszty personelu</text>"),
    (">Consumables</text>", ">Materiały zużywalne</text>"),
    (">Maintenance</text>", ">Konserwacja</text>"),
    (">Training</text>", ">Szkolenia</text>"),
    (">Disposal</text>", ">Utylizacja</text>"),
    (">VISIBLE</text>", ">WIDOCZNE</text>"),
    (">what the price</text>", ">co pokazuje</text>"),
    (">shows</text>", ">cena</text>"),
    (">HIDDEN</text>", ">UKRYTE</text>"),
    (">what the device</text>", ">ile urządzenie</text>"),
    (">really costs</text>", ">naprawdę kosztuje</text>"),
    ("<figcaption>The purchase price is only the tip of the iceberg.</figcaption>",
     "<figcaption>Cena zakupu to tylko wierzchołek góry lodowej.</figcaption>"),
    ("</em>Acquisition</span>", "</em>Zakup</span>"),
    ("</em>Operation over the life cycle</span>", "</em>Eksploatacja w całym cyklu życia</span>"),
    ("The purchase price typically accounts for only about a fifth of the total cost – most of it arises in ongoing operation: maintenance, consumables, energy and staff.",
     "Cena zakupu stanowi zwykle tylko około jednej piątej kosztów całkowitych – większość powstaje w trakcie bieżącej eksploatacji: konserwacja, materiały zużywalne, energia i personel."),
    ('<span class="m-tag">Medical Technology Design</span>',
     '<span class="m-tag">Projektowanie techniki medycznej</span>'),
    ("Early Medical Technology Design that pays off across the entire life cycle",
     "Wczesne projektowanie techniki medycznej, które opłaca się przez cały cykl życia"),
    ("We bring medical technology into the design from the very first concept phase – this reduces costs, creates schedule and cost certainty and anchors the requirements of later operation right from the start.",
     "Uwzględniamy technikę medyczną w projektowaniu już od pierwszej fazy koncepcyjnej – to obniża koszty, zapewnia pewność terminów i kosztów oraz od początku uwzględnia wymagania późniejszej eksploatacji."),
    ("Early integration</span>", "Wczesna integracja</span>"),
    ("Requirements for function, operation, infrastructure and cost efficiency are considered from the outset.",
     "Wymagania dotyczące funkcji, eksploatacji, infrastruktury i efektywności kosztowej są uwzględniane od samego początku."),
    ("Without Medical Technology Design</span>", "Bez projektowania techniki medycznej</span>"),
    ("Higher costs and increased coordination effort in later project phases.",
     "Wyższe koszty i większy nakład koordynacji w późniejszych fazach projektu."),
    (">Our task</span>", ">Nasze zadanie</span>"),
    ("Creating reliable foundations in the early phases",
     "Tworzenie solidnych podstaw we wczesnych fazach"),
    ("Cost efficiency through early design</div>", "Efektywność kosztowa dzięki wczesnemu projektowaniu</div>"),
    ("Diagram: project cost over 30 years – significantly lower life-cycle cost with early design.",
     "Wykres: koszt projektu w ciągu 30 lat – znacznie niższe koszty cyklu życia dzięki wczesnemu projektowaniu."),
    (">Cost without</text>", ">Koszt bez</text>"),
    (">Cost with</text>", ">Koszt z</text>"),
    (">design</text>", ">projektowania</text>"),
    (">Years</text>", ">Lata</text>"),
    (">PROJECT COST</text>", ">KOSZT PROJEKTU</text>"),
    (">DESIGN</text>", ">PROJEKTOWANIE</text>"),
    (">OPERATION</text>", ">EKSPLOATACJA</text>"),
    ("<figcaption>Design early. Lower life-cycle costs.</figcaption>",
     "<figcaption>Projektuj wcześnie. Niższe koszty cyklu życia.</figcaption>"),
    ("Medical Technology Design as an integral process</h3>",
     "Projektowanie techniki medycznej jako proces zintegrowany</h3>"),
    ("What our Medical Technology Design enables</span>",
     "Co umożliwia nasze projektowanie techniki medycznej</span>"),
    ("<span>Fewer changes</span>", "<span>Mniej zmian</span>"),
    ("<span>Cost certainty</span>", "<span>Pewne koszty</span>"),
    ("<span>Schedule certainty</span>", "<span>Pewne terminy</span>"),
    ("<span>Efficient collaboration</span>", "<span>Sprawna współpraca</span>"),
    ("<span>Optimised operations</span>", "<span>Optymalne procesy eksploatacyjne</span>"),
    (">Savings</text>", ">Oszczędność</text>"),
    ("Integrated design model – BIM as the central coordination hub between architecture, medical technology, building services and operational organisation, shaped by budget, hygiene requirements, regulatory requirements and user needs.",
     "Zintegrowany model projektowania – BIM jako centralny węzeł koordynacji między architekturą, techniką medyczną, instalacjami budynku i organizacją eksploatacji, kształtowany przez budżet, wymagania higieniczne, wymagania prawne i potrzeby użytkowników."),
    ("BIM-based design and standardised processes", "Projektowanie oparte na BIM i standaryzowane procesy"),
    ("Model-based working, in-house databases and repeatable results – the backbone of our Medical Technology Design.",
     "Praca oparta na modelu, własne bazy danych i powtarzalne wyniki – fundament naszego projektowania techniki medycznej."),
    ("BIM as the central coordination hub – connected with IFC, REVIT, BCF and data.",
     "BIM jako centralny węzeł koordynacji – połączony z IFC, REVIT, BCF i danymi."),
    (">Coordination</text>", ">Koordynacja</text>"),
    (">Data</text>", ">Dane</text>"),
    ("<h3>Model-based approach</h3>", "<h3>Podejście oparte na modelu</h3>"),
    ("<li>Autodesk Revit as standard tool</li>", "<li>Autodesk Revit jako standardowe narzędzie</li>"),
    ("<li>Model-based design across all project phases</li>", "<li>Projektowanie oparte na modelu we wszystkich fazach</li>"),
    ("<li>Integration into architecture and building-services models</li>", "<li>Integracja z modelami architektury i instalacji</li>"),
    ("<h3>In-house databases</h3>", "<h3>Własne bazy danych</h3>"),
    ("<li>Equipment and connection database</li>", "<li>Baza urządzeń i przyłączy</li>"),
    ("<li>BIM family library</li>", "<li>Biblioteka rodzin BIM</li>"),
    ("<h3>Standardised results</h3>", "<h3>Standaryzowane wyniki</h3>"),
    ("<li>Structured room books and functional programmes</li>", "<li>Ustrukturyzowane książki pomieszczeń i programy funkcjonalne</li>"),
    ("<li>Reviewed tender specifications</li>", "<li>Sprawdzone specyfikacje przetargowe</li>"),
    ("<li>Knowledge base from ongoing project work</li>", "<li>Baza wiedzy z bieżącej pracy projektowej</li>"),
    ('<h2>Work with us<span class="end-dot">', '<h2>Współpracuj z nami<span class="end-dot">'),
    (">Get in touch</a>", ">Skontaktuj się</a>"),
    ('href="/en/leistungen.html"', 'href="/pl/leistungen.html"'),
    ('href="/en/kontakt.html"', 'href="/pl/kontakt.html"'),
]

# Rumänische Übersetzung der Startseite (Phrasen -> Rumänisch)
_RO_MAP = [
    ("Engineering for medical technology", "Inginerie pentru tehnologia medicală"),
    ("We design, supply and support medical solutions to the highest quality standards.",
     "Proiectăm, furnizăm și susținem soluții medicale la cele mai înalte standarde de calitate."),
    ("Your partner across the entire life cycle of medical technology",
     "Partenerul dumneavoastră pe întregul ciclu de viață al tehnologiei medicale"),
    ("Shaping progress together", "Construim progresul împreună"),
    ("With our many years of experience in medical technology, we offer a comprehensive range of services tailored individually to your requirements. Whether initial concepts and feasibility studies, strategic procurement or the detailed design of your clinic – we support you competently and reliably in every project phase.",
     "Cu experiența noastră de mulți ani în tehnologia medicală, oferim o gamă completă de servicii, adaptate individual cerințelor dumneavoastră. Fie că este vorba de primele concepte și studii de fezabilitate, de achiziția strategică sau de proiectarea detaliată a clinicii dumneavoastră – vă sprijinim competent și de încredere în fiecare fază a proiectului."),
    ('<h3 class="m-svc2-title">Medical Technology Design<span class="end-dot">',
     '<h3 class="m-svc2-title">Proiectarea tehnologiei medicale<span class="end-dot">'),
    ("From idea to implementation – we deliver your medical technology projects. With clear structures and efficient project control we ensure on-time delivery, cost certainty and the highest quality.",
     "De la idee la implementare – realizăm proiectele dumneavoastră de tehnologie medicală. Prin structuri clare și un control eficient al proiectului asigurăm respectarea termenelor, certitudinea costurilor și cea mai înaltă calitate."),
    ('<h3 class="m-svc2-title">Consulting<span class="end-dot">',
     '<h3 class="m-svc2-title">Consultanță<span class="end-dot">'),
    ("Strategies with substance – consulting backed by many years of experience in medical technology. Tailored solutions that optimise processes, reduce costs and deliver lasting results.",
     "Strategii cu substanță – consultanță susținută de mulți ani de experiență în tehnologia medicală. Soluții personalizate care optimizează procesele, reduc costurile și oferă rezultate durabile."),
    ('<h3 class="m-svc2-title">Procurement<span class="end-dot">',
     '<h3 class="m-svc2-title">Achiziții<span class="end-dot">'),
    ("Quality that lasts. Solutions that pay off. Durable, low-maintenance medical products and individually tailored solutions – with personal advice and trusting, partnership-based collaboration.",
     "Calitate care durează. Soluții care merită. Produse medicale durabile, cu întreținere redusă, și soluții adaptate individual – cu consiliere personală și o colaborare de încredere, de tip parteneriat."),
    ('<h3 class="m-svc2-title">Inspection<span class="end-dot">',
     '<h3 class="m-svc2-title">Verificare tehnică<span class="end-dot">'),
    ("Reliable technical service – maximum safety. Flawless equipment, legally compliant inspections, minimal downtime.",
     "Serviciu tehnic de încredere – siguranță maximă. Echipamente impecabile, verificări conforme legal, timpi de nefuncționare minimi."),
    ("What does medical technology really cost", "Cât costă cu adevărat tehnologia medicală"),
    ("The purchase price is only the tip of the iceberg. Over the entire life cycle, far higher costs arise – in operation, maintenance, consumables and staff. We know these total costs in detail and factor them into every decision from the outset.",
     "Prețul de achiziție este doar vârful aisbergului. Pe întregul ciclu de viață apar costuri mult mai mari – în exploatare, întreținere, consumabile și personal. Cunoaștem aceste costuri totale în detaliu și le luăm în calcul în fiecare decizie, încă de la început."),
    ("Design early · Reduce total cost · Preserve value long-term",
     "Proiectați din timp · Reduceți costul total · Păstrați valoarea pe termen lung"),
    ("Iceberg model: above the waterline the visible acquisition cost, below it the hidden costs such as transport, installation, commissioning, operating costs, staff, consumables, maintenance, training and disposal.",
     "Modelul aisbergului: deasupra liniei apei costul de achiziție vizibil, dedesubt costurile ascunse precum transport, instalare, punere în funcțiune, costuri de exploatare, personal, consumabile, întreținere, instruire și eliminare."),
    (">WATERLINE</text>", ">LINIA APEI</text>"),
    (">THE TIP</text>", ">VÂRFUL</text>"),
    (">Acquisition cost</text>", ">Cost de achiziție</text>"),
    (">Installation</text>", ">Instalare</text>"),
    (">Commissioning</text>", ">Punere în funcțiune</text>"),
    (">Operating costs</text>", ">Costuri de exploatare</text>"),
    (">Staff costs</text>", ">Costuri de personal</text>"),
    (">Consumables</text>", ">Consumabile</text>"),
    (">Maintenance</text>", ">Întreținere</text>"),
    (">Training</text>", ">Instruire</text>"),
    (">Disposal</text>", ">Eliminare</text>"),
    (">VISIBLE</text>", ">VIZIBIL</text>"),
    (">what the price</text>", ">ce arată</text>"),
    (">shows</text>", ">prețul</text>"),
    (">HIDDEN</text>", ">ASCUNS</text>"),
    (">what the device</text>", ">cât costă</text>"),
    (">really costs</text>", ">echipamentul</text>"),
    ("<figcaption>The purchase price is only the tip of the iceberg.</figcaption>",
     "<figcaption>Prețul de achiziție este doar vârful aisbergului.</figcaption>"),
    ("</em>Acquisition</span>", "</em>Achiziție</span>"),
    ("</em>Operation over the life cycle</span>", "</em>Exploatare pe ciclul de viață</span>"),
    ("The purchase price typically accounts for only about a fifth of the total cost – most of it arises in ongoing operation: maintenance, consumables, energy and staff.",
     "Prețul de achiziție reprezintă de obicei doar aproximativ o cincime din costul total – cea mai mare parte apare în exploatarea curentă: întreținere, consumabile, energie și personal."),
    ('<span class="m-tag">Medical Technology Design</span>',
     '<span class="m-tag">Proiectarea tehnologiei medicale</span>'),
    ("Early Medical Technology Design that pays off across the entire life cycle",
     "Proiectare timpurie a tehnologiei medicale, rentabilă pe întregul ciclu de viață"),
    ("We bring medical technology into the design from the very first concept phase – this reduces costs, creates schedule and cost certainty and anchors the requirements of later operation right from the start.",
     "Integrăm tehnologia medicală în proiectare încă din prima fază de concept – acest lucru reduce costurile, oferă certitudinea termenelor și a costurilor și include de la început cerințele exploatării ulterioare."),
    ("Early integration</span>", "Integrare timpurie</span>"),
    ("Requirements for function, operation, infrastructure and cost efficiency are considered from the outset.",
     "Cerințele privind funcția, exploatarea, infrastructura și eficiența costurilor sunt luate în considerare de la început."),
    ("Without Medical Technology Design</span>", "Fără proiectarea tehnologiei medicale</span>"),
    ("Higher costs and increased coordination effort in later project phases.",
     "Costuri mai mari și efort de coordonare crescut în fazele ulterioare ale proiectului."),
    (">Our task</span>", ">Sarcina noastră</span>"),
    ("Creating reliable foundations in the early phases",
     "Crearea unor baze solide în fazele timpurii"),
    ("Cost efficiency through early design</div>", "Eficiența costurilor prin proiectare timpurie</div>"),
    ("Diagram: project cost over 30 years – significantly lower life-cycle cost with early design.",
     "Diagramă: costul proiectului pe 30 de ani – costuri ale ciclului de viață semnificativ mai mici prin proiectare timpurie."),
    (">Cost without</text>", ">Cost fără</text>"),
    (">Cost with</text>", ">Cost cu</text>"),
    (">design</text>", ">proiectare</text>"),
    (">Years</text>", ">Ani</text>"),
    (">PROJECT COST</text>", ">COSTUL PROIECTULUI</text>"),
    (">DESIGN</text>", ">PROIECTARE</text>"),
    (">OPERATION</text>", ">EXPLOATARE</text>"),
    ("<figcaption>Design early. Lower life-cycle costs.</figcaption>",
     "<figcaption>Proiectați din timp. Costuri mai mici pe ciclul de viață.</figcaption>"),
    ("Medical Technology Design as an integral process</h3>",
     "Proiectarea tehnologiei medicale ca proces integrat</h3>"),
    ("What our Medical Technology Design enables</span>",
     "Ce permite proiectarea noastră a tehnologiei medicale</span>"),
    ("<span>Fewer changes</span>", "<span>Mai puține modificări</span>"),
    ("<span>Cost certainty</span>", "<span>Costuri sigure</span>"),
    ("<span>Schedule certainty</span>", "<span>Termene fiabile</span>"),
    ("<span>Efficient collaboration</span>", "<span>Colaborare eficientă</span>"),
    ("<span>Optimised operations</span>", "<span>Fluxuri de operare optime</span>"),
    (">Savings</text>", ">Economii</text>"),
    ("Integrated design model – BIM as the central coordination hub between architecture, medical technology, building services and operational organisation, shaped by budget, hygiene requirements, regulatory requirements and user needs.",
     "Model integrat de proiectare – BIM ca nod central de coordonare între arhitectură, tehnologia medicală, instalațiile clădirii și organizarea exploatării, influențat de buget, cerințe de igienă, cerințe legale și nevoile utilizatorilor."),
    ("BIM-based design and standardised processes", "Proiectare bazată pe BIM și procese standardizate"),
    ("Model-based working, in-house databases and repeatable results – the backbone of our Medical Technology Design.",
     "Lucrul bazat pe model, baze de date proprii și rezultate reproductibile – coloana vertebrală a proiectării noastre a tehnologiei medicale."),
    ("BIM as the central coordination hub – connected with IFC, REVIT, BCF and data.",
     "BIM ca nod central de coordonare – conectat cu IFC, REVIT, BCF și date."),
    (">Coordination</text>", ">Coordonare</text>"),
    (">Data</text>", ">Date</text>"),
    ("<h3>Model-based approach</h3>", "<h3>Abordare bazată pe model</h3>"),
    ("<li>Autodesk Revit as standard tool</li>", "<li>Autodesk Revit ca instrument standard</li>"),
    ("<li>Model-based design across all project phases</li>", "<li>Proiectare bazată pe model în toate fazele proiectului</li>"),
    ("<li>Integration into architecture and building-services models</li>", "<li>Integrare în modelele de arhitectură și instalații</li>"),
    ("<h3>In-house databases</h3>", "<h3>Baze de date proprii</h3>"),
    ("<li>Equipment and connection database</li>", "<li>Bază de date de echipamente și racorduri</li>"),
    ("<li>BIM family library</li>", "<li>Bibliotecă de familii BIM</li>"),
    ("<h3>Standardised results</h3>", "<h3>Rezultate standardizate</h3>"),
    ("<li>Structured room books and functional programmes</li>", "<li>Cărți de încăperi structurate și programe funcționale</li>"),
    ("<li>Reviewed tender specifications</li>", "<li>Specificații de licitație verificate</li>"),
    ("<li>Knowledge base from ongoing project work</li>", "<li>Bază de cunoștințe din activitatea de proiect curentă</li>"),
    ('<h2>Work with us<span class="end-dot">', '<h2>Lucrați cu noi<span class="end-dot">'),
    (">Get in touch</a>", ">Contactați-ne</a>"),
    ('href="/en/leistungen.html"', 'href="/ro/leistungen.html"'),
    ('href="/en/kontakt.html"', 'href="/ro/kontakt.html"'),
]

BODY_INDEX_PL = _tr(BODY_INDEX_EN, _PL_MAP, "PL")
BODY_INDEX_RO = _tr(BODY_INDEX_EN, _RO_MAP, "RO")

# ---- Integriertes Planungsmodell / Integrated Design Model als Inline-SVG ----
# Sprachneutral aufgebaute Grafik (verschwimmt mit dem mist-blauen Abschnitt),
# Beschriftungen je Sprache. Ersetzt das frühere PNG in allen Sprachen.
import math as _math
_MDL_C = (750, 512); _MDL_Ro, _MDL_Ri, _MDL_Rc, _MDL_Rl = 286, 172, 118, 229
_MDL_BIM_FS = 74; _MDL_DOT_GAP = 18
_MDL_SEGS = {"arch": (184, 266, "#004AAD"), "med": (274, 356, "#2A6ABC"),
             "geb": (4, 86, "#4F8BCB"), "betr": (94, 176, "#79A9D6")}
# Konnektoren: Label mit Unterlinie, Knick zu einem Punkt mit Abstand zum Segment
_MDL_CORN = {"budget": dict(side="L", vpos="T", dot_a=246),
             "hyg": dict(side="R", vpos="T", dot_a=294),
             "user": dict(side="L", vpos="B", dot_a=114),
             "reg": dict(side="R", vpos="B", dot_a=66)}
_MDL_UY_T, _MDL_UY_B = 190, 834
_MDL_UXL_OUT, _MDL_UXL_IN = 80, 430
_MDL_UXR_OUT, _MDL_UXR_IN = 1420, 1070
_MDL_TXT = {
 "de": dict(title="INTEGRIERTES PLANUNGSMODELL", arch="ARCHITEKTUR", med="MEDIZINTECHNIK",
            geb="GEBÄUDETECHNIK", betr="BETRIEBSORGANISATION",
            budget="BUDGET", hyg="HYGIENEANFORDERUNGEN", user="NUTZERBEDÜRFNISSE", reg="BEHÖRDLICHE ANFORDERUNGEN",
            cap1="BIM bildet die zentrale Koordinationsdrehscheibe im Kern der",
            cap2="Zusammenarbeit. Externe Faktoren prägen den Planungsprozess."),
 "en": dict(title="INTEGRATED DESIGN MODEL", arch="ARCHITECTURE", med="MEDICAL TECHNOLOGY",
            geb="BUILDING SERVICES", betr="OPERATIONAL ORG.",
            budget="BUDGET", hyg="HYGIENE REQUIREMENTS", user="USER NEEDS", reg="REGULATORY REQUIREMENTS",
            cap1="BIM serves as the central coordination hub at the core of",
            cap2="collaboration. External factors shape the design process."),
 "pl": dict(title="ZINTEGROWANY MODEL PROJEKTOWY", arch="ARCHITEKTURA", med="TECHNIKA MEDYCZNA",
            geb="INSTALACJE BUDYNKU", betr="ORGANIZACJA OPERACYJNA",
            budget="BUDŻET", hyg="WYMAGANIA HIGIENICZNE", user="POTRZEBY UŻYTKOWNIKÓW", reg="WYMOGI URZĘDOWE",
            cap1="BIM stanowi centralny węzeł koordynacji w rdzeniu",
            cap2="współpracy. Czynniki zewnętrzne kształtują proces projektowania."),
 "ro": dict(title="MODEL DE PROIECTARE INTEGRAT", arch="ARHITECTURĂ", med="TEHNOLOGIE MEDICALĂ",
            geb="INSTALAȚIILE CLĂDIRII", betr="ORG. OPERAȚIONALĂ",
            budget="BUGET", hyg="CERINȚE DE IGIENĂ", user="NEVOILE UTILIZATORILOR", reg="CERINȚE DE REGLEMENTARE",
            cap1="BIM constituie platforma centrală de coordonare în centrul",
            cap2="colaborării. Factorii externi modelează procesul de proiectare."),
}
def _mdl_pt(a_deg, r):
    a = _math.radians(a_deg)
    return (_MDL_C[0] + r * _math.cos(a), _MDL_C[1] + r * _math.sin(a))
def _mdl_seg(a1, a2):
    P1 = _mdl_pt(a1, _MDL_Ro); P2 = _mdl_pt(a2, _MDL_Ro)
    P3 = _mdl_pt(a2, _MDL_Ri); P4 = _mdl_pt(a1, _MDL_Ri)
    return (f'M {P1[0]:.1f} {P1[1]:.1f} A {_MDL_Ro} {_MDL_Ro} 0 0 1 {P2[0]:.1f} {P2[1]:.1f} '
            f'L {P3[0]:.1f} {P3[1]:.1f} A {_MDL_Ri} {_MDL_Ri} 0 0 0 {P4[0]:.1f} {P4[1]:.1f} Z')
def _mdl_arc(a1, a2, r):
    P1 = _mdl_pt(a1, r); P2 = _mdl_pt(a2, r)
    return f'M {P1[0]:.1f} {P1[1]:.1f} A {r} {r} 0 0 1 {P2[0]:.1f} {P2[1]:.1f}'
def _design_model_svg(lang):
    t = _MDL_TXT[lang]; C = _MDL_C; o = []
    o.append(f'<svg class="m-mtd-svg" viewBox="0 0 1500 1016" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_html.escape(t["title"])}">')
    o.append('<defs>')
    for k, (a1, a2, _c) in _MDL_SEGS.items():
        o.append(f'<path id="tp-{lang}-{k}" fill="none" d="{_mdl_arc(a1, a2, _MDL_Rl)}"/>')
    o.append('</defs>')
    o.append(f'<text x="20" y="48" font-family="IBM Plex Mono, monospace" font-size="34" font-weight="600" letter-spacing="7" fill="#3D6BB0">{_html.escape(t["title"])}</text>')
    o.append('<line x1="20" y1="86" x2="1480" y2="86" stroke="#D5E1F2" stroke-width="1.5"/>')
    for k, (a1, a2, c) in _MDL_SEGS.items():
        o.append(f'<path d="{_mdl_seg(a1, a2)}" fill="{c}"/>')
    o.append(f'<circle cx="{C[0]}" cy="{C[1]}" r="{_MDL_Rc}" fill="#E8EEF7" stroke="#0F1B2C" stroke-width="2.5"/>')
    o.append(f'<text x="{C[0]}" y="{C[1]+26}" text-anchor="middle" font-family="Hanken Grotesk, sans-serif" font-size="{_MDL_BIM_FS}" font-weight="800" fill="#0F1B2C">BIM</text>')
    for k in ("arch", "med", "geb", "betr"):
        lbl = t[k]; fs = 26 if len(lbl) <= 14 else (23 if len(lbl) <= 19 else 20)
        o.append(f'<text font-family="Hanken Grotesk, sans-serif" font-size="{fs}" font-weight="700" letter-spacing="1" fill="#FFFFFF">'
                 f'<textPath href="#tp-{lang}-{k}" startOffset="50%" text-anchor="middle">{_html.escape(lbl)}</textPath></text>')
    for key, cfg in _MDL_CORN.items():
        uy = _MDL_UY_T if cfg["vpos"] == "T" else _MDL_UY_B
        if cfg["side"] == "L":
            uxo, uxi, tx, anc = _MDL_UXL_OUT, _MDL_UXL_IN, _MDL_UXL_OUT, "start"
        else:
            uxo, uxi, tx, anc = _MDL_UXR_OUT, _MDL_UXR_IN, _MDL_UXR_OUT, "end"
        d = _mdl_pt(cfg["dot_a"], _MDL_Ro + _MDL_DOT_GAP)
        o.append(f'<polyline points="{uxo},{uy} {uxi},{uy} {d[0]:.1f},{d[1]:.1f}" fill="none" stroke="#2E5C9E" stroke-width="2"/>')
        o.append(f'<circle cx="{d[0]:.1f}" cy="{d[1]:.1f}" r="6" fill="#2E5C9E"/>')
        o.append(f'<text x="{tx}" y="{uy-13}" text-anchor="{anc}" font-family="IBM Plex Mono, monospace" font-size="23" letter-spacing="2" fill="#454F5C">{_html.escape(t[key])}</text>')
    o.append(f'<text x="{C[0]}" y="945" text-anchor="middle" font-family="Hanken Grotesk, sans-serif" font-size="30" font-weight="700" fill="#0F1B2C">{_html.escape(t["cap1"])}</text>')
    o.append(f'<text x="{C[0]}" y="985" text-anchor="middle" font-family="Hanken Grotesk, sans-serif" font-size="30" font-weight="700" fill="#0F1B2C">{_html.escape(t["cap2"])}</text>')
    o.append('</svg>')
    return "\n".join(o)
def _inject_model(body, lang):
    return _re.sub(r'<img[^>]*integrated-design-model[^>]*>', lambda m: _design_model_svg(lang), body, count=1)

BODY_INDEX    = _inject_model(BODY_INDEX, "de")
BODY_INDEX_EN = _inject_model(BODY_INDEX_EN, "en")
BODY_INDEX_PL = _inject_model(BODY_INDEX_PL, "pl")
BODY_INDEX_RO = _inject_model(BODY_INDEX_RO, "ro")

BODY_INDEX    = _inject_partner(_inject_flyer(BODY_INDEX, "de"), "de")
BODY_INDEX_EN = _inject_partner(_inject_flyer(BODY_INDEX_EN, "en"), "en")
BODY_INDEX_PL = _inject_partner(_inject_flyer(BODY_INDEX_PL, "pl"), "pl")
BODY_INDEX_RO = _inject_partner(_inject_flyer(BODY_INDEX_RO, "ro"), "ro")

BODY_LEISTUNGEN_PL = _tr(BODY_LEISTUNGEN_EN, _LEIST_PL, "PL leistungen")
BODY_LEISTUNGEN_RO = _tr(BODY_LEISTUNGEN_EN, _LEIST_RO, "RO leistungen")

# ---- Management (EN + PL/RO) ----
BODY_MANAGEMENT_EN = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Management</span>
    <h1>Medical technology with responsibility, quality and vision<span class="end-dot">.</span></h1>
    <p class="lede">Our management brings more than 15 years of experience in medical technology that shapes our company. Quality, reliability and constant availability come first for us. We rely on partnership-based collaboration, personal support and fast, solution-oriented responses. By using the latest technologies, we ensure future-proof, high-quality solutions for our customers.</p>
  </div>
</section>

<section class="m-section">
  <div class="m-shell">
    <div class="m-solo">
      <img class="m-solo-photo" src="/assets/portrait-scherzer.jpg" alt="Georg Scherzer" loading="lazy">
      <div class="m-solo-body">
        <div class="m-member-name">Georg Scherzer</div>
        <div class="m-member-role">Founder · Medical engineer</div>
        <div class="m-member-contact"><span class="k">Contact</span><a href="mailto:g.scherzer@medeqon.com">g.scherzer@medeqon.com</a><span class="sep">·</span><a href="tel:+436705505612">+43 670 5505612</a></div>
        <div class="m-member-langs"><span class="k">Languages</span>German (native), English, French</div>
        <div class="m-member-quals">
          <span class="k">Experience &amp; qualifications</span>
          <ul class="ring-list">
            <li>More than 15 years of experience in medical technology</li>
            <li>Former head of the medical technology department at AKH Vienna and Krems University Hospital</li>
            <li>International project experience in crisis regions for the Red Cross</li>
            <li>Consulting work for the WHO</li>
            <li>Certified sworn and court-appointed expert (in training)</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>'''

_MGMT_PL = [
    ("Medical technology with responsibility, quality and vision", "Technika medyczna z odpowiedzialnością, jakością i wizją przyszłości"),
    ("Our management brings more than 15 years of experience in medical technology that shapes our company. Quality, reliability and constant availability come first for us. We rely on partnership-based collaboration, personal support and fast, solution-oriented responses. By using the latest technologies, we ensure future-proof, high-quality solutions for our customers.",
     "Nasze kierownictwo dysponuje ponad 15-letnim doświadczeniem w technice medycznej, które kształtuje naszą firmę. Jakość, niezawodność i stała dostępność są dla nas najważniejsze. Stawiamy na partnerską współpracę, osobistą opiekę oraz szybkie, zorientowane na rozwiązania reakcje. Dzięki zastosowaniu najnowocześniejszych technologii zapewniamy naszym klientom przyszłościowe rozwiązania o wysokiej jakości."),
    ("Founder · Medical engineer", "Założyciel · Inżynier techniki medycznej"),
    (">Contact</span>", ">Kontakt</span>"),
    (">Languages</span>German (native), English, French", ">Języki</span>niemiecki (ojczysty), angielski, francuski"),
    ("Experience &amp; qualifications", "Doświadczenie i kwalifikacje"),
    ("<li>More than 15 years of experience in medical technology</li>", "<li>Ponad 15 lat doświadczenia w technice medycznej</li>"),
    ("<li>Former head of the medical technology department at AKH Vienna and Krems University Hospital</li>", "<li>Były kierownik działu techniki medycznej w AKH Wiedeń oraz w Szpitalu Uniwersyteckim w Krems</li>"),
    ("<li>International project experience in crisis regions for the Red Cross</li>", "<li>Międzynarodowe doświadczenie projektowe w regionach kryzysowych dla Czerwonego Krzyża</li>"),
    ("<li>Consulting work for the WHO</li>", "<li>Działalność doradcza dla WHO</li>"),
    ("<li>Certified sworn and court-appointed expert (in training)</li>", "<li>Zaprzysiężony i sądowo certyfikowany rzeczoznawca (w trakcie szkolenia)</li>"),
]
_MGMT_RO = [
    ("Medical technology with responsibility, quality and vision", "Tehnologie medicală cu responsabilitate, calitate și viziune"),
    ("Our management brings more than 15 years of experience in medical technology that shapes our company. Quality, reliability and constant availability come first for us. We rely on partnership-based collaboration, personal support and fast, solution-oriented responses. By using the latest technologies, we ensure future-proof, high-quality solutions for our customers.",
     "Conducerea noastră are peste 15 ani de experiență în tehnologia medicală, experiență care ne definește compania. Calitatea, fiabilitatea și disponibilitatea permanentă sunt pentru noi pe primul loc. Ne bazăm pe o colaborare de tip parteneriat, pe asistență personală și pe reacții rapide, orientate spre soluții. Prin utilizarea celor mai noi tehnologii, asigurăm clienților noștri soluții de înaltă calitate, pregatite pentru viitor."),
    ("Founder · Medical engineer", "Fondator · Inginer de tehnologie medicală"),
    (">Contact</span>", ">Contact</span>"),
    (">Languages</span>German (native), English, French", ">Limbi</span>germană (nativ), engleză, franceză"),
    ("Experience &amp; qualifications", "Experiență și calificări"),
    ("<li>More than 15 years of experience in medical technology</li>", "<li>Peste 15 ani de experiență în tehnologia medicală</li>"),
    ("<li>Former head of the medical technology department at AKH Vienna and Krems University Hospital</li>", "<li>Fost șef al departamentului de tehnologie medicală la AKH Viena și la Spitalul Universitar Krems</li>"),
    ("<li>International project experience in crisis regions for the Red Cross</li>", "<li>Experiență internațională de proiect în zone de criză pentru Crucea Roșie</li>"),
    ("<li>Consulting work for the WHO</li>", "<li>Activitate de consultanță pentru OMS</li>"),
    ("<li>Certified sworn and court-appointed expert (in training)</li>", "<li>Expert autorizat, jurat și desemnat de instanță (în formare)</li>"),
]
BODY_MANAGEMENT_PL = _tr(BODY_MANAGEMENT_EN, _MGMT_PL, "MGMT-PL")
BODY_MANAGEMENT_RO = _tr(BODY_MANAGEMENT_EN, _MGMT_RO, "MGMT-RO")

# ---- Kontakt (EN + PL/RO). Formularfelder (name=) bleiben deutsch (Empfänger). ----
BODY_KONTAKT_EN = '''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">Contact</span>
    <h1>We're here for you<span class="end-dot">.</span></h1>
    <p class="lede">Whether a project enquiry, service, consulting or the procurement of medical products — get in touch. We find the right product and deliver reliably. Our team will get back to you quickly and personally.</p>
  </div>
</section>

<section class="m-section">
  <div class="m-shell">
    <div class="m-contactgrid">
      <div>
        <div class="m-secH" style="margin-bottom:28px">
          <span class="m-tag">Enquiry</span>
          <h2>Write to us<span class="end-dot">.</span></h2>
          <div class="sub">Fields marked * are required. Your enquiry goes straight to our team.</div>
        </div>
        <form class="m-form" id="kontaktForm" novalidate>
          <div class="m-field">
            <label for="k-name">Name *</label>
            <input class="m-input" id="k-name" name="Name" type="text" autocomplete="name" required>
          </div>
          <div class="m-form-row">
            <div class="m-field">
              <label for="k-mail">Email *</label>
              <input class="m-input" id="k-mail" name="E-Mail" type="email" autocomplete="email" required>
            </div>
            <div class="m-field">
              <label for="k-tel">Phone</label>
              <input class="m-input" id="k-tel" name="Telefon" type="tel" autocomplete="tel">
            </div>
          </div>
          <div class="m-field">
            <label for="k-org">Company</label>
            <input class="m-input" id="k-org" name="Unternehmen" type="text" autocomplete="organization">
          </div>
          <div class="m-field">
            <label for="k-topic">Subject</label>
            <select class="m-input" id="k-topic" name="Anliegen">
              <option>Project enquiry</option>
              <option>Consulting</option>
              <option>Procurement of medical products</option>
              <option>Service / inspection</option>
              <option>Other</option>
            </select>
          </div>
          <div class="m-field">
            <label for="k-msg">Message *</label>
            <textarea class="m-input" id="k-msg" name="Nachricht" required></textarea>
          </div>
          <input type="text" name="_honey" class="m-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <input type="hidden" name="_subject" value="Neue Anfrage über medeqon.com">
          <input type="hidden" name="_template" value="table">
          <div class="m-turnstile"><div class="cf-turnstile" data-sitekey="__TURNSTILE_SITEKEY__" data-theme="light" data-language="auto"></div></div>
          <button class="m-btn" type="submit" id="k-submit">Send enquiry</button>
          <div class="m-form-status" id="formStatus" role="status" aria-live="polite"></div>
          <noscript><p class="sub">Please enable JavaScript or write to us directly at office@medeqon.com.</p></noscript>
        </form>
        <p class="m-form-note">When you submit this contact form, we process your personal data (name, email, phone number and message) in order to respond to your enquiry. The legal basis is (pre-)contractual communication pursuant to Art. 6(1)(b) GDPR. You can find further information in our <a href="/en/datenschutz.html">privacy policy</a>.</p>
      </div>

      <aside class="m-caside">
        <div>
          <span class="k">Direct</span>
          <a href="mailto:office@medeqon.com">office@medeqon.com</a>
          <a href="tel:+4313580045">+43 1 3580045</a>
        </div>
        <div>
          <span class="k">Office</span>
          <p>Bergstraße 42/5/3<br>2102 Hagenbrunn · Austria<br>Mon – Fri · and by appointment</p>
        </div>
      </aside>
    </div>
  </div>
</section>

<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<script>
(function(){
  var f=document.getElementById("kontaktForm");
  if(!f) return;
  var s=document.getElementById("formStatus");
  var btn=document.getElementById("k-submit");
  var ENDPOINT="https://formsubmit.co/ajax/office@medeqon.com";
  var t0=Date.now();
  f.addEventListener("submit", function(e){
    e.preventDefault();
    if(f._honey.value){ return; }
    if(Date.now()-t0 < 1500){ return; }
    if(!f.checkValidity()){ f.reportValidity(); return; }
    var tk=f.querySelector('[name="cf-turnstile-response"]');
    if(!tk || !tk.value){
      s.className="m-form-status is-err";
      s.textContent="Please confirm in the security check that you are not a robot.";
      return;
    }
    btn.disabled=true;
    s.className="m-form-status is-sending"; s.textContent="Sending your enquiry …";
    var fd=new FormData(f); fd.delete("cf-turnstile-response");
    fetch(ENDPOINT,{method:"POST",headers:{"Accept":"application/json"},body:fd})
      .then(function(r){ return r.json().catch(function(){return {};}); })
      .then(function(){
        s.className="m-form-status is-ok";
        s.textContent="Thank you! Your enquiry has been sent – we'll get back to you shortly.";
        f.reset();
        if(window.turnstile){ turnstile.reset(); }
      })
      .catch(function(){
        s.className="m-form-status is-err";
        s.innerHTML='An error occurred while sending. Please write to us directly at <a href="mailto:office@medeqon.com">office@medeqon.com</a>.';
      })
      .then(function(){ btn.disabled=false; });
  });
})();
</script>'''

_KONT_PL = [
    (">Contact</span>", ">Kontakt</span>"),
    ("We're here for you", "Jesteśmy do Państwa dyspozycji"),
    ("Whether a project enquiry, service, consulting or the procurement of medical products — get in touch. We find the right product and deliver reliably. Our team will get back to you quickly and personally.",
     "Zapytanie projektowe, serwis, doradztwo czy zaopatrzenie w wyroby medyczne — prosimy o kontakt. Znajdziemy odpowiedni produkt i dostarczymy go niezawodnie. Nasz zespół skontaktuje się z Państwem szybko i osobiście."),
    (">Enquiry</span>", ">Zapytanie</span>"),
    ("<h2>Write to us<span", "<h2>Napisz do nas<span"),
    ("Fields marked * are required. Your enquiry goes straight to our team.",
     "Pola oznaczone * są obowiązkowe. Państwa zapytanie trafia bezpośrednio do naszego zespołu."),
    (">Email *</label>", ">E-mail *</label>"),
    (">Phone</label>", ">Telefon</label>"),
    (">Company</label>", ">Firma</label>"),
    (">Subject</label>", ">Temat</label>"),
    ("<option>Project enquiry</option>", "<option>Zapytanie projektowe</option>"),
    ("<option>Consulting</option>", "<option>Doradztwo</option>"),
    ("<option>Procurement of medical products</option>", "<option>Zaopatrzenie w wyroby medyczne</option>"),
    ("<option>Service / inspection</option>", "<option>Serwis / kontrola</option>"),
    ("<option>Other</option>", "<option>Inne</option>"),
    (">Message *</label>", ">Wiadomość *</label>"),
    ("When you submit this contact form, we process your personal data (name, email, phone number and message) in order to respond to your enquiry. The legal basis is (pre-)contractual communication pursuant to Art. 6(1)(b) GDPR. You can find further information in our <a href=\"/en/datenschutz.html\">privacy policy</a>.",
     "Wysyłając ten formularz kontaktowy, przetwarzamy Państwa dane osobowe (imię i nazwisko, adres e-mail, numer telefonu, wiadomość) w celu udzielenia odpowiedzi na Państwa zapytanie. Podstawą prawną jest komunikacja (przed)umowna zgodnie z art. 6 ust. 1 lit. b RODO. Więcej informacji znajdą Państwo w naszej <a href=\"/pl/datenschutz.html\">polityce prywatności</a>."),
    (">Send enquiry</button>", ">Wyślij zapytanie</button>"),
    ("Please enable JavaScript or write to us directly at office@medeqon.com.",
     "Prosimy włączyć JavaScript lub napisać bezpośrednio na office@medeqon.com."),
    (">Direct</span>", ">Bezpośrednio</span>"),
    (">Office</span>", ">Biuro</span>"),
    ("2102 Hagenbrunn · Austria<br>Mon – Fri · and by appointment", "2102 Hagenbrunn · Austria<br>pon. – pt. · i po umówieniu"),
    ("Please confirm in the security check that you are not a robot.",
     "Prosimy potwierdzić w teście bezpieczeństwa, że nie są Państwo robotem."),
    ('s.textContent="Sending your enquiry …";', 's.textContent="Wysyłanie zapytania …";'),
    ("Thank you! Your enquiry has been sent – we'll get back to you shortly.",
     "Dziękujemy! Państwa zapytanie zostało wysłane – wkrótce się odezwiemy."),
    ("An error occurred while sending. Please write to us directly at",
     "Podczas wysyłania wystąpił błąd. Prosimy napisać bezpośrednio na"),
]
_KONT_RO = [
    (">Contact</span>", ">Contact</span>"),
    ("We're here for you", "Suntem aici pentru dumneavoastră"),
    ("Whether a project enquiry, service, consulting or the procurement of medical products — get in touch. We find the right product and deliver reliably. Our team will get back to you quickly and personally.",
     "Fie că este vorba de o solicitare de proiect, service, consultanță sau achiziția de produse medicale — contactați-ne. Găsim produsul potrivit și livrăm cu încredere. Echipa noastră vă va răspunde rapid și personal."),
    (">Enquiry</span>", ">Solicitare</span>"),
    ("<h2>Write to us<span", "<h2>Scrieți-ne<span"),
    ("Fields marked * are required. Your enquiry goes straight to our team.",
     "Câmpurile marcate cu * sunt obligatorii. Solicitarea dumneavoastră ajunge direct la echipa noastră."),
    (">Email *</label>", ">E-mail *</label>"),
    (">Phone</label>", ">Telefon</label>"),
    (">Company</label>", ">Companie</label>"),
    (">Subject</label>", ">Subiect</label>"),
    ("<option>Project enquiry</option>", "<option>Solicitare de proiect</option>"),
    ("<option>Consulting</option>", "<option>Consultanță</option>"),
    ("<option>Procurement of medical products</option>", "<option>Achiziția de produse medicale</option>"),
    ("<option>Service / inspection</option>", "<option>Service / verificare</option>"),
    ("<option>Other</option>", "<option>Altele</option>"),
    (">Message *</label>", ">Mesaj *</label>"),
    ("When you submit this contact form, we process your personal data (name, email, phone number and message) in order to respond to your enquiry. The legal basis is (pre-)contractual communication pursuant to Art. 6(1)(b) GDPR. You can find further information in our <a href=\"/en/datenschutz.html\">privacy policy</a>.",
     "Prin trimiterea acestui formular de contact, prelucrăm datele dumneavoastră cu caracter personal (nume, e-mail, număr de telefon, mesaj) pentru a răspunde solicitării dumneavoastră. Temeiul juridic este comunicarea (pre)contractuală în conformitate cu art. 6 alin. 1 lit. b RGPD. Mai multe informații găsiți în <a href=\"/ro/datenschutz.html\">politica noastră de confidențialitate</a>."),
    (">Send enquiry</button>", ">Trimite solicitarea</button>"),
    ("Please enable JavaScript or write to us directly at office@medeqon.com.",
     "Vă rugăm activați JavaScript sau scrieți-ne direct la office@medeqon.com."),
    (">Direct</span>", ">Direct</span>"),
    (">Office</span>", ">Birou</span>"),
    ("2102 Hagenbrunn · Austria<br>Mon – Fri · and by appointment", "2102 Hagenbrunn · Austria<br>Luni – Vineri · și pe bază de programare"),
    ("Please confirm in the security check that you are not a robot.",
     "Vă rugăm să confirmați în verificarea de securitate că nu sunteți robot."),
    ('s.textContent="Sending your enquiry …";', 's.textContent="Se trimite solicitarea …";'),
    ("Thank you! Your enquiry has been sent – we'll get back to you shortly.",
     "Vă mulțumim! Solicitarea a fost trimisă – revenim în curând."),
    ("An error occurred while sending. Please write to us directly at",
     "A apărut o eroare la trimitere. Vă rugăm scrieți-ne direct la"),
]
BODY_KONTAKT_PL = _tr(BODY_KONTAKT_EN, _KONT_PL, "KONT-PL")
BODY_KONTAKT_RO = _tr(BODY_KONTAKT_EN, _KONT_RO, "KONT-RO")

# ---- Cloudflare Turnstile Site-Key (öffentlicher Schlüssel, kommt in die HTML) ----
# Nach dem Anlegen des Widgets im Cloudflare-Dashboard hier den echten Site-Key eintragen.
TURNSTILE_SITEKEY = "0x4AAAAAAEFXPvYQbzRLlVhj"
for _kn in ("BODY_KONTAKT", "BODY_KONTAKT_EN", "BODY_KONTAKT_PL", "BODY_KONTAKT_RO"):
    globals()[_kn] = globals()[_kn].replace("__TURNSTILE_SITEKEY__", TURNSTILE_SITEKEY)

# ---- Karriere (EN/PL/RO), _JOBS ist leer -> Leerzustand ----
_KARR_ICON = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" '
              'stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="15" width="32" height="24" rx="3"/>'
              '<path d="M18 15v-3a3 3 0 0 1 3-3h6a3 3 0 0 1 3 3v3"/><path d="M8 26h32"/>'
              '<circle cx="24" cy="26" r="2.4" class="sig-fill"/></svg>')

def _karriere_body(tag, h1, lede, otag, oh2, osub, empty_lead, empty_sub,
                   itag, ih2, isub, note_p, note_btn, subj):
    return f'''<section class="m-page-hero">
  <div class="m-shell">
    <span class="m-tag">{tag}</span>
    <h1>{h1}<span class="end-dot">.</span></h1>
    <p class="lede">{lede}</p>
  </div>
</section>

<section class="m-section" id="offene-positionen">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">{otag}</span>
      <h2 class="m-bigH">{oh2}<span class="end-dot">.</span></h2>
      <div class="sub">{osub}</div>
    </div>
      <div class="m-jobs-empty">
        <span class="m-jobs-empty-ic" aria-hidden="true">{_KARR_ICON}</span>
        <p class="m-jobs-empty-lead">{empty_lead}</p>
        <p class="m-jobs-empty-sub">{empty_sub}</p>
      </div>
  </div>
</section>

<section class="m-section alt" id="initiativbewerbung">
  <div class="m-shell">
    <div class="m-secH">
      <span class="m-tag">{itag}</span>
      <h2 class="m-bigH">{ih2}<span class="end-dot">.</span></h2>
      <div class="sub">{isub}</div>
    </div>
    <div class="m-dl-note">
      <p>{note_p}</p>
      <a class="m-dl-note-btn" href="mailto:office@medeqon.com?subject={subj}">{note_btn}</a>
    </div>
  </div>
</section>'''

BODY_KARRIERE_EN = _karriere_body(
    "Careers", "Become part of medeqon",
    "We combine technical expertise with personal support and work on demanding projects in medical technology. If you value quality, responsibility and direct contact with clinics and manufacturers, we look forward to meeting you.",
    "Open positions", "Current vacancies",
    "Here you will find our currently advertised positions. Click a position to see details on tasks and profile.",
    "There are currently no open positions.",
    "But we always welcome your speculative application &ndash; see below.",
    "Speculative application", "No suitable position?",
    "Convince us with your speculative application. We are continuously interested in committed people who fit medeqon &ndash; regardless of whether a position is currently advertised.",
    'Simply send us your application documents (CV, a short cover letter) by email to <a href="mailto:office@medeqon.com">office@medeqon.com</a>. We will get back to you personally.',
    "Send speculative application", "Speculative%20application")

BODY_KARRIERE_PL = _karriere_body(
    "Kariera", "Dołącz do medeqon",
    "Łączymy wiedzę techniczną z osobistą opieką i pracujemy nad wymagającymi projektami w technice medycznej. Jeśli cenisz jakość, odpowiedzialność i bezpośredni kontakt z klinikami i producentami, chętnie Cię poznamy.",
    "Otwarte stanowiska", "Aktualne oferty pracy",
    "Tutaj znajdziesz nasze aktualnie ogłaszane stanowiska. Kliknij stanowisko, aby zobaczyć szczegóły dotyczące zadań i profilu.",
    "Obecnie nie ma otwartych stanowisk.",
    "Zawsze jednak cieszymy się na Twoją aplikację spontaniczną &ndash; patrz poniżej.",
    "Aplikacja spontaniczna", "Nie ma odpowiedniego stanowiska?",
    "Przekonaj nas swoją aplikacją spontaniczną. Nieustannie poszukujemy zaangażowanych osób pasujących do medeqon &ndash; niezależnie od tego, czy akurat jest ogłoszone stanowisko.",
    'Prześlij nam po prostu swoje dokumenty aplikacyjne (CV, krótki list motywacyjny) e-mailem na <a href="mailto:office@medeqon.com">office@medeqon.com</a>. Odezwiemy się osobiście.',
    "Wyślij aplikację spontaniczną", "Aplikacja%20spontaniczna")

BODY_KARRIERE_RO = _karriere_body(
    "Cariere", "Deveniți parte din medeqon",
    "Îmbinăm expertiza tehnică cu asistența personală și lucrăm la proiecte solicitante în tehnologia medicală. Dacă apreciați calitatea, responsabilitatea și contactul direct cu clinicile și producătorii, ne bucurăm să vă cunoaștem.",
    "Posturi disponibile", "Posturi vacante actuale",
    "Aici găsiți posturile pe care le anunțăm în prezent. Faceți clic pe un post pentru a vedea detalii despre sarcini și profil.",
    "În prezent nu există posturi vacante.",
    "Însă așteptăm oricând cu plăcere candidatura dumneavoastră spontană &ndash; vezi mai jos.",
    "Candidatură spontană", "Niciun post potrivit?",
    "Convingeți-ne cu o candidatură spontană. Suntem permanent interesați de persoane dedicate care se potrivesc medeqon &ndash; indiferent dacă există în prezent un post anunțat.",
    'Trimiteți-ne pur și simplu documentele de candidatură (CV, o scurtă scrisoare de intenție) prin e-mail la <a href="mailto:office@medeqon.com">office@medeqon.com</a>. Vă vom contacta personal.',
    "Trimite candidatura spontană", "Candidatura%20spontana")

# Übersetzte Seiten je Sprache (weitere Seiten folgen). Modellgrafik = englische Version.
PAGES_EN = [
    ("index.html", "medeqon · Engineering for medical technology",
     "medeqon GmbH — Vienna-based engineering firm for medical technology. Design, consulting, procurement and safety-related inspection of clinical infrastructure.",
     BODY_INDEX_EN),
    ("leistungen.html", "Services · medeqon",
     "medeqon services: Medical Technology Design of clinical infrastructure, independent consulting and procurement, plus safety-related inspection and acceptance.",
     BODY_LEISTUNGEN_EN),
    ("produkte.html", "Products · medeqon",
     "Products from medeqon — certified medical technology: radiation protection (ROTHBAND, KENEX), medical furnishing (COINFYCARE), medical aids (MOBIAK) and manufacturer-independent procurement.",
     BODY_PRODUKTE_EN),
    ("referenzen.html", "References · medeqon",
     "Personal project references by Georg Scherzer: over 50 realised projects at AKH Vienna and VAMED with around € 84 million medical-technology procurement volume.",
     BODY_REFERENZEN_EN),
    ("management.html", "Management · medeqon",
     "The management of medeqon: over 15 years of experience in medical technology and clinical infrastructure.",
     BODY_MANAGEMENT_EN),
    ("kontakt.html", "Contact · medeqon",
     "Contact medeqon GmbH: office@medeqon.com, +43 1 3580045, Bergstraße 42/5/3, 2102 Hagenbrunn, Austria.",
     BODY_KONTAKT_EN),
    ("karriere.html", "Careers · medeqon",
     "Careers at medeqon GmbH: open positions in medical technology and the option of a speculative application to office@medeqon.com.",
     BODY_KARRIERE_EN),
    ("agb.html", "Terms &amp; Conditions · medeqon",
     "General Terms &amp; Conditions of medeqon GmbH.",
     BODY_AGB_EN),
    ("datenschutz.html", "Privacy Policy · medeqon",
     "Privacy policy of medeqon GmbH.",
     BODY_DATENSCHUTZ_EN),
    ("impressum.html", "Imprint · medeqon",
     "Imprint / legal notice of medeqon GmbH.",
     BODY_IMPRESSUM_EN),
]
PAGES_PL = [
    ("index.html", "medeqon · Inżynieria techniki medycznej",
     "medeqon GmbH — biuro inżynieryjne techniki medycznej z Wiednia. Projektowanie, doradztwo, zaopatrzenie oraz kontrola bezpieczeństwa infrastruktury klinicznej.",
     BODY_INDEX_PL),
    ("leistungen.html", "Usługi · medeqon",
     "Usługi medeqon: projektowanie techniki medycznej infrastruktury klinicznej, niezależne doradztwo i zaopatrzenie oraz kontrola bezpieczeństwa i odbiory.",
     BODY_LEISTUNGEN_PL),
    ("produkte.html", "Produkty · medeqon",
     "Produkty medeqon — certyfikowana technika medyczna: ochrona radiologiczna (ROTHBAND, KENEX), wyposażenie medyczne (COINFYCARE), środki pomocnicze (MOBIAK) oraz zaopatrzenie niezależne od producentów.",
     BODY_PRODUKTE_PL),
    ("referenzen.html", "Referencje · medeqon",
     "Osobiste referencje projektowe Georga Scherzera: ponad 50 zrealizowanych projektów w AKH Wiedeń i VAMED o wolumenie zaopatrzenia w technikę medyczną ok. 84 mln €.",
     BODY_REFERENZEN_PL),
    ("management.html", "Kierownictwo · medeqon",
     "Kierownictwo medeqon: ponad 15 lat doświadczenia w technice medycznej i infrastrukturze klinicznej.",
     BODY_MANAGEMENT_PL),
    ("kontakt.html", "Kontakt · medeqon",
     "Kontakt do medeqon GmbH: office@medeqon.com, +43 1 3580045, Bergstraße 42/5/3, 2102 Hagenbrunn, Austria.",
     BODY_KONTAKT_PL),
    ("karriere.html", "Kariera · medeqon",
     "Kariera w medeqon GmbH: otwarte stanowiska w technice medycznej oraz możliwość aplikacji spontanicznej na office@medeqon.com.",
     BODY_KARRIERE_PL),
    ("agb.html", "Regulamin · medeqon",
     "Ogólne warunki handlowe (regulamin) medeqon GmbH.",
     BODY_AGB_PL),
    ("datenschutz.html", "Polityka prywatności · medeqon",
     "Polityka prywatności medeqon GmbH.",
     BODY_DATENSCHUTZ_PL),
    ("impressum.html", "Nota prawna · medeqon",
     "Nota prawna medeqon GmbH.",
     BODY_IMPRESSUM_PL),
]
PAGES_RO = [
    ("index.html", "medeqon · Inginerie pentru tehnologia medicală",
     "medeqon GmbH — birou de inginerie pentru tehnologia medicală din Viena. Proiectare, consultanță, achiziții și verificarea siguranței infrastructurii clinice.",
     BODY_INDEX_RO),
    ("leistungen.html", "Servicii · medeqon",
     "Serviciile medeqon: proiectarea tehnologiei medicale a infrastructurii clinice, consultanță și achiziții independente, precum și verificarea siguranței și recepția.",
     BODY_LEISTUNGEN_RO),
    ("produkte.html", "Produse · medeqon",
     "Produse de la medeqon — tehnologie medicală certificată: protecție radiologică (ROTHBAND, KENEX), mobilier medical (COINFYCARE), mijloace ajutătoare (MOBIAK) și achiziții independente de producători.",
     BODY_PRODUKTE_RO),
    ("referenzen.html", "Referințe · medeqon",
     "Referințe de proiect personale ale lui Georg Scherzer: peste 50 de proiecte realizate la AKH Viena și VAMED, cu un volum de achiziții de tehnologie medicală de cca. 84 mil. €.",
     BODY_REFERENZEN_RO),
    ("management.html", "Management · medeqon",
     "Conducerea medeqon: peste 15 ani de experiență în tehnologia medicală și infrastructura clinică.",
     BODY_MANAGEMENT_RO),
    ("kontakt.html", "Contact · medeqon",
     "Contact medeqon GmbH: office@medeqon.com, +43 1 3580045, Bergstraße 42/5/3, 2102 Hagenbrunn, Austria.",
     BODY_KONTAKT_RO),
    ("karriere.html", "Cariere · medeqon",
     "Cariere la medeqon GmbH: posturi în tehnologia medicală și posibilitatea unei candidaturi spontane la office@medeqon.com.",
     BODY_KARRIERE_RO),
    ("agb.html", "Termeni și condiții · medeqon",
     "Termeni și condiții generale ale medeqon GmbH.",
     BODY_AGB_RO),
    ("datenschutz.html", "Politica de confidențialitate · medeqon",
     "Politica de confidențialitate a medeqon GmbH.",
     BODY_DATENSCHUTZ_RO),
    ("impressum.html", "Notă legală · medeqon",
     "Notă legală a medeqon GmbH.",
     BODY_IMPRESSUM_RO),
]

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
    ("karriere.html", "Karriere · medeqon",
     "Karriere bei medeqon GmbH: offene Positionen in der Medizintechnik und jederzeit die Möglichkeit zur Initiativbewerbung an office@medeqon.com.",
     "Karriere", BODY_KARRIERE),
    ("kontakt.html", "Kontakt · medeqon",
     "Kontakt zu medeqon GmbH: office@medeqon.com, +43 1 3580045, Bergstrasse 42/5/3, 2102 Hagenbrunn.",
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
    html = page(filename, title, desc, body, lang="de")
    (ROOT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename)

# Übersetzte Seiten nach /en/, /pl/, /ro/
for _lang, _pages in (("en", PAGES_EN), ("pl", PAGES_PL), ("ro", PAGES_RO)):
    (ROOT / _lang).mkdir(exist_ok=True)
    for filename, title, desc, body in _pages:
        html = page(filename, title, desc, body, lang=_lang)
        (ROOT / _lang / filename).write_text(html, encoding="utf-8")
        print("wrote", _lang + "/" + filename)
print("done")
