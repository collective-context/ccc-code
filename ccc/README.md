# CCC - Collective Context Commander

Production-ready orchestration and AI coordination tool built on Cement v3.

## 🚀 Quick Start

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup
cd ccc
uv venv .venv-ccc
source .venv-ccc/bin/activate
uv pip install -e ".[dev]"

# Test
ccc info
ccc status
pytest
```

## 📦 Installation

### Development

```bash
git clone https://github.com/collective-context/ccc-code.git
cd ccc-code/ccc
uv venv .venv-ccc
source .venv-ccc/bin/activate
uv pip install -e ".[dev]"
```

### Production

```bash
uv pip install ccc
```

## 🎯 Usage

```bash
ccc info      # System information
ccc status    # Operational status
ccc debug     # Debug information
ccc --help    # Show help
```

## 🧪 Testing

```bash
pytest                              # Run all tests
pytest --cov=ccc --cov-report=html  # With coverage
open htmlcov/index.html             # View coverage
```

## 🛠️ Development

```bash
black ccc/ tests/    # Format
flake8 ccc/ tests/   # Lint
mypy ccc/            # Type check
isort ccc/ tests/    # Sort imports
```

## 📁 Structure

```
ccc/
├── ccc/
│   ├── main.py           # Cement v3 app
│   ├── core/             # Core logic
│   ├── controllers/      # Controllers
│   └── config/           # Configuration
├── tests/
│   ├── test_main.py      # Unit tests
│   └── test_cli.py       # CLI tests
├── .github/workflows/    # CI/CD
└── pyproject.toml        # Package config
```

## 📚 Links

- Homepage: https://collective-context.org
- Docs: https://docs.collective-context.org
- GitHub: https://github.com/collective-context/ccc-code

## 📄 License

MIT License
