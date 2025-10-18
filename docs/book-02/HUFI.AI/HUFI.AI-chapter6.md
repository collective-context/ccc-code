# Kapitel 6 - Python pur: Arbeiten mit dem Cement Framework

## Von der Theorie zur Praxis - Ein Tag im Leben eines Cement v3 Projekts

### Das Framework, von dem niemand weiß

Frag zehn Python-Entwickler nach Cement. Neun werden dich fragend anschauen.

**"Cement? Nie gehört."**

Und doch: Über 10 Jahre alt. Battle-tested. Production-ready. Von Datafolklabs entwickelt. Genutzt in Enterprise-Software.

**Cement** ist das Framework, das keiner kennt - aber jeder gebrauchen könnte.

### Was ist Cement überhaupt?

**Die offizielle Beschreibung:**
> "A CLI application framework for Python."

**Die ehrliche Beschreibung:**
Ein Framework, um professionelle Command-Line Tools zu bauen. Mit allem was dazu gehört:
- Argument Parsing
- Logging
- Config Files
- Plugins
- Extensions
- Output Handlers
- Testing

**Think:** argparse + logging + configparser + ... auf Steroiden.

### Warum Cement?

Es gibt viele CLI-Frameworks für Python:
- Click
- Argparse (Standard Library)
- Docopt
- Typer

**Warum also Cement?**

#### Der Vergleich:

**argparse (Standard Library):**
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version')
parser.add_argument('command', choices=['info', 'help'])
args = parser.parse_args()

if args.command == 'info':
    print("My App v1.0")
elif args.command == 'help':
    print("Usage: ...")
```

**Problem:** Bei 10+ Commands wird das chaotisch.

**Click:**
```python
import click

@click.group()
def cli():
    pass

@cli.command()
def info():
    click.echo("My App v1.0")

@cli.command()
def help():
    click.echo("Usage: ...")
```

**Besser!** Aber: Keine Plugin-System, keine Extensions, keine Config-Files out-of-the-box.

**Cement:**
```python
from cement import App, Controller, ex

class Base(Controller):
    class Meta:
        label = 'base'
    
    @ex(help='show info')
    def info(self):
        print("My App v1.0")

class MyApp(App):
    class Meta:
        label = 'myapp'
        handlers = [Base]

with MyApp() as app:
    app.run()
```

**Vollständig!** Mit Logging, Config, Plugins, Extensions - alles dabei.

### Cement v2 vs v3: Ein Breaking Change

In unserem Projekt nutzen wir **beide Versionen**:
- **ccc/**: Cement v2.10.14
- **ccb/**: Cement v3.0.14

**Warum?** Kapitel 3 erklärt das Drama. Hier die technischen Details.

#### Import-Unterschiede:

**Cement v2:**
```python
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
```

**Cement v3:**
```python
from cement import App, Controller, ex
```

**Massiv vereinfacht!**

#### API-Unterschiede:

| Aspekt | v2 | v3 |
|--------|----|----|
| App Class | `CementApp` | `App` |
| Controller | `CementBaseController` | `Controller` |
| Decorator | `@expose` | `@ex` |
| Setup | `app.setup()` + `app.run()` | nur `app.run()` |

#### Das gleiche Tool in beiden Versionen:

**Cement v2 (ccc/):**
```python
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

class CCCBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'CCC CODE Tools'
    
    @expose(help='show version')
    def info(self):
        print(f'CCC CODE v{self.app.VERSION}')

class CCCApp(CementApp):
    class Meta:
        label = 'ccc'
        handlers = [CCCBaseController]

def main():
    with CCCApp() as app:
        app.setup()
        app.run()
```

**Cement v3 (ccb/):**
```python
from cement import App, Controller, ex

class Base(Controller):
    class Meta:
        label = 'base'
        description = 'CCB Tools'
    
    @ex(help='show version')
    def info(self):
        print(f'CCB v{self.app.VERSION}')

class CCBApp(App):
    class Meta:
        label = 'ccb'
        handlers = [Base]

def main():
    with CCBApp() as app:
        app.run()
```

**Die Logik:** Identisch.  
**Die API:** Komplett anders.

**Das ist "intentional breakage".**

### Der Tag, an dem __version__ fehlte

16. Oktober 2025, 14:30 Uhr. Wir hatten gerade ccb/ implementiert. Cement v3 nach Best Practices. Installation funktionierte. Dann der Test:

```bash
$ bash tests-ccb/travis.sh
```

Installation läuft durch. Cement installiert. Symlinks erstellt. Alles grün.

Dann:

```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
AttributeError: module 'ccb' has no attribute '__version__'
```

**Test fehlgeschlagen.**

### Das Problem: Python Conventions

Unser `ccb/__init__.py`:

```python
VERSION = '0.1.0'

def get_version():
    return VERSION
```

**Das Test-Script erwartet:**

```python
import ccb
print(ccb.__version__)  # AttributeError!
```

**Warum `__version__`?**

**Python Package Convention:**

Die meisten Python Packages haben:
```python
__version__ = '1.0.0'
```

**Warum?**

1. **setup.py kann darauf zugreifen:**
```python
from mypackage import __version__

setup(
    name='mypackage',
    version=__version__,
)
```

2. **Tools erwarten es:**
```bash
python3 -c "import mypackage; print(mypackage.__version__)"
```

3. **Es ist Standard:** PEP 396 empfiehlt `__version__`

### Die Lösung: Beide Conventions

**ccb/__init__.py (Fixed):**
```python
VERSION = '0.1.0'
__version__ = VERSION  # Python Standard Convention

def get_version():
    return VERSION
```

**Jetzt funktionieren beide:**
```python
import ccb

# Version 1: Unsere interne Funktion
print(ccb.get_version())  # '0.1.0'

# Version 2: Python Standard
print(ccb.__version__)     # '0.1.0'

# Version 3: Direkt
print(ccb.VERSION)         # '0.1.0'
```

**Alle drei Zugriffe funktionieren.**

### Was Aider-1 tat (ohne zu fragen)

DevOps übergab die Log-Datei. Aider-1:

1. **Analysierte** logs/ccb-test.log
2. **Erkannte** das Problem (`__version__` fehlt)
3. **Implementierte** den Fix (eine Zeile)
4. **Testete** erneut
5. **Committete**

**Keine Rückfrage. Keine Verzögerung.**

**Warum durfte er das?**

- ✅ Problem eindeutig (AttributeError)
- ✅ Lösung Standard-Praxis (Python Convention)
- ✅ Risiko minimal (eine Zeile)
- ✅ Kontext klar (Test schlägt fehl)

**Das ist selbstständiges Arbeiten.**

Nicht blind. Nicht unkontrolliert. **Professionell.**

### Die Cement Project-Struktur

Schauen wir uns an, wie ein sauberes Cement v3 Projekt aussieht:

```
ccb/                          # Hauptmodul
├── __init__.py              # VERSION + __version__
├── main.py                  # Entry Point
├── controllers/
│   ├── __init__.py
│   └── base.py              # Base Controller
├── core/
│   ├── __init__.py
│   ├── exc.py               # Custom Exceptions
│   └── version.py           # Version Helper
├── ext/                     # Extensions
│   └── __init__.py
├── plugins/                 # Plugins
│   └── __init__.py
└── templates/               # Templates
    └── .gitkeep
```

**Warum diese Struktur?**

#### Die Rolle jedes Verzeichnisses:

**ccb/__init__.py:**
- Package Marker
- Version exportieren
- Grundlegende Imports

**ccb/main.py:**
- App Definition
- Controller Registration
- Entry Point

**ccb/controllers/:**
- Alle Commands
- Gruppiert nach Funktionalität
- Base Controller für gemeinsame Funktionen

**ccb/core/:**
- Business Logic
- Helper Functions
- Custom Exceptions

**ccb/ext/:**
- Cement Extensions
- Custom Logging
- Custom Output Handlers

**ccb/plugins/:**
- Optionale Features
- Dynamisch ladbar
- Unabhängig voneinander

### Der Entry Point: main.py

Das Herz jeder Cement App:

```python
from cement import App, Controller, ex
from ccb.core.version import get_version

VERSION_BANNER = """
CCC Beta (ccb) v%s
Experimental tools for CCC CODE development
https://collective-context.org
""" % get_version()


class Base(Controller):
    """Base controller"""
    
    class Meta:
        label = 'base'
        description = 'CCB Tools'
        arguments = [
            (['-v', '--version'], {
                'action': 'version',
                'version': VERSION_BANNER
            }),
        ]
    
    def _default(self):
        """Default action (help)"""
        self.app.args.print_help()
    
    @ex(
        help='show version and info',
        description='Display version information'
    )
    def info(self):
        """Show info"""
        print(f'CCC Beta (ccb) v{get_version()}')
        print('Experimental tools for CCC CODE development')
        print('')
        print('Available commands:')
        print('  ccb info       - Show this information')
        print('  ccb --help     - Display help')
        print('  ccb --version  - Display version')


class CCB(App):
    """Main application"""
    
    class Meta:
        label = 'ccb'
        handlers = [Base]
        extensions = ['colorlog']
        log_handler = 'colorlog'
        plugin_dirs = ['ccb/plugins']


def main():
    """Main entry point"""
    with CCB() as app:
        try:
            app.run()
        except AssertionError as e:
            print(f'AssertionError: {e}')
            app.exit_code = 1
        except KeyboardInterrupt:
            print('\nInterrupted')
            app.exit_code = 130


if __name__ == '__main__':
    main()
```

### Die Meta Class: Cement's Konfiguration

Jede Cement Class hat eine `Meta` Inner-Class:

```python
class MyController(Controller):
    class Meta:
        label = 'base'           # Eindeutiger Name
        description = 'Tools'    # Beschreibung
        arguments = [...]        # CLI Arguments
        
class MyApp(App):
    class Meta:
        label = 'myapp'          # App Name
        handlers = [...]         # Controller
        extensions = [...]       # Extensions (colorlog, etc.)
        log_handler = '...'      # Logging
        plugin_dirs = [...]      # Plugin Verzeichnisse
```

**Das Meta-Pattern:**
- Alle Konfiguration in einer Inner-Class
- Klar getrennt von der Logik
- Übersichtlich und wartbar

### Der @ex Decorator: Commands definieren

In Cement v3:

```python
@ex(
    help='kurze Hilfe',
    description='lange Beschreibung',
    arguments=[
        (['-f', '--force'], {
            'action': 'store_true',
            'help': 'force operation'
        }),
    ]
)
def my_command(self):
    """Docstring"""
    # Command Logic
    pass
```

**Wird zu:**

```bash
$ ccb my-command --help
usage: ccb my-command [-h] [-f]

lange Beschreibung

optional arguments:
  -h, --help   show this help message and exit
  -f, --force  force operation
```

**Magic!** Cement generiert die CLI aus dem Decorator.

### Custom Exceptions: Saubere Fehlerbehandlung

**ccb/core/exc.py:**

```python
class CCBError(Exception):
    """Base exception"""
    pass


class CCBConfigError(CCBError):
    """Configuration error"""
    pass


class CCBRuntimeError(CCBError):
    """Runtime error"""
    pass
```

**Verwendung:**

```python
from ccb.core.exc import CCBConfigError

def load_config(path):
    if not path.exists():
        raise CCBConfigError(f"Config not found: {path}")
    
    # Load config
    return config
```

**Vorteile:**
- Klare Exception-Hierarchie
- Einfaches Catching
- Bessere Error Messages

### Plugin System: Erweiterbar by Design

Cement hat ein eingebautes Plugin-System:

**ccb/plugins/example.py:**

```python
from cement import Controller, ex

def load(app):
    """Plugin wird geladen"""
    pass


class Example(Controller):
    """Example plugin controller"""
    
    class Meta:
        label = 'example'
        stacked_on = 'base'  # Wird zu 'base' hinzugefügt
    
    @ex(help='example command')
    def example(self):
        print("This is an example plugin")
```

**Wird zu:**

```bash
$ ccb example
This is an example plugin
```

**Plugins:**
- Dynamisch ladbar
- Unabhängig voneinander
- Einfach zu entwickeln
- Production-ready

### Testing: Die vergessene Kunst

**tests-ccb/cli/test_ccb_commands.py:**

```python
import unittest
from ccb.main import CCB


class TestCCBCommands(unittest.TestCase):
    """Test CCB commands"""
    
    def setUp(self):
        """Setup test app"""
        self.app = CCB()
        self.app.setup()
    
    def tearDown(self):
        """Tear down test app"""
        self.app.close()
    
    def test_info_command(self):
        """Test info command"""
        with self.app as app:
            app.run(['info'])
            # Assert output
    
    def test_version_argument(self):
        """Test --version"""
        with self.assertRaises(SystemExit):
            with self.app as app:
                app.run(['--version'])


if __name__ == '__main__':
    unittest.main()
```

**Plus:** Bash-Tests für Integration-Testing.

**tests-ccb/travis.sh:**

```bash
#!/bin/bash

# Installation Test
echo "Testing installation..."
sudo -E bash install-ccb

# Binary Tests
echo "Testing ccb --version..."
ccb --version

echo "Testing ccb --help..."
ccb --help

echo "Testing ccb info..."
ccb info

echo "All tests passed!"
```

**Zwei Test-Ebenen:**
1. **Unit Tests** (Python) - Logik testen
2. **Integration Tests** (Bash) - Installation testen

### Setup & Installation: Das Python Package

**setup-ccb.py:**

```python
from setuptools import setup, find_packages

setup(
    name='ccb',
    version='0.1.0',
    description='CCC Beta Tools',
    packages=find_packages(),
    install_requires=[
        'cement>=3.0.0,<4.0.0',
        'colorlog',
    ],
    entry_points={
        'console_scripts': [
            'ccb=ccb.main:main',
        ],
    },
    python_requires='>=3.8',
)
```

**Was passiert bei `pip install`:**

1. **Packages finden:** `find_packages()` findet ccb/
2. **Dependencies installieren:** cement + colorlog
3. **Binary erstellen:** ccb → ccb.main:main()
4. **In PATH:** /usr/local/bin/ccb

**Ein Befehl:**
```bash
pip install -e .
```

**Ergebnis:**
```bash
$ ccb --version
CCC Beta (ccb) v0.1.0
```

### Real-World Lessons: Was wir lernten

#### Lesson 1: __version__ is Standard

**Immer beide:**
```python
VERSION = '1.0.0'
__version__ = VERSION
```

Tools erwarten `__version__`. Interne Funktionen nutzen `VERSION`.

#### Lesson 2: Meta Class is King

Alle Konfiguration in Meta:
```python
class Meta:
    label = 'base'
    description = '...'
    # Alles andere hier
```

Nicht im Constructor. Nicht in __init__. **In Meta.**

#### Lesson 3: Plugins später

Phase 1: Basis-Funktionalität  
Phase 2-4: Plugins hinzufügen

**Nicht umgekehrt.**

#### Lesson 4: Test lokal BEFORE Push

```bash
# IMMER vor git push:
bash tests-ccb/travis.sh

# Nur wenn ✅:
git push
```

CI/CD ist der finale Test. Lokale Tests sind Pflicht.

#### Lesson 5: Entry Point matters

**setup.py:**
```python
entry_points={
    'console_scripts': [
        'ccb=ccb.main:main',  # Format: command=module:function
    ],
}
```

**Muss matchen:**
- Binary name: `ccb`
- Module: `ccb.main`
- Function: `main()`

### Cement vs Click vs Typer: Der Vergleich

| Feature | Cement | Click | Typer |
|---------|--------|-------|-------|
| Plugins | ✅ Built-in | ❌ Selbst bauen | ❌ Selbst bauen |
| Config Files | ✅ Built-in | ❌ Selbst bauen | ❌ Selbst bauen |
| Logging | ✅ Built-in | ❌ Standard lib | ❌ Standard lib |
| Extensions | ✅ System | ❌ Nein | ❌ Nein |
| Templates | ✅ Built-in | ❌ Selbst bauen | ❌ Selbst bauen |
| Type Hints | ⚠️ Teilweise | ❌ Nein | ✅ Ja! |
| Learning Curve | ⚠️ Steiler | ✅ Flach | ✅ Flach |

**Wann Cement?**
- Enterprise CLI Tools
- Plugin-System nötig
- Config-Files wichtig
- Logging essentiell
- Extensions geplant

**Wann Click/Typer?**
- Schnelle Scripts
- Einfache Tools
- Type Hints wichtig (Typer)
- Minimale Dependencies

### Zusammenfassung Kapitel 6

Was haben wir über Cement gelernt?

#### Das Framework:
- Python CLI Framework
- 10+ Jahre alt
- Battle-tested
- Wenig bekannt, aber mächtig

#### v2 vs v3:
- Breaking Change
- API komplett anders
- Logik gleich
- Beide parallel nutzbar

#### Die Struktur:
```
__init__.py     - VERSION + __version__
main.py         - App + Controller
controllers/    - Commands
core/           - Business Logic
plugins/        - Extensions
```

#### Die Tools:
- @ex Decorator für Commands
- Meta Class für Config
- Plugin System eingebaut
- Testing Framework integriert

#### Die Lektionen:
1. `__version__` ist Standard
2. Meta Class ist König
3. Plugins später
4. Test lokal first
5. Entry Point muss matchen

#### Die wichtigste Erkenntnis:

**Cement ist nicht Click. Cement ist nicht Typer.**

Cement ist ein **Enterprise CLI Framework** mit allem was dazu gehört.

Für schnelle Scripts: Overkill.  
Für professionelle Tools: Perfect.

**WordOps nutzt Cement. CCC CODE nutzt Cement.**

Und jetzt weißt du warum.

---

**Im nächsten Kapitel:** Fehlerkultur in Mensch-KI-Teams - Wenn AI Agents Fehler machen (und Menschen auch), und wie wir daraus lernen.

---

*Ende von Kapitel 6*
