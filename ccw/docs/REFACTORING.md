# CCW Refactoring Changelog

## 2025-10-27: Initial Fork from WordOps

### Changed
- Package: `wordops` → `ccw`
- Entry Point: `wo` → `ccw`
- Namespace: `wo.*` → `ccw.*`
- Classes: `WO*` → `CCW*`
- Paths: `/opt/wo` → `/opt/ccw` (ccw-specific)
- Strings: `"WordOps"` → `"CCC CODE"`
- Strings: `"wordops"` → `"ccc-code"`

### Unchanged (Shared Infrastructure)
- `/etc/nginx/` - Shared Webserver
- `/var/run/php/` - Shared PHP-FPM
- `/var/lib/mysql/` - Shared Database
- `/var/www/` - Shared Webroot

### Version
- 3.22.0 (synced with WordOps)

### Repository
- https://github.com/collective-context/ccc-code

<!-- Zuletzt bearbeitet: 2025-10-27 -->
