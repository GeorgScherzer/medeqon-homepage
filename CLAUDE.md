# Arbeitsanweisung für Claude – medeqon Homepage

Diese Datei beschreibt, wie an der medeqon-Website gearbeitet wird.
**Jede neue Claude-Sitzung liest zuerst diese Datei und hält sich daran.**

## Was ist das?
Statische Website (www.medeqon.com). Alle Seiten werden von `build.py` aus
JSON-Datenquellen + `styles.css` generiert. Deployment über IONOS Deploy Now,
ausgelöst durch einen Git-Push von Georg.

## Der EINZIGE richtige Ablauf
1. Änderungen immer an den Quellen machen: `build.py`, die `*.json`-Dateien
   (products.json, strahlenschutz.json, kenex.json, heilbehelfe.json,
   referenzen.json, …) und/oder `styles.css`.
2. `python3 build.py` ausführen → erzeugt die fertigen HTML-Seiten.
3. Die geänderten Dateien werden DIREKT in dieses Repo geschrieben:
   `…\Homepage\GitHub Homepage\medeqon-homepage\`
   (der Ordner, den GitHub Desktop als Repository „medeqon-homepage" auf
   Branch `main` verfolgt).
4. Georg committet in GitHub Desktop ("Commit to main") und pusht.
   IONOS Deploy Now übernimmt das Deployment automatisch.

## WICHTIG – häufige Fehlerquelle
- Dateien NIEMALS in `…\IONOS Deploy Now\GITHUB Uploads\…` ablegen.
  Das ist NICHT das Git-Repo; GitHub Desktop zeigt dort keine Changes an.
- Der einzig richtige Zielordner ist das Git-Repo oben (`medeqon-homepage`).
- Es werden nur die tatsächlich GEÄNDERTEN Dateien geschrieben (kein
  Voll-Snapshot), damit Georg in GitHub Desktop eine saubere Change-Liste hat.

## Datenblätter / Downloads
- Ablage: `assets/downloads/med/`
- Namensregel Deutsch:  `Datenblatt_<MODELL>.pdf`  (z. B. `Datenblatt_ENID.pdf`)
- Namensregel Englisch: `DataSheet_<MODELL>.pdf`   (z. B. `DataSheet_ENID.pdf`)
- `<MODELL>` = Produktname in Großbuchstaben, Leerzeichen → Unterstrich
  (z. B. `KEND_PRO`, `ALU_SCREEN_1518`).
- Der Downloadbereich ist wie der Produktkatalog gegliedert
  (01 Untersuchungsliegen mit Fix/Hydraulisch/Elektrisch/Chiropraktisch als
  einfache Überschriften, 02 Medizinische Stühle, 03 Sichtschutz).

## Design-Kurzreferenz
- Fonts: Hanken Grotesk (Display) + IBM Plex Mono.
- Farb-Tokens in `styles.css` (:root): --ink #0F1B2C, --steel #6B7785,
  --mist #D5DAE0, --paper #FFF, --mist-blue #E8EEF7, --signal #004AAD,
  --sky #5B9BD5, --brand-700 #003278, --deep-800 #0a1228.

## Mehrsprachigkeit (DE / EN / PL / RO)
Die Website ist viersprachig: Deutsch liegt im Wurzelverzeichnis, die
Übersetzungen unter `/en/`, `/pl/`, `/ro/`. Alles wird von `build.py` erzeugt.
- **Steuerung:** `LANGS`, `AVAILABLE` (welche Seite je Sprache existiert),
  `NAV_LABELS`, `_FOOT_T`, Länderflaggen-Umschalter (`FLAGS`, `_lang_switcher`).
- **Wichtige Terminologie:** „Planung" wird im Englischen immer als
  **„Medical Technology Design"** übersetzt (Marken-/Klarheitsentscheidung).
- **Übersetzungsdaten** liegen in `i18n/` (JSON) und `content/*.<lang>.html`:
  - `i18n/ref_<lang>.json` – Projektnamen/-umfang der Referenzen.
  - `i18n/prod_<quelle>_<lang>.json` – Produktdaten (Modell/Beschreibung/Specs),
    Schlüssel = `slug`; Zahlen/Einheiten/Normen/Modellcodes bleiben unverändert.
  - `content/agb.<lang>.html`, `datenschutz.<lang>.html`, `impressum.<lang>.html`
    – übersetzte Rechtstexte (HTML-Struktur identisch zum Deutschen).
- **Statische UI-Texte** stehen als Wörterbücher direkt in `build.py`
  (`_REFUI`, `_PUI`, `_FOOT_T`, `NAV_LABELS`). Fehlende Übersetzungen werden beim
  Build in `_UIT_MISS` / `_PUIT_MISS` gesammelt (Kontrolle: sollten leer sein).
- **Neue Inhalte übersetzen:** deutschen Text in Quelle/JSON ergänzen, dann die
  entsprechenden `i18n/`- bzw. `_PUI`/`_REFUI`-Einträge nachziehen, `build.py`
  laufen lassen und auf WARN-Meldungen achten.
- **Hinweis Rechtstexte:** AGB/Datenschutz sind sinngemäß maschinell übersetzt –
  vor rechtsverbindlicher Nutzung juristisch prüfen lassen.

## So arbeitet Georg mit Claude weiter (auch nach Monaten)
1. In der Claude-Desktop-App eine neue Cowork-Aufgabe starten und die
   Desktop-App verbunden lassen (Datei-Brücke).
2. Claude bitten, dieses Repo zu öffnen und `CLAUDE.md` sowie `build.py` zu lesen.
3. Änderung beschreiben – Claude passt die Quellen an, baut neu und schreibt
   ins Repo. Georg committet + pusht in GitHub Desktop.
