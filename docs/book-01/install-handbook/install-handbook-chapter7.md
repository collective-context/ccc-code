[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)

# Kapitel 7 - GPG-Schlüssel, Repositories und Updates

Schlüssel und Repos.

### Bash-Skript-Analyse
- **wo_download_gpg_keys()**: Lädt Keys für Redis/MariaDB/Nginx via `curl` und `gpg --dearmor` (Best Practice: `/usr/share/keyrings` für sichere Speicherung).
- **wo_update_repo()**: Bereinigt Repos mit `grep` und `awk` (Methode: Migration alter Repos zu neuen Dateien).

### Python-Dateien
- **wo/core/apt_repo.py**: `add()`, `remove()` für Repos (Methode: `add-apt-repository` mit Logging; Best Practice: `apt-key adv` für Key-Import).
- **wo/core/download.py**: `WODownload` für Releases via `requests` (Methode: `latest_release()` parst GitHub-API; Best Practice: Timeout und Retry für Robustheit).
- **wo/core/stackconf.py**: `WOConf` für Nginx-Konfig (Methode: `nginxcommon()` deployt Templates; Best Practice: Versionsspezifische Upstream-Konfigs).
- **Best Practice**: Aktualisieren Sie Repos vor Installationen und validieren Sie Keys.

[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)
