[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)

# Kapitel 8 - Synchronisation, Upgrades und Migrationen

Sync und Upgrades.

### Bash-Skript-Analyse
- **wo_sync_db()**: Migriert DB von EE mit SQLite (Methode: `echo "CREATE TABLE..." | sqlite3` für Schema; Best Practice: Backups vor Migration).
- **wo_upgrade_nginx()**: Upgradet Nginx mit Rsync (Methode: `apt-get autoremove` für Cleanup).

### Python-Dateien
- **wo/cli/plugins/sitedb.py**: DB-Operationen wie `getSiteInfo()` mit SQLAlchemy (Methode: `db_session.commit()` für Updates; Best Practice: Exception-Handling).
- **wo/core/git.py**: `WOGit` für `add()`, `rollback()` (Methode: `git.bake()` für Befehle; Best Practice: Auto-Commit für Konfigurationsänderungen).
- **wo/cli/plugins/stack_migrate.py**: `WOMigrateController` für Upgrades (Methode: `migrate_mariadb()` mit Backups; Best Practice: `--force` für automatisierte Migrationen).
- **Best Practice**: Testen Sie Migrationen in Staging-Umgebungen.

[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)
