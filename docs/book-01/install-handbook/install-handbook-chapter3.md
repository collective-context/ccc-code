[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)

# Kapitel 3 - Installationsprozess

Der Kerninstallationsprozess im Skript und Python.

### Bash-Skript-Analyse
- **wo_install()**: Erstellt Python-Venv, installiert via `pip` mit `--upgrade-strategy=eager` (Methode: Bedingte Venv-Erstellung; Best Practice: Symlinks für `/usr/local/bin/wo` zur Zugänglichkeit).
- **wo_travis_install()**: Für CI-Tests mit Git-Checkout (Methode: Branch-spezifische Installation).

### Python-Dateien
- **wo/cli/main.py**: `WOApp` als Cement-App mit `config_defaults` und Extensions wie `colorlog` (Methode: `CementApp` für CLI-Struktur; Best Practice: `exit_on_close` für sauberen Shutdown).
- **wo/cli/plugins/stack.py**: `WOStackController` für Stack-Installation mit Argument-Parser (Methode: `install()` prüft und installiert Pakete; Best Practice: Bedingte PHP-Versionen via `WOVar.wo_php_versions`).
- **wo/cli/plugins/stack_pref.py**: `pre_pref()`, `post_pref()` für Konfiguration (Methode: Template-Deployment; Best Practice: Git-Integration für Rollbacks).
- **Best Practice**: Testen Sie nach Installation mit `wo --version` und sichern Sie Backups vor Upgrades.

[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)
