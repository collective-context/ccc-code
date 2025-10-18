[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)

# Kapitel 9 - Schritte nach der Installation und Best Practices

Nach der Installation.

### Bash-Skript-Analyse
- **wo_install_acme_sh()**: Installiert acme.sh mit Git-Clone (Best Practice: Cron für Auto-Renewals und `.well-known`-Setup).
- **wo_update_wp_cli()**: Aktualisiert WP-CLI via `wget` (Methode: Symlink für `/usr/bin/wp`).

### Python-Dateien
- **wo/core/services.py**: `WOService` für `start_service()`, `restart_service()` (Methode: `subprocess.Popen` mit `nginx -t`; Best Practice: Config-Checks vor Reloads).
- **wo/core/sslutils.py**: `SSL` für Zertifikatsprüfungen (Methode: `getexpirationdays()` via `openssl`; Best Practice: Automatische Renewals).
- **wo/cli/plugins/stack_services.py**: `WOStackStatusController` für Dienst-Status (Methode: `get_service_status()` mit `subprocess`; Best Practice: Bedingte Checks für Remote-MySQL).
- **Allgemeine Best Practices**: Führen Sie `wo maintenance` regelmäßig aus; sichern Sie Backups; nutzen Sie `wo sync` für DB-Updates.

[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)
