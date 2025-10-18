[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)

# Kapitel 5 - Distributionsprüfungen und Abhängigkeiten

Prüfungen und Abhängigkeiten.

### Bash-Skript-Analyse
- **wo_check_distro()**: LSB-Release-Check mit `grep -E` für Codename (Best Practice: `--force` nur für Tests; explizite Unterstützung für `focal|jammy`).
- **wo_install_dep()**: Paket-Installation, Locale-Setup mit `locale-gen` (Methode: Bedingte PPAs für Ubuntu).

### Python-Dateien
- **wo/core/checkfqdn.py**: `WOFqdn` für FQDN/IP-Prüfungen via `requests` (Methode: `check_fqdn_ip()` vergleicht IPs; Best Practice: Fallback bei Request-Fehlern).
- **wo/core/domainvalidate.py**: `WODomain` für URL-Validierung (Methode: `validate()` entfernt Protokolle; `getlevel()` nutzt Suffix-Liste für Domain-Typen).
- **wo/core/acme.py**: `WOAcme` für SSL-Issue (Methode: `setupletsencrypt()` mit acme.sh; Best Practice: DNS-Checks vor Zertifikatsausstellung).
- **Best Practice**: Validieren Sie Eingaben frühzeitig, um Sicherheitslücken zu vermeiden.

[Inhalt](../install-handbook.md) | [Einführung](install-handbook-introduction.md) | [Kapitel -1-](install-handbook-chapter1.md) | [-2-](install-handbook-chapter2.md) | [-3-](install-handbook-chapter3.md) | [-4-](install-handbook-chapter4.md) | [-5-](install-handbook-chapter5.md) | [-6-](install-handbook-chapter6.md) | [-7-](install-handbook-chapter7.md) | [-8-](install-handbook-chapter8.md) | [-9-](install-handbook-chapter9.md) | [Anhang -A-](install-handbook-appendixa.md) | [-B-](install-handbook-appendixb.md) | [ALLE](install-handbook-all.md)
