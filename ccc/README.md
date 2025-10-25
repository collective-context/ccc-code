# CCC - Collective Context Commander

Production-ready orchestration and AI coordination tool.

🏗️ Projekt-Struktur komplett:
CCC CODE Repository - Fünf-Sterne-Architektur
═══════════════════════════════════════════════════

LEGACY (Cement v2) - Virtualenv:
├── wo/   ✓ Read-only Referenz
├── ccw/  ✓ Installiert in .venv-v2
└── cca/  ✓ Installiert in .venv-v2

MODERN (Cement v3) - uv:
├── ccb/  ✓ Beta - .venv-ccb ready
└── ccc/  ✓ Production - .venv-ccc ready (NEU!)
🎯 ccc/ Production System:

✅ Modern Cement v3 Framework
✅ pyproject.toml (no setup.py!)
✅ uv Package Management
✅ Vollständige Test Suite
✅ Development Tools (black, flake8, mypy)
✅ Funktionsfähige CLI

🚀 Quick-Test - Mach das jetzt:
bash# 1. In ccc/ wechseln und aktivieren
cd ccc
source .venv-ccc/bin/activate

# 2. CLI testen
ccc status
ccc --help

# 3. Python Import testen
python -c "import ccc; print('CCC Version:', ccc.__version__)"

# 4. Tests laufen lassen
pytest -v

# Ausgabe sollte sein:
# ✓ CCC Status: Operational
# ✓ Version: 1.0.0
# ✓ Tests PASSED

## ----------------------------------------------------------

## 🚀 Features

- **Modern Architecture**: Built on Cement v3 framework
- **AI Integration**: Native support for AI agent orchestration
- **Extensible**: Plugin-based architecture
- **Type-Safe**: Full type hints and mypy support
- **Well-Tested**: Comprehensive test coverage

## 📦 Installation

### Development Setup

```bash
# Create virtual environment with uv
uv venv .venv-ccc --python python3.11

# Activate
source .venv-ccc/bin/activate

# Install in development mode
uv pip install -e ".[dev]"
```

### Production Installation

```bash
uv pip install ccc
```

## 🎯 Usage

```bash
# Check status
ccc status

# Show help
ccc --help

# Run with debug
ccc --debug status
```

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=ccc --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 🛠️ Development

```bash
# Format code
black ccc/ tests/

# Lint
flake8 ccc/ tests/

# Type check
mypy ccc/

# Sort imports
isort ccc/ tests/
```

## 📚 Documentation

Full documentation: https://docs.collective-context.org

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🔗 Links

- Homepage: https://collective-context.org
- Repository: https://github.com/collective-context/ccc-code
- Issues: https://github.com/collective-context/ccc-code/issues
