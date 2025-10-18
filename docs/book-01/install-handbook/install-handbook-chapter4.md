[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)

# Kapitel 4 - Hauptfunktionen und Skriptargumente

Hauptfunktionen und Argument-Handling.

### Bash-Skript-Analyse
- **wo_lib_echo()**, **wo_lib_error()**: Logging-Funktionen mit Farben (Methode: `echo -e` für formattierte Ausgaben; Best Practice: Redirect zu Logs für Traceability).
- **Argument-Parsing**: `while`-Loop für `--branch`, `--force` (Methode: Sichere EUID-Prüfung mit `[[ $EUID -ne 0 ]]`).

### Python-Dateien
- **wo/cli/plugins/site_functions.py**: Funktionen wie `setupdatabase()`, `logwatch()` (Methode: `WOMysql.execute()` für DB-Operationen; Best Practice: `SiteError` für benutzerdefinierte Exceptions).
- **wo/core/shellexec.py**: `WOShellExec` mit `cmd_exec()` (Methode: `subprocess.Popen` mit Logging; Best Practice: `CommandExecutionError` für Fehlerhandling).
- **wo/core/template.py**: `WOTemplate` für `deploy()` (Methode: `app.render` mit Mustache; Best Practice: `overwrite`-Flag für sichere Updates).
- **Best Practice**: Verwenden Sie try-except-Blöcke und loggen Sie detailliert für Debugging.

[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)
