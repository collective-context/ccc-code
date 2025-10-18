# Kapitel 4: Das Vier-System-Modell

## Vier parallele Welten - Eine gemeinsame Mission

### Die ungewöhnliche Entscheidung

Die meisten Projekte haben:
- **Ein** Repository
- **Ein** Branch (main/master)
- **Ein** System

Wir haben:
- **Ein** Repository
- **Vier** komplette Systeme
- **Vier** parallele Installationen

**Warum?**

Das ist die Geschichte, wie eine ungewöhnliche Architektur-Entscheidung zum Erfolgsgeheimnis wurde.

### Der Anfang: Es war einmal ein Fork

Am Anfang war **WordOps**.

**WordOps** ist ein hervorragendes Tool:
- Verwaltet WordPress-Sites
- Nginx-Konfiguration
- SSL-Zertifikate
- Backup & Updates
- Production-ready

**Unsere Vision:** Multi-Agent KI-Orchestrierung

Also machten wir einen Fork: **CCC CODE** (Collective Context Commander)

Aber wie behält man das Original als Referenz UND entwickelt das Neue?

**Die Lösung:** Das Vier-System-Modell.

### Die vier Welten

```
Repository: ccc-code/
├── wo/          # WordOps Original (READ-ONLY)
├── ccc/         # CCC Production (AKTIV)
├── cca/         # CCC Alpha Test (RAPID)
└── ccb/         # CCC Beta Modern (EXPERIMENT)
```

Jedes System ist ein **komplettes, funktionsfähiges Programm**.

Jedes System kann **parallel installiert** werden:

```bash
wo --version    # WordOps 3.x
ccc --version   # CCC 3.x
cca --version   # CCA 3.x
ccb --version   # CCB 3.x
```

Vier Commands. Vier Programme. **Ein Repository.**

### System 1: wo/ - Das Original (READ-ONLY)

**Rolle:** Upstream-Referenz

**Zweck:**
- Original WordOps Code
- **NIEMALS ändern!**
- Dient als Vergleichs-Basis
- Upstream Updates einfach integrieren

**Installation:**
```bash
sudo -E bash install-wo
wo --version
```

**Typische Nutzung:**
```bash
# Updates von upstream holen
cd wo/
git pull upstream master

# Mit ccc/ vergleichen
diff wo/wordops/cli/main.py ccc/ccc/cli/main.py

# Best Practices lernen
vim wo/wordops/core/services.py
```

**Die goldene Regel:**
> **NIEMALS wo/ oder install-wo ändern!**

**Warum nicht?**
- Ermöglicht saubere upstream sync
- Vergleiche bleiben valide
- Kein Merge-Chaos

**Wenn WordOps einen wichtigen Fix hat:**
```bash
# In wo/:
git pull upstream master

# Relevante Changes identifizieren
git log --oneline -10

# Manuell zu ccc/ portieren
vim ccc/ccc/cli/main.py
```

### System 2: ccc/ - Production Fork (AKTIV)

**Rolle:** Production System

**Zweck:**
- Der "echte" Fork
- Multi-Agent Features
- Aktiv deployed
- Für End-User

**Installation:**
```bash
sudo -E bash install
ccc --version
```

**Typische Nutzung:**
```bash
# Features hinzufügen (aus cca/)
ccc agent add claude-max

# Production Operations
ccc site create example.com

# Monitoring
ccc info
```

**Entwicklungs-Flow:**
```
cca/ → test in cca/ → wenn stabil → port zu ccc/ → deploy
```

**API Version:** Cement v2.10.14

**Stabilität:** HOCH (production-grade)

**Updates:**
- Von wo/ (upstream fixes)
- Von cca/ (neue features)

### System 3: cca/ - Alpha Lab (RAPID PROTOTYPING)

**Rolle:** Test-Labor für neue Features

**Zweck:**
- Schnelles Experimentieren
- Minimale Struktur
- Cement v2 (gleiche API wie ccc/)
- Features testen vor ccc/

**Installation:**
```bash
sudo -E bash install-cca
cca --version
```

**Typische Nutzung:**
```bash
# Neues Feature entwickeln
vim cca/cca/controllers/agent.py

# Lokal testen
cca agent list

# Wenn gut → zu ccc/ portieren
```

**Warum cca/?**

**Problem:**
```
Direkt in ccc/ entwickeln = Risiko
Jeder Bug geht live
Jeder Test ist öffentlich
```

**Lösung:**
```
In cca/ entwickeln = Safe
Tests in cca/
Bugs nur in cca/
Wenn stabil → ccc/
```

**API Kompatibilität:**
```python
# cca/ und ccc/ nutzen gleiche Cement API
from cement import App, Controller, ex

# Code läuft 1:1 in beiden!
class AgentController(Controller):
    @ex(help="list agents")
    def list(self):
        # Works in both cca/ and ccc/
```

**Der Vorteil:** Direkter Transfer von cca/ → ccc/

### System 4: ccb/ - Beta Future (EXPERIMENT)

**Rolle:** Zukunfts-Labor

**Zweck:**
- Cement v3 lernen
- Moderne Patterns testen
- Experimentelles System
- Nicht für ccc/ nutzbar (Breaking Changes!)

**Installation:**
```bash
sudo -E bash install-ccb
ccb --version
```

**Typische Nutzung:**
```bash
# v3 Features erkunden
vim ccb/ccb/main.py

# Moderne Patterns lernen
ccb --help

# Für NEUE Projekte vormerken
```

**Warum ccb/?**

**Nach Kapitel 3 (Breaking Changes) wurde klar:**

```
Cement v2 → v3 = NEUSTART
Nicht upgrade-bar
Breaking Changes überall
```

**Alte Strategie:**
```
ccb/ → ccc/ Migration
✗ Funktioniert nicht
```

**Neue Strategie:**
```
ccb/ = Lern-Labor für v3
cca/ = Test-Labor für ccc/
✓ Beide nützlich, unterschiedliche Rollen
```

**API Beispiel:**
```python
# ccc/cca/ (v2)
from cement import App, Controller, ex

# ccb/ (v3) - KOMPLETT ANDERS
from cement import App
from cement import Controller, ex
# Unterschiedliche Struktur!
```

**Langfristige Vision:**
- ccc/ bleibt v2 (stabil)
- ccb/ exploriert v3 (modern)
- Bei Bedarf: NEUE Projekte in v3
- Migration nur wenn Business-Sinn

### Die Interaktionen: Wie sie zusammenspielen

```
┌─────────────────────────────────────────────┐
│                                             │
│   wo/ (Upstream)                            │
│   └─→ Updates → ccc/                        │
│                                             │
└─────────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────┐
│                                             │
│   ccc/ (Production)                         │
│   ├─← Features ← cca/                       │
│   └─→ Learning → ccb/                       │
│                                             │
└─────────────────────────────────────────────┘
         ↑                       │
         │                       ↓
┌──────────────────┐    ┌──────────────────┐
│                  │    │                  │
│  cca/ (Test)     │    │  ccb/ (Future)   │
│  Cement v2       │    │  Cement v3       │
│                  │    │                  │
└──────────────────┘    └──────────────────┘
```

#### Flow 1: Upstream Updates (wo/ → ccc/)

```bash
# 1. WordOps released neuen Fix
cd wo/
git pull upstream master

# 2. Relevanten Code identifizieren
git log -p

# 3. Zu ccc/ portieren
vim ccc/ccc/cli/main.py
# Copy concept, adapt names

# 4. Testen
ccc --version

# 5. Commit
git add ccc/
git commit -m "feat(ccc): port upstream fix from wo/"
```

#### Flow 2: Feature Development (cca/ → ccc/)

```bash
# 1. Prototyp in cca/
vim cca/cca/controllers/agent.py
class AgentController(Controller):
    @ex(help="add agent")
    def add(self):
        print("Add agent")

# 2. Test in cca/
cca agent add
# Funktioniert!

# 3. Port zu ccc/
cp cca/cca/controllers/agent.py ccc/ccc/controllers/agent.py
vim ccc/ccc/controllers/agent.py
# Adapt if needed

# 4. Test in ccc/
ccc agent add
# Funktioniert!

# 5. Deploy
git add ccc/
git commit -m "feat(ccc): add agent controller"
```

#### Flow 3: Learning (alle → ccb/)

```bash
# Von wo/ lernen
cd wo/
vim wordops/cli/main.py
# → "So macht WordOps CLI args!"

# In ccb/ anwenden
cd ccb/
vim ccb/main.py
# → Modernes Pattern mit v3 API

# Dokumentieren
vim docs/learnings.md
# → "v3 Patterns aus wo/ gelernt"
```

### Praxis-Beispiel: Ein Feature entwickeln

Lass uns ein echtes Beispiel durchgehen:

**Ziel:** GitHub Actions Integration

```bash
ccc check actions  # Zeigt aktuelle Workflow-Runs
```

#### Phase 1: Prototyp in cca/ (Tag 1-2)

```bash
# Neue Controller-Klasse
vim cca/cca/controllers/check.py

from cement import Controller, ex
import subprocess

class CheckController(Controller):
    class Meta:
        label = 'check'

    @ex(help="check github actions status")
    def actions(self):
        result = subprocess.run(
            ['gh', 'run', 'list', '--limit=5'],
            capture_output=True
        )
        print(result.stdout.decode())
```

**Test:**
```bash
cca check actions
# ✅ Funktioniert lokal
```

#### Phase 2: Tests schreiben (Tag 2)

```bash
vim tests-cca/test_check.sh

# Test script
cca check actions | grep -q "workflow"
if [ $? -eq 0 ]; then
    echo "✅ check actions works"
else
    echo "❌ check actions failed"
    exit 1
fi
```

#### Phase 3: Port zu ccc/ (Tag 3)

```bash
# Code übertragen
cp cca/cca/controllers/check.py ccc/ccc/controllers/check.py

# In ccc/ registrieren
vim ccc/ccc/main.py

# Controller laden
from ccc.controllers.check import CheckController

class CCC(App):
    class Meta:
        handlers = [
            Base,
            CheckController,  # ← NEU
        ]
```

**Test in ccc/:**
```bash
ccc check actions
# ✅ Funktioniert!
```

#### Phase 4: GitHub Actions Test (Tag 3)

```yaml
# .github/workflows/test-ccc.yml
- name: Test check plugin
  run: ccc check actions
```

**Push → GitHub Actions → GREEN ✅**

#### Phase 5: Documentation (Tag 4)

```markdown
# README.md
## New Feature: GitHub Actions Integration

```bash
ccc check actions  # View latest workflow runs
```
```

#### Das Ergebnis:

```
Tag 1-2: Prototyp in cca/ (schnell, minimal)
Tag 3: Port zu ccc/ (production-ready)
Tag 3: CI/CD Test (GitHub Actions green)
Tag 4: Dokumentiert

GESAMT: 4 Tage von Idee zu Production
```

**Das Vier-System-Modell macht es möglich:**
- cca/ = Schnelles Prototyping
- ccc/ = Production Deployment
- wo/ = Nicht betroffen (bleibt stabil)
- ccb/ = Lernt für Zukunft

---

### Die Vorteile des Vier-System-Modells

#### Vorteil 1: Risikofreies Experimentieren

**Problem gelöst:**
```
"Wie teste ich neue Features ohne Production zu gefährden?"
```

**Lösung:**
```
cca/ = Experimentier-Sandkasten
→ Kein Production-Impact
→ Schnelles Iterieren
→ Wenn stabil → ccc/
```

#### Vorteil 2: Kontinuität mit Upstream

**Problem gelöst:**
```
"Wie halte ich meinen Fork synchron mit dem Original?"
```

**Lösung:**
```
wo/ = Saubere Original-Kopie
→ Updates easy portierbar
→ Vergleich jederzeit möglich
→ Best Practices lernen
```

#### Vorteil 3: Technologie-Parallelität

**Problem gelöst:**
```
"Wie nutze ich v2 UND lerne v3, ohne Migration-Zwang?"
```

**Lösung:**
```
cca/ccc/ = v2 (production-stable)
ccb/ = v3 (learning lab)
→ Beide nutzbar
→ Migration optional
→ Kein Druck
```

#### Vorteil 4: Klare Rollen & Verantwortlichkeiten

**Problem gelöst:**
```
"Welches System ist für was zuständig?"
```

**Lösung:**
```
wo/  = Referenz (READ-ONLY)
ccc/ = Production (AKTIV)
cca/ = Testing (RAPID)
ccb/ = Future (LEARN)
→ Keine Verwirrung
→ Jeder weiß seine Rolle
```

#### Vorteil 5: Didaktischer Wert

**Problem gelöst:**
```
"Wie lernt ein neuer Entwickler das System?"
```

**Lösung:**
```
1. Studiere wo/ (das Original)
2. Verstehe ccc/ (die Production)
3. Experimentiere in cca/ (minimal)
4. Lerne ccb/ (die Zukunft)
→ Stufenweises Lernen
```

---

### Die Herausforderungen (ehrlich gesagt)

Nicht alles ist perfekt. Hier sind die Herausforderungen:

#### Herausforderung 1: Komplexität

**Vier Systeme = Vier Mal Wartung**

```bash
# Bug in allen Systemen?
vim wo/  # Nein, READ-ONLY
vim ccc/ # Fix hier
vim cca/ # Auch hier?
vim ccb/ # Und hier?
```

**Mitigation:**
- wo/ wird nicht gewartet (upstream)
- ccc/ ist Primary
- cca/ und ccb/ sind optional

#### Herausforderung 2: Synchronisation

**Wie hält man alles synchron?**

```
wo/ updated → ccc/ muss folgen
cca/ Feature → ccc/ portieren
ccb/ Learning → dokumentieren
```

**Mitigation:**
- Klare Prozesse
- Gute Dokumentation (.init-project.md)
- GitHub Actions als Safety Net

#### Herausforderung 3: Verwirrung für Neue

**Neue Entwickler:** "Warum vier Systeme?!"

**Mitigation:**
- Diese Dokumentation
- .init-project.md IMMER lesen
- Stufenweises Onboarding:
  1. Verstehe wo/
  2. Nutze ccc/
  3. Experimentiere cca/
  4. Optional: ccb/

#### Herausforderung 4: Setup Jonglieren

**Zwei setup.py Files:**

```
setup.py     → cca/ccc/wo/ (v2)
setup-ccb.py → ccb/ (v3)
```

**Problem:** Installation muss richtige setup.py nutzen

**Mitigation:**
- Klare Naming (setup-ccb.py)
- Install-Scripts handhaben automatisch
- Dokumentation

---

### Best Practices für das Vier-System-Modell

#### Best Practice 1: Klare Namenskonvention

```
wo    → Original
ccc   → Production
cca   → Alpha
ccb   → Beta

install-wo
install     (für ccc)
install-cca
install-ccb

tests-wo/
tests/      (für ccc)
tests-cca/
tests-ccb/
```

**Warum:** Sofort klar, welches System gemeint ist

#### Best Practice 2: Rollen dokumentieren

```markdown
# .init-project.md

## Die vier Systeme

| System | Rolle | Ändern? |
|--------|-------|---------|
| wo/    | Referenz | NIEMALS |
| ccc/   | Production | JA |
| cca/   | Test | JA |
| ccb/   | Experiment | JA |
```

**Warum:** Neue Entwickler verstehen sofort die Architektur

#### Best Practice 3: Migrations-Flow definieren

```bash
# Feature-Flow
cca/ → test → ccc/ → deploy

# Update-Flow
wo/ → analyze → ccc/ → adapt

# Learning-Flow
wo/ccb/ → learn → document
```

**Warum:** Jeder weiß, wie Features entwickelt werden

#### Best Practice 4: Tests für alle

```yaml
# .github/workflows/
test-wo.yml
test-ccc.yml
test-cca.yml
test-ccb.yml
```

**Warum:** Alle Systeme müssen funktionieren

#### Best Practice 5: Separat commiten

```bash
# ❌ NICHT:
git add wo/ ccc/ cca/ ccb/
git commit -m "update all"

# ✅ SONDERN:
git add cca/
git commit -m "feat(cca): new agent controller"

git add ccc/
git commit -m "feat(ccc): port agent controller from cca"
```

**Warum:** Klare Commit-Historie, einfaches Rollback

---

### Die Installation-Matrix

Wie installiert man alle vier Systeme? Hier die Schritt-für-Schritt Anleitung:

#### Schritt 1: WordOps Original (Referenz)

```bash
wget -qO wo https://raw.githubusercontent.com/.../install-wo
sudo -E bash wo
wo --version  # Prüfen
```

**Warum als erstes?** Das Original als Basis verstehen.

#### Schritt 2: CCC CODE (Production)

```bash
wget -qO ccc https://raw.githubusercontent.com/.../install
sudo -E bash ccc
ccc --version  # Prüfen
```

**Warum als zweites?** Die Production-Version verstehen.

#### Schritt 3: CCA Alpha (Test-Labor)

```bash
wget -qO cca https://raw.githubusercontent.com/.../install-cca
sudo -E bash cca
cca --version  # Prüfen
```

**Warum als drittes?** Minimales v2 Labor für Experimente.

#### Schritt 4: CCB Beta (Zukunfts-Labor)

```bash
wget -qO ccb https://raw.githubusercontent.com/.../install-ccb
sudo -E bash ccb
ccb --version  # Prüfen
```

**Warum zuletzt?** Das experimentelle v3 System.

#### Verification: Alle vier laufen

```bash
wo --version && \
ccc --version && \
cca --version && \
ccb --version

# Alle vier sollten ihre Version zeigen!
```

---

### Zusammenfassung Kapitel 4

Was haben wir über das Vier-System-Modell gelernt?

#### Die vier Welten:

| System | API | Rolle | Zweck |
|--------|-----|-------|-------|
| **wo/** | v2 | READ-ONLY | Original-Referenz |
| **ccc/** | v2 | AKTIV | Production Fork |
| **cca/** | v2 | TEST | Rapid Prototyping |
| **ccb/** | v3 | EXPERIMENT | Zukunfts-Labor |

#### Die Flows:

```
wo/ → ccc/         (Updates)
cca/ → ccc/        (Features)
ccc/ → ccb/        (Learning)
wo/ ↔ alle         (Reference)
```

#### Die Vorteile:

1. **Risikofreies Experimentieren** (cca/)
2. **Upstream Synchronität** (wo/)
3. **Technologie-Parallelität** (v2 + v3)
4. **Klare Rollen** (jeder kennt seinen Platz)
5. **Didaktischer Wert** (stufenweises Lernen)

#### Die Herausforderungen:

1. Komplexität (vier Systeme)
2. Synchronisation (konsistent halten)
3. Verwirrung (für Neue)
4. Setup-Jonglieren (setup.py vs setup-ccb.py)

#### Die Best Practices:

1. ✅ Klare Namenskonvention
2. ✅ Rollen dokumentieren (.init-project.md)
3. ✅ Migrations-Flow definieren
4. ✅ Tests für alle Systeme
5. ✅ Separat commiten

#### Die wichtigste Erkenntnis:

**Vier parallele Systeme sind nicht Komplexität - sie sind Klarheit.**

Jedes System hat eine Rolle. Jeder weiß, wo was hingehört. Features fließen strukturiert von cca/ → ccc/. Updates fließen von wo/ → ccc/. Learning fließt von ccb/ → Dokumentation.

**Das ist nicht Chaos. Das ist Orchestrierung.**

---

**Im nächsten Kapitel:** GitHub Actions - Wenn CI/CD zum Lernwerkzeug wird, und wie tagelange rote Builds uns bessere Entwickler machten.

---

*Ende von Kapitel 4*
