[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)

# Kapitel 6 - Verzeichnisinitialisierung und Logging

Verzeichnisse und Logging.

### Bash-Skript-Analyse
- **wo_dir_init()**: Erstellt `/var/log/wo`, setzt ACL mit `chmod 750` (Best Practice: `chown root:adm` für sichere Logs).
- **wo_init_variables()**: Setzt Logs, Backups mit `readonly` (Methode: Bedingte Migration von EE).

### Python-Dateien
- **wo/core/logging.py**: Klasse `Log` für `error()`, `info()` mit ANSI-Codes (Methode: `valide()` für Fortschrittsanzeige; Best Practice: `app.log` für zentrales Logging).
- **wo/core/fileutils.py**: `WOFileUtils` für `mkdir()`, `chown()` (Methode: Rekursive Operationen mit `os.walk`; Best Practice: Exception-Handling für I/O-Fehler).
- **wo/core/logwatch.py**: `LogWatcher` für Echtzeit-Logs (Methode: `loop()` mit `readlines()`; Best Practice: Rotation-Handling).
- **Best Practice**: Loggen Sie alle Operationen und sichern Sie Verzeichnisse mit minimalen Rechten.

[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)
