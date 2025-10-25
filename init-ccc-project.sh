#!/bin/bash
################################################################################
# CCC CODE: Modern Cement v3 Project Initializer
# Erstellt ein production-ready Cement v3 Projekt mit uv
# Version 1.0 - October 2025
################################################################################

set -e  # Exit on error

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
cat << "EOF"
╔════════════════════════════════════════════════════╗
║     CCC Production Project Initializer            ║
║     Modern Cement v3 + uv Setup                   ║
╚════════════════════════════════════════════════════╝
EOF
echo ""

# Config
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CCC_DIR="$PROJECT_ROOT/ccc"
VERSION="1.0.0"
PYTHON_VERSION="3.11"

echo -e "${BLUE}Project Root:${NC} $PROJECT_ROOT"
echo -e "${BLUE}CCC Directory:${NC} $CCC_DIR"
echo -e "${BLUE}Version:${NC} $VERSION"
echo ""

# Check uv
if ! command -v uv &> /dev/null; then
    echo -e "${RED}✗${NC} uv not found!"
    echo ""
    echo "Install with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi
echo -e "${GREEN}✓${NC} uv installed: $(uv --version)"

# Check if ccc/ exists and is empty
if [ -d "$CCC_DIR" ]; then
    if [ "$(ls -A $CCC_DIR)" ]; then
        echo -e "${YELLOW}⚠${NC} Warning: ccc/ directory is not empty!"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
else
    mkdir -p "$CCC_DIR"
    echo -e "${GREEN}✓${NC} Created ccc/ directory"
fi

cd "$CCC_DIR"

################################################################################
# 1. Create pyproject.toml (Modern Python Packaging)
################################################################################
echo ""
echo -e "${CYAN}[1/8]${NC} Creating pyproject.toml..."

cat > pyproject.toml << 'EOF'
[project]
name = "ccc"
version = "1.0.0"
description = "Collective Context Commander - Production orchestration tool"
authors = [
    { name = "Collective Context Team", email = "info@collective-context.org" }
]
readme = "README.md"
requires-python = ">=3.9"
license = { text = "MIT" }
keywords = ["orchestration", "ai", "automation", "cement", "cli"]

classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: System :: Systems Administration",
]

dependencies = [
    "cement>=3.0.0,<4.0.0",
    "colorlog>=6.7.0",
    "pyyaml>=6.0",
    "jinja2>=3.1.0",
    "requests>=2.31.0",
    "psutil>=5.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "black>=23.7.0",
    "flake8>=6.1.0",
    "mypy>=1.5.0",
    "isort>=5.12.0",
    "pre-commit>=3.3.0",
]

[project.scripts]
ccc = "ccc.main:main"

[project.urls]
Homepage = "https://collective-context.org"
Documentation = "https://docs.collective-context.org"
Repository = "https://github.com/collective-context/ccc-code"
Issues = "https://github.com/collective-context/ccc-code/issues"

[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["ccc"]

[tool.setuptools.package-data]
ccc = [
    "config/*.yaml",
    "templates/*.j2",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--verbose",
    "--strict-markers",
    "--tb=short",
    "--cov=ccc",
    "--cov-report=term-missing",
    "--cov-report=html",
]

[tool.black]
line-length = 88
target-version = ['py39', 'py310', 'py311', 'py312']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
EOF

echo -e "${GREEN}✓${NC} Created pyproject.toml"

################################################################################
# 2. Create Project Structure
################################################################################
echo ""
echo -e "${CYAN}[2/8]${NC} Creating project structure..."

mkdir -p ccc/{cli,core,config,templates}
mkdir -p tests/{unit,integration}
mkdir -p docs

# Create __init__.py files
cat > ccc/__init__.py << 'EOF'
"""
Collective Context Commander (CCC)
Production orchestration and AI coordination tool
"""

__version__ = "1.0.0"
__author__ = "Collective Context Team"

from ccc.main import CCCApp

__all__ = ["CCCApp", "__version__"]
EOF

touch ccc/cli/__init__.py
touch ccc/core/__init__.py
touch ccc/config/__init__.py
touch ccc/templates/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py

echo -e "${GREEN}✓${NC} Created directory structure"

################################################################################
# 3. Create Main Application (Cement v3)
################################################################################
echo ""
echo -e "${CYAN}[3/8]${NC} Creating main application..."

cat > ccc/main.py << 'EOF'
"""
Main application entry point for CCC
Cement v3 based CLI application
"""

from cement import App, Controller, ex
from cement.core.exc import CaughtSignal


class BaseController(Controller):
    """Base controller for CCC CLI"""

    class Meta:
        label = "base"
        description = "Collective Context Commander - AI orchestration tool"
        arguments = [
            (["-v", "--version"], {"action": "version", "version": "CCC 1.0.0"}),
        ]

    @ex(
        help="Show current status",
    )
    def status(self):
        """Display system status"""
        self.app.log.info("Checking CCC status...")
        print("CCC Status: Operational ✓")
        print(f"Version: {self.app.config.get('ccc', 'version')}")


class CCCApp(App):
    """CCC Application"""

    class Meta:
        label = "ccc"
        base_controller = "base"
        handlers = [BaseController]
        extensions = ["yaml", "colorlog", "jinja2"]
        config_file_suffix = ".yml"
        config_defaults = {
            "ccc": {
                "version": "1.0.0",
                "debug": False,
            }
        }
        log_handler = "colorlog"
        output_handler = "jinja2"


def main():
    """Main entry point"""
    with CCCApp() as app:
        try:
            app.run()
        except AssertionError as e:
            print(f"AssertionError: {e}")
            app.exit_code = 1
        except CaughtSignal as e:
            print(f"\n{e}")
            app.exit_code = 0


if __name__ == "__main__":
    main()
EOF

echo -e "${GREEN}✓${NC} Created ccc/main.py"

################################################################################
# 4. Create Config Files
################################################################################
echo ""
echo -e "${CYAN}[4/8]${NC} Creating configuration files..."

cat > ccc/config/default.yaml << 'EOF'
# CCC Default Configuration
ccc:
  version: "1.0.0"
  debug: false
  
  # Logging
  log:
    level: INFO
    file: /var/log/ccc/ccc.log
  
  # Orchestration
  orchestration:
    enabled: true
    max_parallel_tasks: 5
  
  # AI Integration
  ai:
    enabled: true
    provider: anthropic
    model: claude-sonnet-4-5
EOF

echo -e "${GREEN}✓${NC} Created config/default.yaml"

################################################################################
# 5. Create Tests
################################################################################
echo ""
echo -e "${CYAN}[5/8]${NC} Creating test suite..."

cat > tests/test_main.py << 'EOF'
"""
Tests for main CCC application
"""

import pytest
from ccc.main import CCCApp


def test_app_creation():
    """Test that app can be created"""
    with CCCApp() as app:
        assert app is not None


def test_app_version():
    """Test app version"""
    with CCCApp() as app:
        assert app.config.get("ccc", "version") == "1.0.0"
EOF

cat > tests/conftest.py << 'EOF'
"""
Pytest configuration and fixtures
"""

import pytest
from ccc.main import CCCApp


@pytest.fixture
def app():
    """App fixture"""
    with CCCApp() as app:
        yield app
EOF

echo -e "${GREEN}✓${NC} Created test files"

################################################################################
# 6. Create Documentation
################################################################################
echo ""
echo -e "${CYAN}[6/8]${NC} Creating documentation..."

cat > README.md << 'EOF'
# CCC - Collective Context Commander

Production-ready orchestration and AI coordination tool.

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
EOF

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
.venv-ccc/
venv/
ENV/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
/var/log/ccc/

# Config (local overrides)
*.local.yaml
*.local.yml
EOF

echo -e "${GREEN}✓${NC} Created documentation files"

################################################################################
# 7. Create uv venv and Install
################################################################################
echo ""
echo -e "${CYAN}[7/8]${NC} Creating uv virtual environment..."

uv venv .venv-ccc --python "python$PYTHON_VERSION"
echo -e "${GREEN}✓${NC} Created .venv-ccc"

echo ""
echo -e "${CYAN}[7/8]${NC} Installing dependencies..."
uv pip install -e ".[dev]" --python .venv-ccc

echo -e "${GREEN}✓${NC} Dependencies installed"

################################################################################
# 8. Run Tests
################################################################################
echo ""
echo -e "${CYAN}[8/8]${NC} Running initial tests..."

source .venv-ccc/bin/activate
pytest tests/ -v
deactivate

################################################################################
# Summary
################################################################################
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         CCC Project Initialized! ✓                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Project Structure:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ccc/"
echo "├── ccc/                  # Main package"
echo "│   ├── __init__.py"
echo "│   ├── main.py           # Cement v3 app"
echo "│   ├── cli/              # CLI commands"
echo "│   ├── core/             # Core logic"
echo "│   ├── config/           # Configuration"
echo "│   └── templates/        # Jinja2 templates"
echo "├── tests/                # Test suite"
echo "│   ├── unit/"
echo "│   └── integration/"
echo "├── docs/                 # Documentation"
echo "├── pyproject.toml        # Modern packaging (no setup.py!)"
echo "├── README.md"
echo "└── .gitignore"
echo ""
echo -e "${BLUE}Virtual Environment:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Location: $CCC_DIR/.venv-ccc"
echo "Python:   $(python$PYTHON_VERSION --version)"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. ${CYAN}Activate environment:${NC}"
echo "   cd ccc"
echo "   source .venv-ccc/bin/activate"
echo ""
echo "2. ${CYAN}Test the CLI:${NC}"
echo "   ccc status"
echo "   ccc --help"
echo ""
echo "3. ${CYAN}Run tests:${NC}"
echo "   pytest"
echo ""
echo "4. ${CYAN}Add to PyCharm:${NC}"
echo "   Settings → Python Interpreter → Add Interpreter"
echo "   Select: $CCC_DIR/.venv-ccc/bin/python"
echo ""
echo "5. ${CYAN}Start developing:${NC}"
echo "   - Add controllers in ccc/cli/"
echo "   - Add core logic in ccc/core/"
echo "   - Add tests in tests/"
echo ""
echo -e "${GREEN}✓ Ready for development!${NC}"
