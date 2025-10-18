# Kapitel 2: Die Anatomie eines perfekten Arbeitsauftrags

## Ein Python-Projekt mit dem Cement Framework starten - Ein Musterbeispiel aus der Praxis

### Die Herausforderung

Stell dir vor, du hast ein Problem:

**Situation:**
- Du hast tagelang versucht, ein Cement v3 Projekt aufzusetzen
- GitHub Actions schlagen seit Tagen fehl
- Die manuelle Implementation funktioniert nicht
- `cement generate` ist nicht installiert (und soll es auch nicht sein)

**Ziel:**
- Ein funktionierendes Cement v3 Projekt
- Automatisierte Installation
- GitHub Actions müssen grün werden
- Alles ohne manuelle Vorarbeit

**Die Frage:**
**Wie schreibt man einen Arbeitsauftrag, der dieses Problem löst?**

In diesem Kapitel analysieren wir einen echten Arbeitsauftrag aus unserer aktuellen Session - Version 4, die finale Version nach mehreren Iterationen.

### Die Evolution eines Arbeitsauftrags

Bevor wir zum finalen Auftrag kommen, schauen wir uns die Evolution an:

#### Version 1: Der naive Ansatz
*"Nutze cement generate in /tmp und dokumentiere die Struktur."*

**Problem:** 
- Arbeitet in /tmp (nicht im Repository)
- Erfordert cement Installation
- Komplizierter Transfer

#### Version 2: Der schnelle Fix
*"Nutze cement generate ccb direkt im Repository."*

**Problem:**
- Erfordert immer noch cement Installation
- DevOps muss vorab arbeiten
- Widerspricht Automatisierungs-Prinzip

#### Version 3: Pfad-Korrektur
*"Entferne cd ~/ccc-code - Aider-1 ist bereits im Repository."*

**Problem:**
- Immer noch cement generate erforderlich
- Kern-Problem nicht gelöst

#### Version 4: Die Lösung ✅
*"Erstelle Cement v3 Projekt manuell nach Best Practices aus offizieller Dokumentation."*

**Erfolg:**
- Keine Vorinstallation nötig
- Automatisierung bleibt intakt
- Vollständiger Code inklusive
- Klar strukturiert

**Was haben wir gelernt?**
Ein guter Arbeitsauftrag entsteht durch **Iteration und Feedback**. Version 1 war nicht schlecht - sie war nur nicht die richtige Lösung für das Problem.

### Der Muster-Arbeitsauftrag: Anatomie

Schauen wir uns jetzt den finalen Auftrag im Detail an. Ich zeige dir die Struktur und erkläre, **warum** jeder Teil wichtig ist.

#### Teil 1: Der Kopf - Orientierung geben

```markdown
# Arbeitsauftrag für Aider-1: CCB Phase 1 - Cement v3 Projekt erstellen (v4)

**Phase:** 1 von 4  
**Ziel:** Cement v3 Projekt manuell nach Best Practices erstellen  
**Arbeitsverzeichnis:** Repository Root (du bist bereits dort)
```

**Warum dieser Kopf?**

1. **Klarer Titel** - Empfänger (Aider-1) kennt sofort das Thema
2. **Versionierung** (v4) - Zeigt, dass iteriert wurde
3. **Phasen-Kontext** (1 von 4) - Agent versteht, dass es weitergehen wird
4. **Ein-Satz-Ziel** - Kristallklar, was erreicht werden soll
5. **Arbeitsverzeichnis** - Keine Verwirrung über Pfade

**❌ Schlechtes Beispiel:**
```markdown
# Auftrag

Mach bitte was mit Cement.
```

**✅ Gutes Beispiel:**
```markdown
# Arbeitsauftrag für Aider-1: Neues Python CLI Tool mit Cement Framework (Phase 1)

**Ziel:** Funktionsfähiges Cement v3 Projekt erstellen
**Kontext:** Du bist im Repository Root
```

#### Teil 2: Das Warum - Kontext schaffen

```markdown
## 🎯 Ziel

Erstelle ein funktionierendes Cement v3 Projekt als neue ccb/ Basis 
**nach den offiziellen Cement v3 Best Practices**.

**Warum manuelle Erstellung:** 
- cement generate ist nicht vorab installiert
- Wir bauen ein Installationstool - alles muss automatisiert funktionieren
- Die offizielle Cement v3 Struktur ist dokumentiert und kann repliziert werden

**Status:** ccb-old/ Backup ist bereits erstellt, ccb/ Verzeichnis ist frei
```

**Warum dieser Kontext?**

1. **Wiederholt das Ziel** - Redundanz ist gut bei komplexen Aufträgen
2. **Erklärt das Warum** - Agent versteht den Grund
3. **Gibt Status** - Agent weiß, was schon gemacht wurde
4. **Setzt Erwartungen** - "Manuell nach Best Practices"

**Das Learning:**
Ein guter AI Agent will verstehen **WARUM** er etwas tut. Das macht ihn zu einem besseren Partner.

#### Teil 3: Die Referenz - Wissen vermitteln

```markdown
## 📚 Cement v3 Struktur (aus offizieller Dokumentation)

Erstelle diese Struktur nach Cement v3 Best Practices:

```
ccb/
├── __init__.py
├── main.py
├── controllers/
│   ├── __init__.py
│   └── base.py
├── core/
│   ├── __init__.py
│   ├── exc.py
│   └── version.py
...
```

**Quelle:** https://docs.builtoncement.com/getting-started/...
```

**Warum diese Referenz?**

1. **Visuelle Struktur** - Agent sieht das Ziel
2. **Offizielle Quelle** - Credibility
3. **Nachvollziehbar** - DevOps kann prüfen

**Das Learning:**
Wenn du willst, dass ein AI Agent eine Struktur erstellt, **zeige sie ihm visuell**.

#### Teil 4: Der Code - Keine Geheimnisse

Hier kommt der mächtigste Teil des Auftrags. Ich habe **den kompletten Code** bereitgestellt:

```markdown
## 🔧 Was zu tun ist

### Schritt 1: ccb/ Modul-Struktur erstellen

#### ccb/__init__.py
```python
"""CCC Beta (ccb) - Experimental tools for CCC CODE development"""

VERSION = '0.1.0'

def get_version():
    return VERSION
```

#### ccb/main.py
```python
"""Main application entry point"""
from cement import App, Controller, ex
from ccb.core.version import get_version

VERSION_BANNER = """
CCC Beta (ccb) v%s
...
""" % get_version()

class Base(Controller):
    class Meta:
        label = 'base'
        ...
```

**Warum kompletter Code?**

Das ist die Kern-Innovation dieses Auftrags:

1. **Keine Interpretation nötig** - Agent sieht genau was zu tun ist
2. **Copy & Paste ready** - Schnelle Umsetzung
3. **Keine Fehlerquelle** - Code ist geprüft
4. **Lern-Effekt** - Agent sieht Best Practices
5. **Zeitersparnis** - Kein Hin und Her

**Das Learning:**
**Code zeigen ist 100x besser als Code beschreiben.**

#### Teil 5: Die Tests - Erfolg messbar machen

```markdown
## ✅ Test-Kriterien

### Lokal testen (VOR Commit):
```bash
# Installation
sudo -E bash install-ccb

# Basis-Commands
ccb --version
ccb --help
ccb info

# Test Suite
bash tests-ccb/travis.sh
```

### Must Have:
- [ ] ccb/ Verzeichnis mit korrekter Cement v3 Struktur
- [ ] setup-ccb.py funktionsfähig
- [ ] install-ccb angepasst
- [ ] tests-ccb/ mit funktionierenden Tests
```

**Warum Test-Kriterien?**

1. **Klare Definition von "Fertig"**
2. **Agent weiß wie er prüfen soll**
3. **DevOps kann verifizieren**
4. **Keine Missverständnisse**

**Das Learning:**
**"Fertig" ohne Test-Kriterien ist nicht fertig.**

#### Teil 6: Die Checkliste - Komplexität managen

```markdown
## 📋 Checkliste

- [ ] ccb/ Modul-Struktur erstellt
- [ ] ccb/main.py mit Base Controller
- [ ] ccb/core/version.py und exc.py
- [ ] Alle __init__.py Dateien
- [ ] setup-ccb.py erstellt
- [ ] install-ccb angepasst
- [ ] tests-ccb/cli/test_ccb_commands.py
- [ ] tests-ccb/travis.sh (executable!)
- [ ] test-ccb.yml geprüft/angepasst
- [ ] Lokale Tests: Installation ✅
- [ ] Lokale Tests: Commands ✅
- [ ] Lokale Tests: Test Suite ✅
- [ ] Bereit für Commit
```

**Warum eine Checkliste?**

Bei komplexen Aufträgen (13+ Punkte):
- Übersicht behalten
- Nichts vergessen
- Fortschritt tracken
- Motivation sehen

**Das Learning:**
**Checklisten sind für komplexe Aufträge essentiell.**

#### Teil 7: Die Warnungen - Kritisches hervorheben

```markdown
## 🚨 Wichtige Hinweise

1. **Cement v3 Best Practices replizieren** - Struktur aus offizieller Doku
2. **Keine Plugins in Phase 1** - nur Basis-Funktionalität
3. **Lokal testen VOR Commit** - alle Commands müssen funktionieren
4. **setup-ccb.py separat** - NICHT setup.py überschreiben
5. **Fehlerbehandlung in main()** - für saubere Exit Codes
```

**Warum Warnungen?**

- Kritische Punkte hervorheben
- Fehler vermeiden
- Best Practices betonen

**Das Learning:**
**Was schief gehen kann, wird schief gehen - außer man warnt davor.**

### Die 5 Prinzipien perfekter Arbeitsaufträge

Aus unserer Erfahrung:

#### Prinzip 1: WAS vor WIE

**Definiere das Ziel, nicht jeden Schritt.**

```markdown
✅ "Erstelle ein funktionierendes Cement v3 Projekt"
❌ "Öffne Terminal, tippe cd, dann mkdir, dann..."
```

**Warum?**
AI Agents können denken. Gib ihnen den Raum dazu.

#### Prinzip 2: Show, don't tell

**Code zeigen statt beschreiben.**

```markdown
✅ Kompletter Code im Auftrag
❌ "Erstelle eine Funktion die..."
```

**Warum?**
Eliminiert Interpretation und Fehler.

#### Prinzip 3: Kontext ist König

**Erkläre WARUM, nicht nur WAS.**

```markdown
✅ "Warum manuelle Erstellung: cement generate widerspricht Automatisierungs-Prinzip"
❌ "Erstelle manuell"
```

**Warum?**
Verständnis führt zu besseren Entscheidungen.

#### Prinzip 4: Test-getrieben denken

**Definiere Erfolg messbar.**

```markdown
✅ "Erfolg = Installation + Commands + Tests alle ✅"
❌ "Wenn es funktioniert"
```

**Warum?**
Klare Definition von "Fertig".

#### Prinzip 5: Iteration ist normal

**Version 1 → Feedback → Version 2 → Feedback → Version 3**

```markdown
✅ Arbeitsauftrag v4 (nach 3 Iterationen)
❌ "Muss perfekt beim ersten Mal sein"
```

**Warum?**
Qualität durch Feedback, nicht durch Raten.

### Do's & Don'ts: Die 7 häufigsten Fehler

#### Fehler 1: Zu vage

```markdown
❌ "Erstelle ein CLI Tool"
✅ "Erstelle ein Cement v3 CLI Tool mit info Command und --version Flag"
```

#### Fehler 2: Ohne Code

```markdown
❌ "Erstelle eine main.py mit Controller"
✅ [Kompletter Code für main.py im Auftrag]
```

#### Fehler 3: Ohne Test-Kriterien

```markdown
❌ "Wenn fertig, commit"
✅ "Erst wenn alle Tests grün, dann commit"
```

#### Fehler 4: Ohne Kontext

```markdown
❌ "Erstelle Setup-Datei"
✅ "Erstelle setup-ccb.py (nicht setup.py!) für Cement v3"
```

#### Fehler 5: Annahmen treffen

```markdown
❌ "cement generate ist installiert"
✅ "Manuelle Erstellung (cement generate nicht vorhanden)"
```

#### Fehler 6: Kritisches verstecken

```markdown
❌ "Ach ja, setup.py nicht überschreiben"
✅ "🚨 NIEMALS setup.py überschreiben! [Erklärung warum]"
```

#### Fehler 7: Erfolg nicht definieren

```markdown
❌ "Mach bis es funktioniert"
✅ "Erfolg = Installation + Commands + Tests alle ✅"
```

### Template: Dein eigener Arbeitsauftrag

Hier ist ein Template, das du nutzen kannst:

```markdown
# Arbeitsauftrag für [AI-Agent]: [Titel] (v[X])

**Phase:** [X] von [Y]  
**Ziel:** [Ein-Satz Beschreibung]  
**Kontext:** [Wo arbeitet der Agent? Was ist schon da?]

---

## 🎯 Ziel

[Detaillierte Beschreibung was erreicht werden soll]

**Warum?**
- [Grund 1]
- [Grund 2]

**Status:**
- [Was ist bereits gemacht]
- [Was ist die Ausgangslage]

---

## 📚 Referenz/Struktur

[Visual: Zeige die Ziel-Struktur oder das gewünschte Ergebnis]

**Quelle:** [Link zur Dokumentation]

---

## 🔧 Was zu tun ist

### Schritt 1: [Beschreibung]

[Wenn Code: Zeige den kompletten Code]
[Wenn Datei: Zeige den kompletten Inhalt]

**Warum dieser Schritt?** [Erklärung]

### Schritt 2: [Beschreibung]

[...]

---

## ✅ Test-Kriterien

### Lokal testen:
```bash
[Kommandos zum Testen]
```

### Must Have:
- [ ] [Kriterium 1]
- [ ] [Kriterium 2]

---

## 📋 Checkliste

- [ ] [Aufgabe 1]
- [ ] [Aufgabe 2]
- [ ] [...]

---

## 🚨 Wichtige Hinweise

1. **[Kritischer Punkt 1]**
2. **[Kritischer Punkt 2]**

---

## 🎯 Ziel dieser Phase

[Zusammenfassung was erreicht werden soll]

**Viel Erfolg!** 🚀
```

### Die drei Ebenen der Komplexität

Nicht jeder Auftrag braucht 500 Zeilen. Hier die drei Ebenen:

#### Ebene 1: Einfach (50-100 Zeilen)

**Für:** Kleine Änderungen, Bug-Fixes, einzelne Features

```markdown
# Arbeitsauftrag: Fix Typo in README

**Ziel:** Korrigiere Schreibfehler

## Was zu tun
Ändere "instalation" zu "installation" in README.md

## Test
README.md enthält "installation" ✓

## Checklist
- [ ] Typo gefixt
- [ ] Committed
```

#### Ebene 2: Mittel (100-300 Zeilen)

**Für:** Neue Features, mehrere Dateien, etwas Komplexität

```markdown
# Arbeitsauftrag: Neues Command hinzufügen

**Ziel:** ccb status Command

## Code
[Kompletter Code für status.py]

## Tests
[Test-Kommandos]

## Checklist
- [ ] status.py erstellt
- [ ] In main.py registriert
- [ ] Tests geschrieben
- [ ] Lokal getestet
```

#### Ebene 3: Komplex (300-500+ Zeilen)

**Für:** Neue Projekte, große Features, viele Dateien

```markdown
# Arbeitsauftrag: Komplettes neues Projekt

**Ziel:** [Detailliert]

## Struktur
[Visual Tree]

## Code
[15+ Dateien mit komplettem Code]

## Tests
[Umfangreiche Test-Suite]

## Checklist
[13+ Punkte]

## Warnungen
[Kritische Punkte]
```

**Die Regel:** Komplexität des Auftrags = Komplexität der Aufgabe

### Warum dieser Auftrag funktionierte

Unser Arbeitsauftrag v4 führte zu:

✅ **Code perfekt umgesetzt** - Struktur 100% korrekt  
✅ **Tests funktionieren** - Lokale Tests grün  
✅ **GitHub Actions grün** - CI/CD erfolgreich  
✅ **Keine Rückfragen nötig** - Alles war klar  
✅ **Zeitersparnis** - <30 Minuten Implementation  

**Warum?**

1. **Kompletter Code** - Keine Interpretation
2. **Klare Struktur** - Visual Tree
3. **Test-Kriterien** - Klares "Fertig"
4. **Kontext** - Warum erklärt
5. **Warnungen** - Kritisches hervorgehoben

### Zusammenfassung Kapitel 2

Was haben wir über Arbeitsaufträge gelernt?

#### Die Anatomie:
1. **Der Kopf** - Orientierung
2. **Das Warum** - Kontext
3. **Die Referenz** - Visualisierung
4. **Der Code** - Vollständig!
5. **Die Tests** - Messbar
6. **Die Checkliste** - Übersicht
7. **Die Warnungen** - Kritisches

#### Die Prinzipien:
1. **WAS vor WIE** - Ziel klar, Weg offen
2. **Show, don't tell** - Code zeigen
3. **Kontext ist König** - Warum erklären
4. **Test-getrieben** - Erfolg messbar
5. **Iteration** - Feedback & Anpassung

#### Die Ebenen:
- **Einfach:** 50-100 Zeilen
- **Mittel:** 100-300 Zeilen
- **Komplex:** 300-500+ Zeilen

#### Das Template:
Kopierbar, anpassbar, funktioniert.

#### Die wichtigste Erkenntnis:

**Ein guter Arbeitsauftrag ist wie ein guter Lehrer:**
- Klar in der Zielsetzung
- Reich an Kontext
- Zeigt statt beschreibt
- Definiert Erfolg
- Ermutigt Fragen

---

**Im nächsten Kapitel:** Cement v2 vs v3 - Warum ein "einfaches Update" zu einem Drama wurde, und was wir daraus über Breaking Changes gelernt haben.

---

*Ende von Kapitel 2*
