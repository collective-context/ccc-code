[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)

# Kapitel 2 - Vorbereitung auf die Installation

Vorbereitung umfasst Distro-Prüfungen und Abhängigkeiten.

### Bash-Skript-Analyse
- **wo_check_distro()**: Prüft LSB-Release (Ubuntu/Debian/Raspbian); `--force` überspringt (Best Practice: Explizite Codename-Checks wie `buster|focal` für Versionssicherheit).
- **wo_install_dep()**: Installiert Pakete wie `python3-pip`, `git` via `apt-get` mit `--assume-yes` (Methode: Bedingte Installation für Ubuntu/Debian; Best Practice: `export DEBIAN_FRONTEND=noninteractive` für headless Setup).

### Python-Dateien
- **wo/core/aptget.py**: Klasse `WOAptGet` mit `update()`, `install()` (Methode: Subprocess für `apt-get` mit Logging; Best Practice: Fehlerbehandlung via `proc.returncode` und `Log.error`).
- **wo/core/apt_repo.py**: `WORepo` für `add()`, `remove()` von Repos (Methode: PPA-Handling mit `add-apt-repository`; Best Practice: `apt-key adv` für Key-Import).
- **wo/core/database.py**: Initialisiert SQLAlchemy-Engine (Methode: `create_engine` für DB-Verbindung; Best Practice: Scoped Sessions für Thread-Safety).
- **Best Practice**: Führen Sie `apt update` vor Installationen aus und handhaben Sie Key-Errors robust.

[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)
