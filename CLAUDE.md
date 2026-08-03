# medeqon Website — Projekt- & Arbeitsanleitung

**Diese Datei ist zweierlei:**
1. Eine **Anleitung für Georg**, wie er später mit Claude Änderungen an der Website macht (Teil A).
2. Eine **vollständige technische Referenz**, damit sich eine neue Claude-Sitzung sofort auskennt (Teil B).

> **Für eine neue Claude-Sitzung:** Bitte zuerst diese Datei komplett lesen, danach `build.py`.
> Alle Änderungen laufen über die Quellen (`build.py`, die `*.json`-Dateien, `styles.css`,
> `content/*.html`) — **niemals** direkt in den fertigen HTML-Dateien. Danach `python3 build.py`
> ausführen und die geänderten Dateien ins Repo schreiben. Georg committet + pusht.

---

## TEIL A — So arbeitest du (Georg) mit Claude

### 1. Neue Sitzung starten
1. In der **Claude-Desktop-App** eine neue **Cowork-Aufgabe** starten und die Desktop-App
   verbunden lassen (damit Claude über die Datei-Brücke auf dein Repo zugreifen kann).
2. Diese Datei (`CLAUDE.md`) in den Chat laden **oder** Claude bitten:
   *„Öffne mein Repo `medeqon-homepage` und lies zuerst `CLAUDE.md`, dann `build.py`."*
3. Kurz warten, bis Claude bestätigt, dass es sich eingelesen hat.

### 2. Der Ablauf (immer gleich)
1. Du beschreibst die Änderung in normalen Worten.
2. Claude ändert die **Quelldateien** (nicht die fertigen HTML-Seiten), baut mit `python3 build.py`
   neu und schreibt **nur die geänderten Dateien** in dein Repo.
3. Du öffnest **GitHub Desktop**, siehst die Änderungen, klickst **„Commit to main"** und **„Push"**.
4. **IONOS Deploy Now** veröffentlicht automatisch (dauert meist 1–3 Minuten).
5. Danach am besten die Live-Seite prüfen — bei Übersetzungen ruhig in mehreren Sprachen.

### 3. Wichtig, damit es reibungslos läuft
- **Sag immer, welche Seite** gemeint ist (Startseite, Leistungen, Produkte, Referenzen,
  Management, Karriere, Kontakt, AGB/Datenschutz/Impressum).
- **Sag, ob es alle Sprachen betrifft** (DE/EN/PL/RO) oder nur eine. In der Regel: alle.
- **Neue Dateien (PDFs, Bilder):** gib Claude den **genauen Ordnerpfad** auf deinem Rechner.
  Claude holt sie sich dann selbst über die Datei-Brücke. Beispiel-Ordner, die wir schon genutzt haben:
  `…\9. EINRICHTUNGSKATALOG\0_Firmen Unterlagen\ROTHBAND - Firmen Unterlagen\…`
- **Screenshots helfen enorm.** Wenn dir etwas optisch nicht gefällt, mach einen Screenshot und
  markiere die Stelle (z. B. rot einkringeln) — so trifft Claude die richtige Stelle sofort.
- **Speicherplatz:** Das IONOS-Projekt ist Typ **„Static" = 1 GB** pro Deployment. Die Website ist
  aktuell ~170 MB, du hast also viel Reserve. Größe ist normalerweise kein Thema.

### 4. Beispiel-Sätze für typische Änderungen
- *„Auf der Produkte-Seite beim Modell ENID die Beschreibung ändern auf …"*
- *„Füge auf der Referenzen-Seite ein neues Projekt in der Kategorie Österreich hinzu: Name …, Umfang …, Kosten …"*
- *„Ich habe neue Projektbilder in den Ordner … gelegt — bitte im medeqon-Stil mit Logo hochladen."*
- *„Ändere die Telefonnummer im Footer auf …"*
- *„Neues Datenblatt für Produkt X — liegt im Ordner …, bitte in den Download-Bereich einbauen."*
- *„Übersetze den neuen Text auch ins Englische, Polnische und Rumänische."*

---

## TEIL B — Technische Referenz (für Claude)

### 1. Was ist das?
Statische Website **www.medeqon.com** (medeqon GmbH, Ingenieurbüro für Medizintechnik in Wien).
**Alle** HTML-Seiten werden von **`build.py`** aus JSON-Datenquellen, `styles.css`,
`content/*.html` und den i18n-Daten erzeugt. Kein CMS, kein Framework — reines HTML/CSS + etwas
Vanilla-JS, generiert durch ein Python-Skript.

- **Fonts:** Hanken Grotesk (Display) + IBM Plex Mono.
- **Farb-Tokens** in `styles.css` (`:root`): `--ink #0F1B2C`, `--steel #6B7785`, `--mist #D5DAE0`,
  `--paper #FFF`, `--mist-blue #E8EEF7`, `--signal #004AAD`, `--sky #5B9BD5`,
  `--brand-700 #003278`, `--deep-800 #0a1228`.

### 2. Deployment
- **IONOS Deploy Now**, Projekt-Typ **Static (1 GB/Deployment)**. Ausgelöst durch **git push**
  (Georg via GitHub Desktop). IONOS baut/veröffentlicht automatisch.
- Repo-Ordner auf Georgs Rechner (der von GitHub Desktop verfolgte Ordner, Branch `main`):
  `…\Homepage\GitHub Homepage\medeqon-homepage\`
- **Nur die tatsächlich geänderten Dateien** ins Repo schreiben (kein Voll-Snapshot), damit
  GitHub Desktop eine saubere Change-Liste zeigt.
- Claude läuft in der Cloud und schreibt über die **Datei-Brücke** (`mcp__remote-devices__…`,
  `SendUserFile` → `device_commit_files`) ins Repo. **Wichtig:** Bei mehreren Dateien die
  `fileUuid → devicePath`-Zuordnung sorgfältig prüfen (schon mal Quelle von Fehlern gewesen).

### 3. Der EINZIGE richtige Ablauf beim Bauen
1. Änderung an den **Quellen** machen: `build.py`, `*.json`, `styles.css`, `content/*.html`,
   `i18n/*.json`. **Niemals** die fertigen `*.html` direkt editieren.
2. `python3 build.py` ausführen → erzeugt alle HTML-Seiten (Root = Deutsch, `/en/ /pl/ /ro/`).
3. Auf **WARN**-Meldungen im Build achten (fehlende Übersetzungen etc.).
4. Nur die geänderten Dateien ins Repo schreiben. Georg committet + pusht.

### 4. Repo-Struktur
```
build.py                  # DER Generator (alles wird hier gesteuert)
styles.css                # globales CSS
index.html, leistungen.html, produkte.html, referenzen.html,
management.html, karriere.html, kontakt.html,
agb.html, datenschutz.html, impressum.html      # generiert (DE, Root)
en/  pl/  ro/             # generierte Übersetzungen (gleiche Dateinamen)
products.json             # Medizinische Einrichtung (COINFYCARE): 36 Produkte
kenex.json                # Montierter Strahlenschutz (KENEX)
strahlenschutz.json       # Persönlicher Strahlenschutz (ROTHBAND, PSA)
heilbehelfe.json          # Heilbehelfe & Hilfsmittel (MOBIAK)
referenzen.json           # Projektreferenzen (Gruppen + Projekte)
content/agb.html, datenschutz.html, impressum.html         # Rechtstexte DE
content/agb.<lang>.html, datenschutz.<lang>.html, …        # Rechtstexte EN/PL/RO
i18n/ref_<lang>.json                # Referenzen: Projektnamen/-umfang übersetzt
i18n/prod_<quelle>_<lang>.json      # Produktdaten übersetzt (key = slug)
assets/                   # Bilder, PDFs, Marken-Logos …
  assets/produkte/<slug>/…jpg       # Produktbilder
  assets/ref/<slug>/…jpg            # Projektbilder (Referenzen)
  assets/downloads/med/…pdf         # Datenblätter Medizinische Einrichtung
  assets/downloads/ss/…pdf          # ROTHBAND-Kataloge + OUTLAST (Strahlenschutz)
  assets/brands/  assets/optionen/  assets/farben/  …
```

### 5. `build.py` — Architektur in Kürze
- **Seiten-Gerüst:** `header(filename, lang)`, `footer(lang)`, `page(filename, title, desc, body, lang)`
  bauen Kopf/Fuß/Grundgerüst. Body-Strings (`BODY_INDEX`, `BODY_LEISTUNGEN`, `BODY_PRODUKTE`,
  `BODY_REFERENZEN`, …) enthalten den Seiteninhalt.
- **Seiten-Listen:** `PAGES` (Deutsch), `PAGES_EN`, `PAGES_PL`, `PAGES_RO`. Die Generierungs-Schleife
  am Ende schreibt alle Seiten.
- **`AVAILABLE`** (dict pro Sprache): welche Seite in welcher Sprache existiert. `_href(filename, lang)`
  verlinkt sprachspezifisch bzw. fällt auf Deutsch zurück.
- **Navigation/Fuß:** `NAV_LABELS`, `_FOOT_T` (Übersetzungen), `FLAGS` (Inline-SVG-Landesflaggen),
  `_lang_switcher(...)` (Sprachumschaltung durch Klick auf die Flagge).

### 6. Mehrsprachigkeit (DE / EN / PL / RO)
- Deutsch liegt im **Wurzelverzeichnis**, Übersetzungen unter `/en/ /pl/ /ro/`.
  Übersetzte Seiten nutzen **root-absolute Pfade** (`/assets/…`, `/styles.css`), damit sie am
  Domain-Root korrekt laden.
- **Übersetzungs-Mechanik:**
  - `_tr(html, pairs, label)` — Phrasen-Ersetzung (Startseite etc.).
  - `_uit` / `_puit` / `_reft` / `_prodt` — Nachschlage-Übersetzer für Referenzen bzw. Produkte.
  - **Statische UI-Texte** stehen als Wörterbücher direkt in `build.py`: `_REFUI` (Referenzen),
    `_PUI` (Produkte), `_FOOT_T`, `NAV_LABELS`.
  - **Daten-Übersetzungen** (Projekte, Produkte) liegen als JSON in `i18n/`.
- **Kontrolle:** Fehlende Übersetzungen sammeln sich beim Build in `_UIT_MISS` / `_PUIT_MISS`
  (Daten-Lücken zusätzlich als **WARN**). Bei neuen Texten immer die passenden Wörterbuch-/JSON-
  Einträge in **allen** Sprachen nachziehen.
- **WICHTIGE TERMINOLOGIE:** „Planung" wird im **Englischen immer** als **„Medical Technology
  Design"** übersetzt (Marken-/Klarheitsentscheidung des Kunden). PL „Projektowanie techniki
  medycznej", RO „Proiectarea tehnologiei medicale".

### 7. Diagramme (Inline-SVG, kein Pixelbild)
Auf der Startseite werden drei Grafiken als **Inline-SVG** in `build.py` erzeugt (scharf,
übersetzbar, verschwimmen mit dem hellblauen Hintergrund `#E8EEF7`):
- **Integriertes Planungsmodell / Integrated Design Model:** `_design_model_svg(lang)` — Ring mit
  4 Segmenten (Architektur/Medizintechnik/Gebäudetechnik/Betriebsorganisation), BIM-Kern,
  4 Außenlabels mit Knick-Linien. Wird per `_inject_model(...)` in alle Startseiten eingesetzt.
- **BIM-Koordinationsgrafik** (IFC/REVIT/BCF/Daten) — Inline-SVG im Startseiten-Body.
- **Kosten-Diagramm „Kosteneffizienz durch frühe Planung"** (`m-tco-chart`) — Inline-SVG; Achsen/
  Beschriftungen schwarz (`#0F1B2C`), dünner Rahmen, transparent (verschwimmt mit dem Hintergrund).

### 8. Download-Bereiche
Gegliedert nach Produktkatalog. Zwei aktive Bereiche mit echten Download-Buttons:
- **Medizinische Einrichtung** (`assets/downloads/med/`): pro Produkt **Datenblatt (DE)** + **DataSheet (EN)**.
  - Namensregel: `Datenblatt_<MODELL>.pdf` (DE), `DataSheet_<MODELL>.pdf` (EN); `<MODELL>` in
    Großbuchstaben, Leerzeichen → Unterstrich (z. B. `Datenblatt_KEND_PRO.pdf`).
  - Struktur in `DL_MED_CATS`, gerendert von `_downloads_datasheets(...)` (mit Unterüberschriften
    Fix/Hydraulisch/Elektrisch/Chiropraktisch etc.). Karten via `_ds_card(model, lang)`.
- **Strahlenschutz** (`assets/downloads/ss/`): **ROTHBAND-Kataloge** (Persönliche Schutzausrüstung,
  Schnittbildgebung, Strahlenschutzbrillen, Zubehör) je DE/EN/PL + **OUTLAST „Innenmaterial"** DE/EN/PL.
  - Struktur in `DL_STRAHLENSCHUTZ` (Helper `_cat3(base)` erzeugt die DE/EN/PL-Links),
    gerendert von `_downloads_category(..., lang)`; Karten via `_dl_card(item, lang)`.
  - Dateinamen: `Katalog_<Thema>_ROTHBAND_<DE|EN|PL>.pdf`, `OUTLAST_Innenmaterial_<DE|EN|PL>.pdf`.
- Heilbehelfe steht weiterhin auf **„auf Anfrage"** (kein Download; nur Hinweis + Kontakt-Button).
- **Große PDFs:** Die Datei-Brücke akzeptiert max. **20 MB/Datei**. Größere PDFs vor dem Commit mit
  Ghostscript verkleinern, z. B. auf ~200 dpi:
  `gs -sDEVICE=pdfwrite -dNOPAUSE -dQUIET -dBATCH -dColorImageResolution=200 -dGrayImageResolution=200 -sOutputFile=out.pdf in.pdf`

### 9. Referenzen — Filter-Kategorien
Die filterbaren „Realisierte Projekte" werden aus `referenzen.json` erzeugt. Die beiden AKH-Wien-
Gruppen (`akh-persoenlich`, `akh-leitung`) werden per **`_REF_GID_MAP`** zu **einer** Kategorie
**„Österreich"** zusammengefasst (EN/PL/RO: „Austria"). Labels in `_REF_FLABEL`, Übersetzungen in
`_REFUI`. Weitere Kategorien: Schweiz, Internationale Projekte. Zusätzlich: Wissenschaft & Forschung
und Consulting & Lehre als eigene Filter-Grids.

### 10. Häufige Fehlerquellen (bitte vermeiden)
- Dateien NIEMALS in `…\IONOS Deploy Now\GITHUB Uploads\…` ablegen — das ist NICHT das Git-Repo.
  Einziger richtiger Zielordner: `…\GitHub Homepage\medeqon-homepage\`.
- Beim Post-hoc-Ersetzen von Text (`_tr`/Chrome-Ersetzung) auf **kurze Schlüssel** achten
  (z. B. „Fix" traf früher „Fixed" → „Fixeded"). Kurze Wörter mit Tag-Kontext ersetzen.
- Sonderzeichen in Python-Strings: gerade Anführungszeichen `"` in `"..."`-Strings escapen (`\"`).
- Nach dem Build immer prüfen: keine WARN, `_UIT_MISS`/`_PUIT_MISS` nur erwartete Durchläufer
  (Eigennamen, englische Titel), keine deutschen Reste auf EN/PL/RO-Seiten.

### 11. Verifikation vor dem Ausliefern
- `python3 build.py` — auf WARN/Errors achten.
- Optional lokal rendern: `python3 -m http.server 8099` + Screenshots via Playwright
  (Chromium unter `/opt/pw-browsers/chromium`) über `http://localhost:8099/…`. `file://`
  funktioniert nicht, weil die übersetzten Seiten root-absolute Pfade nutzen.
- Übersetzte Seiten stichprobenartig in mehreren Sprachen ansehen.

---

*Stand: Website vollständig viersprachig (DE/EN/PL/RO). Alle Hauptseiten, Referenzen, Produkte,
Rechtstexte übersetzt. Download-Bereiche für Medizinische Einrichtung und Strahlenschutz aktiv.
Rechtstexte (AGB/Datenschutz) sind sinngemäß maschinell übersetzt — vor rechtsverbindlicher
Nutzung juristisch prüfen lassen.*
