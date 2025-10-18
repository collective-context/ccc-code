# Kapitel 7: Wenn das Terminal lebendig wird

## TUI - Die Renaissance der Text-Interfaces

### Der Moment der Erkenntnis

Es war ein ganz normaler Tag. DevOps tippte Befehle:

```bash
ccc site list
ccc agent add --name claude-max
ccc config set debug true
```

Funktional? **Ja.**
Übersichtlich? **Naja.**
Intuitiv? **Nicht wirklich.**

DevOps:
> *"Weißt du was? Für ein Setup mit 20 Optionen wäre ein Menü besser. So wie früher in den 90ern - diese ncurses-Dialoge. Erinnerst du dich?"*

Claude-MAX (ich):
> *"Du meinst eine TUI? Text User Interface? Ja, das wäre tatsächlich besser für interaktive Setups..."*

DevOps:
> *"Genau! Aber keine alten curses-Dialoge. Etwas Modernes. Mit Farben, Widgets, vielleicht sogar Maus-Support. Und es sollte mit Cement funktionieren."*

**Und so begann die Reise in die Welt der modernen TUIs.**

---

### Was ist eine TUI überhaupt?

#### Die drei UI-Welten

**GUI (Graphical User Interface)**
```
┌─────────────────────────┐
│  ● ○ ○   Meine App      │
├─────────────────────────┤
│ [Datei] [Bearbeiten]    │
│                         │
│  ┌──────────────────┐   │
│  │ Klick mich!      │   │
│  └──────────────────┘   │
│                         │
└─────────────────────────┘
```
- Windows, Buttons, Mäuse
- Pixel-basiert
- Ressourcen-intensiv

**CLI (Command Line Interface)**
```bash
$ ccc site list
site1.com
site2.com

$ ccc agent add --name test
Agent added successfully
```
- Nur Text und Befehle
- Kein visuelles Feedback
- Für Profis

**TUI (Text User Interface)**
```
┌─────────────────────────┐
│ CCC Setup Menü          │
├─────────────────────────┤
│ [X] Enable Debug        │
│ [ ] Auto-Update         │
│ [ ] Verbose Logging     │
│                         │
│ [  Speichern  ] [Cancel]│
└─────────────────────────┘
```
- Text-basiert ABER visuell
- Widgets, Navigation, Interaktion
- Läuft im Terminal
- Best of both worlds!

#### Warum TUI in 2025?

**Die Vorteile:**

1. **Lightweight**
   - Keine GUI-Frameworks nötig
   - Läuft auf Server ohne X11
   - Minimal RAM/CPU Nutzung

2. **SSH-fähig**
   ```bash
   ssh user@server
   ccc setup --interactive
   # → TUI läuft über SSH!
   ```

3. **Cross-Platform**
   - Linux ✅
   - macOS ✅
   - Windows ✅
   - Sogar Raspberry Pi ✅

4. **Moderne Features**
   - Farben (16.7 Millionen!)
   - Maus-Support
   - Animationen
   - CSS-ähnliches Styling

5. **Für Admins perfekt**
   - Server ohne GUI
   - Schneller als Web-UI
   - Terminal-freundlich
   - Automatisierbar (falls nötig CLI)

---

### Die TUI-Landschaft 2025

Es gibt viele TUI-Frameworks für Python:

#### Die Klassiker

**Curses** - Die Uralt-Bibliothek
```python
import curses

def main(stdscr):
    stdscr.addstr(0, 0, "Hello")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

**Probleme:**
- Low-level (viel Boilerplate)
- Windows-Support mangelhaft
- Keine Widgets
- Code ist... hässlich

**Urwid** - Der Veteran (seit ~2004)
```python
import urwid

txt = urwid.Text("Hello World")
fill = urwid.Filler(txt, 'top')
loop = urwid.MainLoop(fill)
loop.run()
```

**Vorteile:**
- Bewährt und stabil
- Viele Widgets
- Gute Doku

**Nachteile:**
- Sync-only (kein async)
- Altbackenes API
- Kein CSS-Styling

#### Die Modernen

**Rich** - Der Schöngeist
```python
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Users")
table.add_column("Name")
table.add_row("Alice")
console.print(table)
```

**Gut für:**
- Schöne Outputs
- Logs, Tabellen, Progress-Bars
- Einfache Anzeigen

**NICHT gut für:**
- Komplexe interaktive UIs
- Event-Handling
- Forms

**Textual** - Der Champion (2025)
```python
from textual.app import App
from textual.widgets import Button, Input

class MyApp(App):
    def compose(self):
        yield Input(placeholder="Name...")
        yield Button("OK")

MyApp().run()
```

**Darum gewinnt Textual:**
- Modern (2021 gestartet)
- **Async-first** (asyncio!)
- CSS-ähnliches Styling
- React-ähnliche Components
- **Web-Browser Support** (!)
- Aktiv entwickelt
- Textualize.io backed
- Große Community

---

### Warum wir Textual wählen

Für CCC CODE haben wir uns für **Textual** entschieden. Hier ist warum:

#### Grund 1: Modern & Async

```python
# Cement ist modern (2025)
# Python 3.12 ist modern
# Async/await ist Standard

# Textual passt perfekt:
from textual.app import App

class SetupApp(App):
    async def on_mount(self):
        # Async von Anfang an!
        await self.load_config()
```

**Alter Tech Stack:**
```
Curses → Sync → Blocking → Alt
```

**Neuer Tech Stack:**
```
Textual → Async → Non-blocking → Modern
```

#### Grund 2: CSS-Styling (!)

Ja, du hast richtig gelesen. **CSS. Im Terminal.**

```python
# setup_app.tcss
Screen {
    background: #1e1e1e;
}

Button {
    width: 20;
    height: 3;
    background: #0078d4;
    color: white;
}

Button:hover {
    background: #106ebe;
}
```

**Warum das genial ist:**
- Designer können Themes erstellen
- Kein Python-Code für Styles
- Separation of Concerns
- Easy to customize

#### Grund 3: Web-Browser Support (!!)

**Das ist der Game-Changer.**

```bash
# Normal: Im Terminal
python ccc-setup.py

# Magic: Im Browser
textual serve ccc-setup.py
```

Dann öffnest du: **http://localhost:8000**

**Und siehst die GLEICHE App. Im Browser. Ohne Änderung.**

```
         Terminal                    Browser
┌─────────────────────┐     ┌─────────────────────┐
│ $ textual serve     │────▶│ http://localhost    │
│   app.py            │     │                     │
│                     │     │ [Same UI, HTML!]    │
│ ┌─────────────────┐ │     │ ┌─────────────────┐ │
│ │ [X] Option 1    │ │     │ │ [X] Option 1    │ │
│ │ [ ] Option 2    │ │     │ │ [ ] Option 2    │ │
│ └─────────────────┘ │     │ └─────────────────┘ │
└─────────────────────┘     └─────────────────────┘
```

**Ein Code. Zwei Interfaces. Zero Extra Work.**

#### Grund 4: React-ähnliche API

Wenn du Modern Web Development kennst, fühlst sich Textual vertraut an:

```python
# Textual (Python)
class MyApp(App):
    def compose(self):
        yield Header()
        yield Container(
            Button("Click me"),
            Input(placeholder="Name..."),
        )
        yield Footer()

# React (JavaScript)
function MyApp() {
    return (
        <div>
            <Header />
            <Container>
                <Button>Click me</Button>
                <Input placeholder="Name..." />
            </Container>
            <Footer />
        </div>
    );
}
```

**Ähnliche Konzepte:**
- Components / Widgets
- Compose / Render
- Props / Reactive attributes
- Events / Handlers
- State Management

#### Grund 5: Batteries Included

Textual kommt mit allem:

```python
from textual.widgets import (
    Button,          # Klickbar
    Input,           # Text eingeben
    Checkbox,        # An/Aus
    Switch,          # Toggle
    Select,          # Dropdown
    DataTable,       # Tabelle
    Tree,            # Hierarchie
    ProgressBar,     # Fortschritt
    Label,           # Text
    Header,          # Oben
    Footer,          # Unten
    # ... und mehr
)
```

**Alles was man braucht. Out of the box.**

---

### Cement + Textual: Die Integration

Jetzt das Wichtigste: **Wie verbinden wir Textual mit Cement?**

#### Pattern 1: Controller-Integration (Recommended)

```python
# ccc/controllers/setup.py
from cement import Controller, ex
from textual.app import App
from textual.widgets import Button, Input, Checkbox

class SetupTUI(App):
    """Die Textual App"""
    
    CSS = """
    Screen {
        align: center middle;
    }
    
    Button {
        margin: 1;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.result = {}
    
    def compose(self):
        yield Input(placeholder="Project Name", id="name")
        yield Checkbox("Enable Debug", id="debug")
        yield Checkbox("Auto-Update", id="update")
        yield Button("Save & Exit", id="save")
    
    def on_button_pressed(self, event):
        if event.button.id == "save":
            # Werte sammeln
            self.result = {
                'name': self.query_one("#name").value,
                'debug': self.query_one("#debug").value,
                'update': self.query_one("#update").value,
            }
            self.exit(self.result)

class SetupController(Controller):
    """Der Cement Controller"""
    
    class Meta:
        label = 'setup'
        stacked_on = 'base'
        description = 'CCC Setup'
    
    @ex(
        help='interactive setup (TUI)',
        arguments=[
            (['-i', '--interactive'],
             {'action': 'store_true',
              'help': 'use TUI instead of CLI'})
        ]
    )
    def run(self):
        if self.app.pargs.interactive:
            # TUI starten
            tui = SetupTUI()
            config = tui.run()
            
            # Config speichern
            self.app.config.set('ccc', 'name', config['name'])
            self.app.config.set('ccc', 'debug', config['debug'])
            
            self.app.log.info(f"Setup complete: {config}")
        else:
            # CLI-Modus
            print("Use --interactive for TUI setup")
```

**Nutzung:**
```bash
# CLI-Modus (klassisch)
ccc setup run --name myproject --debug

# TUI-Modus (interaktiv)
ccc setup run --interactive
```

#### Pattern 2: Separater Command

```python
class SetupController(Controller):
    class Meta:
        label = 'setup'
    
    @ex(help='CLI setup')
    def cli(self):
        # Klassische CLI-Flags
        pass
    
    @ex(help='TUI setup')
    def tui(self):
        # Textual App starten
        app = SetupTUI()
        app.run()
```

**Nutzung:**
```bash
ccc setup cli --flags...   # CLI
ccc setup tui              # TUI
```

#### Pattern 3: Hybrid mit Auto-Detection

```python
@ex(help='smart setup')
def run(self):
    # Terminal interaktiv?
    if sys.stdin.isatty() and not self.app.pargs.no_tui:
        # TUI
        SetupTUI().run()
    else:
        # CLI (für Scripts/Automation)
        self.cli_setup()
```

**Intelligent:**
```bash
ccc setup run              # → TUI (wenn Terminal)
ccc setup run --no-tui     # → CLI (forced)
echo "yes" | ccc setup run # → CLI (auto-detected)
```

---

### Die Web-UI Option: Ein Code, Zwei Welten

Das Killer-Feature von Textual: **Web-Browser Support**

#### Wie funktioniert das?

**Traditioneller Weg:**
```
Python App → REST API → JavaScript Frontend → Browser
             (Backend)   (separater Code!)     
```

**Textual Weg:**
```
Python App → Textual Serve → Browser
             (GLEICHER Code!)
```

#### Setup: Zero Änderungen nötig

```python
# ccc_setup.py
from textual.app import App
from textual.widgets import Button, Input

class CCCSetup(App):
    def compose(self):
        yield Input(placeholder="Site Name")
        yield Button("Create Site")
    
    def on_button_pressed(self):
        # Business Logic
        site_name = self.query_one(Input).value
        create_site(site_name)

if __name__ == "__main__":
    app = CCCSetup()
    app.run()
```

**Das war's. Dieser Code läuft überall.**

#### Terminal-Mode

```bash
python ccc_setup.py
```

```
┌─────────────────────────┐
│ CCC Setup               │
├─────────────────────────┤
│ ┌─────────────────────┐ │
│ │ Site Name...        │ │
│ └─────────────────────┘ │
│                         │
│   [ Create Site ]       │
└─────────────────────────┘
```

#### Browser-Mode

```bash
textual serve ccc_setup.py
```

```
Server running on http://localhost:8000
```

Browser öffnen:

```
┌─────────────────────────┐
│ http://localhost:8000   │
├─────────────────────────┤
│ CCC Setup               │
├─────────────────────────┤
│ ┌─────────────────────┐ │
│ │ Site Name...        │ │
│ └─────────────────────┘ │
│                         │
│   [ Create Site ]       │
└─────────────────────────┘
```

**Sieht identisch aus. IST identisch. Gleicher Python-Code!**

#### Wie ist das möglich?

**Technisch:**

```
Python App (Textual)
      ↓
   Rendering
      ↓
  ┌───┴───┐
  │       │
Terminal  Browser
  │       │
ANSI    WebSocket
Codes   + HTML/CSS
```

**Textual macht:**
1. Rendert die UI-Komponenten
2. Terminal: Sendet ANSI Escape Codes
3. Browser: Sendet HTML/CSS über WebSocket
4. Events (Klicks, Input) werden zurückgesendet
5. App reagiert (gleiche Event-Handler!)

**Du schreibst nur Python. Textual handled den Rest.**

#### Use Cases für Web-Mode

**1. Remote Management**
```bash
# Auf Server
textual serve ccc-setup.py --host 0.0.0.0 --port 8000

# Von Laptop
# Browser → http://server-ip:8000
# → Manage Server über Web!
```

**2. Team Collaboration**
```bash
# DevOps startet Setup
textual serve ccc-setup.py

# Team-Member verbinden sich
http://server:8000
```

**3. Demos & Präsentationen**
```bash
# Zeigen ohne SSH
textual serve --host 0.0.0.0
# → Audience kann in Browser folgen!
```

**4. Mobile Access (!)**
```bash
# Handy-Browser → Server-Setup
# Touch-freundlich!
```

#### Einschränkungen (ehrlich gesagt)

**Nicht alles funktioniert 1:1:**

1. **Maus vs. Touch**
   - Terminal: Maus-Klicks
   - Browser: Touch-Events
   - Meist OK, manchmal weird

2. **Keyboard Shortcuts**
   - Terminal: Alle Keys
   - Browser: Manche sind Browser-Shortcuts
   - Ctrl+W schließt Tab statt TUI-Action

3. **Performance**
   - Terminal: Nativ, schnell
   - Browser: WebSocket, etwas Latency
   - Bei LAN: kaum spürbar
   - Bei WAN: merkbar

4. **Copy & Paste**
   - Terminal: Native Terminal-Funktion
   - Browser: Browser-Context
   - Unterschiedlich

**Aber:** Für 90% der Use Cases ist es perfekt!

---

### Ein praktisches Plug-and-Play Beispiel

Bevor wir zum großen Site Creator kommen, lass uns mit etwas Einfachem starten: **Ein Setup-Menü, das direkt funktioniert.**

Du kannst diesen Code nehmen, in dein Projekt kopieren, und sofort loslegen. Kein Schnickschnack, nur funktionierender Code.

#### Das Setup-TUI: Schritt für Schritt

```python
# app.py - Dein komplettes Cement + Textual Setup
from cement import App, Controller, ex
from textual.app import App as TUIApp
from textual.widgets import Input, Checkbox, Button, Header, Footer
from textual.containers import Container

class SetupTUI(TUIApp):
    """Textual TUI für Setup – Ready to use!"""
    
    CSS = """
    Screen { 
        background: #1e1e1e; 
    }
    
    Container { 
        width: 50; 
        border: solid #0078d4; 
        padding: 1; 
    }
    
    Button { 
        margin: 1; 
        background: #0078d4; 
        color: white; 
    }
    
    Button:hover { 
        background: #106ebe; 
    }
    """

    def __init__(self, cement_app):
        super().__init__()
        self.cement_app = cement_app  # Cement-Instanz speichern
        self.result = {}

    def compose(self):
        """UI aufbauen"""
        yield Header()
        with Container():
            yield Input(placeholder="Projekt-Name", id="name")
            yield Checkbox("Debug aktivieren", id="debug", value=True)
            yield Checkbox("Auto-Update", id="update")
            yield Button("Speichern", id="save")
        yield Footer()

    def on_button_pressed(self, event):
        """Button-Click Handler"""
        if event.button.id == "save":
            # Werte aus Widgets holen
            self.result = {
                'name': self.query_one("#name").value,
                'debug': self.query_one("#debug").value,
                'update': self.query_one("#update").value
            }
            # TUI beenden und Ergebnis zurückgeben
            self.exit(self.result)

class SetupController(Controller):
    """Cement Controller für Setup"""
    
    class Meta:
        label = 'setup'
        description = 'Interaktives Setup'

    @ex(
        help='Starte Setup (CLI oder TUI)',
        arguments=[
            (['--interactive', '-i'],
             {'action': 'store_true',
              'help': 'TUI statt CLI'})
        ]
    )
    def run(self):
        if self.app.pargs.interactive:
            # TUI-Modus
            print("Starte interaktives Setup...")
            
            tui = SetupTUI(self.app)
            config = tui.run()
            
            if config:
                # In Cement Config speichern
                self.app.config.set('ccc', 'name', config['name'])
                self.app.config.set('ccc', 'debug', config['debug'])
                self.app.config.set('ccc', 'update', config['update'])
                
                print(f"✓ Setup abgeschlossen!")
                print(f"  Projekt: {config['name']}")
                print(f"  Debug: {config['debug']}")
                print(f"  Auto-Update: {config['update']}")
        else:
            # CLI-Modus
            print("Nutze --interactive für das coole TUI-Menü!")
            print("Oder: python app.py setup run -i")

class MyApp(App):
    """Cement App"""
    
    class Meta:
        label = 'ccc'
        base_controller = 'base'
        handlers = [SetupController]
        
        # Config-Datei definieren
        config_files = ['~/.ccc.conf']
        
        # Config-Defaults
        config_defaults = {
            'ccc': {
                'name': 'default',
                'debug': False,
                'update': False,
            }
        }

with MyApp() as app:
    app.run()
```

#### So nutzt du es

**Terminal-Modus (klassisch):**
```bash
python app.py setup run
# → Zeigt CLI-Hinweis

python app.py setup run --interactive
# → TUI startet!
```

**Was passiert im TUI:**
```
┌─────────────────────────────────────────┐
│ Header                                  │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │ Projekt-Name...                     │ │
│ ├─────────────────────────────────────┤ │
│ │ [X] Debug aktivieren                │ │
│ │ [ ] Auto-Update                     │ │
│ │                                     │ │
│ │        [ Speichern ]                │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ Footer                                  │
└─────────────────────────────────────────┘
```

**Browser-Modus (Magic!):**
```bash
textual serve app.py
# → Server running on http://localhost:8000

# Browser öffnen → Gleiche UI im Browser!
```

**Mit Host für Remote-Access:**
```bash
textual serve app.py --host 0.0.0.0 --port 8000
# → Von überall erreichbar!
```

#### Warum dieses Beispiel perfekt ist

**1. Minimal aber komplett**
- Nur ~80 Zeilen Code
- Alles was man braucht
- Keine unnötigen Features
- Kopieren → Anpassen → Fertig

**2. Cement-Integration richtig gemacht**
```python
def __init__(self, cement_app):
    self.cement_app = cement_app
    # ← Jetzt hast du Zugriff auf:
    # - self.cement_app.config
    # - self.cement_app.log
    # - self.cement_app.controllers
```

**3. Config-Persistence**
```python
# TUI setzt Config
self.app.config.set('ccc', 'name', value)

# Andere Commands nutzen Config
value = self.app.config.get('ccc', 'name')
```

**4. Dual-Mode by Design**
```bash
ccc setup run              # CLI
ccc setup run -i           # TUI
ccc setup run --interactive # TUI (long)
```

**5. Erweiterbar**

Willst du mehr Widgets?
```python
def compose(self):
    yield Input(placeholder="Email", id="email")
    yield Select(
        options=[("dev", "Development"), ("prod", "Production")],
        id="environment"
    )
    yield Switch(value=True, id="notifications")
```

Willst du Validierung?
```python
from textual.validation import Function, Length

yield Input(
    placeholder="Email",
    validators=[
        Function(self.validate_email, "Invalid email")
    ]
)
```

Willst du Async-Loading?
```python
async def on_mount(self):
    """Läuft beim Start"""
    self.query_one("#status").update("Loading...")
    data = await self.load_config()
    self.query_one("#status").update("Ready!")
```

#### Die drei Modi im Vergleich

**CLI-Modus: Für Scripts**
```bash
ccc setup run --name myproject --debug --update
# → Automation-freundlich
# → Scriptbar
# → Kein User-Input nötig
```

**TUI-Modus: Für Interaktiv**
```bash
ccc setup run --interactive
# → User-freundlich
# → Visuelles Feedback
# → Navigation mit Pfeilen/Maus
```

**Web-Modus: Für Remote**
```bash
textual serve app.py --host 0.0.0.0
# → Remote-Access
# → Team-Collaboration
# → Mobile-freundlich
```

**Alle drei Modi. Ein Code. Zero Duplikation.**

#### Debugging-Tipps

**Textual-Console für Development:**
```bash
textual console
# Terminal 1: Console läuft

python app.py setup run -i
# Terminal 2: App läuft

# Console zeigt Debug-Output!
```

**Logging in TUI:**
```python
def on_button_pressed(self, event):
    self.cement_app.log.info("Button pressed")
    # → Geht ins Cement Log
    
    self.log("Processing...")
    # → Geht in Textual Console
```

**Error Handling:**
```python
def on_button_pressed(self, event):
    try:
        result = self.validate_and_save()
        self.exit(result)
    except Exception as e:
        self.cement_app.log.error(f"Error: {e}")
        self.query_one("#status").update(f"Error: {e}")
```

---

### Ein vollständiges Beispiel: CCC Site Creator

Jetzt wo du das Basis-Pattern kennst, lass uns eine richtige Feature bauen: Interaktiver Site-Creator

```python
# ccc/tui/site_creator.py
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Input, Button, Checkbox, Static
from textual.validation import Function

class SiteCreator(App):
    """TUI für CCC Site Creation"""
    
    CSS = """
    Screen {
        background: #0e1117;
    }
    
    Container {
        width: 60;
        height: auto;
        border: solid #2e3440;
        background: #1e2127;
        padding: 1 2;
    }
    
    Input {
        margin: 1 0;
    }
    
    Button {
        width: 100%;
        margin: 1 0;
    }
    
    #success {
        color: #a3be8c;
        text-align: center;
    }
    
    #error {
        color: #bf616a;
        text-align: center;
    }
    """
    
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+s", "save", "Create Site"),
    ]
    
    def __init__(self, cement_app):
        super().__init__()
        self.cement_app = cement_app
        self.result = None
    
    def compose(self) -> ComposeResult:
        """Create UI"""
        yield Header()
        with Container():
            yield Static("Create New Site", id="title")
            yield Input(
                placeholder="example.com",
                id="domain",
                validators=[
                    Function(self.validate_domain, "Invalid domain")
                ]
            )
            yield Checkbox("Enable SSL (Let's Encrypt)", id="ssl", value=True)
            yield Checkbox("Enable PHP", id="php", value=True)
            yield Checkbox("Enable Cache", id="cache", value=True)
            yield Button("Create Site", id="create", variant="success")
            yield Static("", id="status")
        yield Footer()
    
    def validate_domain(self, value: str) -> bool:
        """Validate domain format"""
        import re
        pattern = r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,}$'
        return bool(re.match(pattern, value.lower()))
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button click"""
        if event.button.id == "create":
            await self.create_site()
    
    async def action_save(self) -> None:
        """Keyboard shortcut handler"""
        await self.create_site()
    
    async def create_site(self) -> None:
        """Create the site"""
        status = self.query_one("#status", Static)
        
        # Get values
        domain = self.query_one("#domain", Input).value
        ssl = self.query_one("#ssl", Checkbox).value
        php = self.query_one("#php", Checkbox).value
        cache = self.query_one("#cache", Checkbox).value
        
        # Validate
        if not domain:
            status.update("[#error]Error: Domain required")
            return
        
        try:
            # Call Cement business logic
            status.update("Creating site...")
            
            # Hier würde der echte CCC Code laufen:
            # self.cement_app.controllers['site'].create(
            #     domain=domain,
            #     ssl=ssl,
            #     php=php,
            #     cache=cache
            # )
            
            # Simulate
            import asyncio
            await asyncio.sleep(1)
            
            self.result = {
                'domain': domain,
                'ssl': ssl,
                'php': php,
                'cache': cache,
            }
            
            status.update(f"[#success]✓ Site {domain} created successfully!")
            
            # Auto-close nach 2 Sekunden
            await asyncio.sleep(2)
            self.exit(self.result)
            
        except Exception as e:
            status.update(f"[#error]Error: {str(e)}")

# Integration in Cement Controller:
class SiteController(Controller):
    class Meta:
        label = 'site'
    
    @ex(help='create site (interactive)')
    def create_interactive(self):
        """TUI for site creation"""
        from ccc.tui.site_creator import SiteCreator
        
        tui = SiteCreator(self.app)
        result = tui.run()
        
        if result:
            self.app.log.info(f"Site created via TUI: {result}")
            print(f"✓ Site {result['domain']} ready!")
```

**Nutzung:**

```bash
# Terminal
ccc site create-interactive

# Browser
textual serve ccc/tui/site_creator.py --host 0.0.0.0
# → http://localhost:8000
```

**Features:**
- ✅ Validierung (Domain-Format)
- ✅ Checkboxes (SSL, PHP, Cache)
- ✅ Status-Messages (Success/Error)
- ✅ Keyboard Shortcuts (Ctrl+S)
- ✅ Async (non-blocking)
- ✅ CSS-Styling
- ✅ Terminal UND Browser ready

---

### Testing TUI Apps

Textual hat eingebaute Test-Support!

```python
# tests/test_site_creator.py
from textual.pilot import Pilot
from ccc.tui.site_creator import SiteCreator

async def test_site_creation():
    """Test TUI programmatically"""
    app = SiteCreator(cement_app=None)
    
    async with app.run_test() as pilot:
        # Type domain
        await pilot.click("#domain")
        await pilot.press("e", "x", "a", "m", "p", "l", "e", ".", "c", "o", "m")
        
        # Click button
        await pilot.click("#create")
        
        # Wait
        await pilot.pause()
        
        # Assert
        status = app.query_one("#status")
        assert "created successfully" in status.renderable.plain
```

**Kein Browser. Kein Terminal. Reine Tests.**

---

### Best Practices für CCC CODE

Für unser Projekt empfehle ich:

#### 1. Separate TUI Module

```
ccc/
├── cli/
│   └── main.py          # CLI Entry
├── controllers/
│   ├── site.py          # Business Logic
│   └── setup.py
├── tui/
│   ├── __init__.py
│   ├── site_creator.py  # TUI Apps
│   ├── setup_wizard.py
│   └── styles.tcss      # Shared CSS
└── core/
    └── logic.py         # Shared Code
```

**Trennung:**
- `controllers/` → Cement Controller (CLI)
- `tui/` → Textual Apps (TUI)
- `core/` → Business Logic (shared)

#### 2. Dual-Mode Commands

```python
@ex(
    help='create site',
    arguments=[
        (['--interactive', '-i'],
         {'action': 'store_true'}),
        (['domain'],
         {'help': 'domain name'}),
    ]
)
def create(self):
    if self.app.pargs.interactive:
        # TUI
        from ccc.tui.site_creator import SiteCreator
        tui = SiteCreator(self.app)
        result = tui.run()
    else:
        # CLI
        domain = self.app.pargs.domain
        self.create_site(domain)
```

**Flexibel:**
```bash
ccc site create example.com           # CLI
ccc site create -i                    # TUI
ccc site create --interactive         # TUI
```

#### 3. Shared Business Logic

```python
# ccc/core/site.py
def create_site(domain, ssl=True, php=True):
    """Core logic - used by CLI AND TUI"""
    # Nginx config
    # SSL setup
    # Database
    return result

# CLI nutzt es:
class SiteController(Controller):
    def create(self):
        from ccc.core.site import create_site
        result = create_site(domain, ssl, php)

# TUI nutzt es auch:
class SiteCreator(App):
    async def create_site(self):
        from ccc.core.site import create_site
        result = create_site(domain, ssl, php)
```

**DRY:** Don't Repeat Yourself

#### 4. Web-Mode für Remote

```bash
# Install Script könnte optional:
ccc setup --web

# Dann:
systemd service für: textual serve ccc-tui

# Team kann verbinden:
http://server-ip:8000
```

---

### Zusammenfassung Kapitel 7

Was haben wir über TUI gelernt?

#### Die Kernkonzepte:

**TUI = Text User Interface**
- Text-basiert, aber visuell
- Widgets, Navigation, Interaktion
- Im Terminal (oder Browser!)
- Best of CLI + GUI

**Textual = Moderne TUI-Library**
- Async-first (asyncio)
- CSS-Styling
- React-ähnliche API
- Batteries included
- **Browser-Support!**

#### Cement + Textual Integration:

```python
# Pattern:
Controller (Cement) → Business Logic (Core) ← TUI (Textual)
```

**Trennung:**
- Cement: CLI-Parsing, Config, Logging
- Core: Business Logic (shared)
- Textual: Interactive UI

#### Die Web-UI Magie:

```
Ein Python Code:
  ├─→ Terminal (python app.py)
  └─→ Browser (textual serve app.py)

Zero Änderungen. Gleiche App. Zwei Interfaces.
```

**Use Cases:**
- Remote Management
- Team Collaboration
- Demos & Präsentationen
- Mobile Access

#### Best Practices:

1. ✅ Separate TUI Module (`ccc/tui/`)
2. ✅ Dual-Mode Commands (`--interactive`)
3. ✅ Shared Business Logic
4. ✅ CSS für Styling (nicht Python)
5. ✅ Tests mit Textual Pilot
6. ✅ Web-Mode für Remote-Teams

#### Die wichtigste Erkenntnis:

**TUI ist nicht "alt" oder "retro" - TUI ist die Zukunft für CLI-Tools.**

Textual macht TUI:
- Modern (async, CSS, React-like)
- Schön (16M Farben, Animationen)
- Flexibel (Terminal UND Browser)
- Entwickler-freundlich (Python-only)

**Für CCC CODE bedeutet das:**
- Setup-Wizard? TUI.
- Site-Creator? TUI.
- Config-Editor? TUI.
- Remote-Management? Web-TUI.

**Und der User freut sich:**
```bash
ccc setup --interactive  # → Beautiful TUI
# Statt:
ccc setup --name x --debug true --ssl true --php 8.2 ...
```

**HUFi.AI in Action:**
- Human führt (wählt TUI oder CLI)
- AI unterstützt (baut beide Modi)
- Beide werden besser (User Experience++)

---

**Im nächsten Kapitel:** Fehlerkultur in Mensch-KI-Teams - Wenn AI Agents Fehler machen (und Menschen auch), und wie wir daraus lernen.

---

*Ende von Kapitel 7*
