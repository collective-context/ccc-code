"""CCA plugins module - auto-loaded by Cement v2"""

# Cement v2 lädt automatisch alle .py Dateien in diesem Verzeichnis
# und ruft die load() Funktion in jeder Datei auf.
# 
# KEIN zentraler Loader hier - jedes Plugin registriert sich selbst!
# 
# Pattern (wie in WordOps):
# - App setzt plugin_bootstrap = 'cca.cli.plugins'
# - Cement scannt alle .py Dateien hier
# - Cement ruft load(app) in JEDER Plugin-Datei auf
# - Jedes Plugin registriert seinen Controller in seiner load() Funktion
