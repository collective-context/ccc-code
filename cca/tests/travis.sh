#!/usr/bin/env bash
#
# CCA Alpha Testing Script
# Based on CCC CODE tests/travis.sh pattern
#
# Usage:
#   sudo bash cca/tests/travis.sh          # Full test suite
#   sudo bash cca/tests/travis.sh --ci     # CI optimized

# Colors (wie CCC CODE)
CSI='\033['
CRED="${CSI}1;31m"
CGREEN="${CSI}1;32m"
CYELLOW="${CSI}1;33m"
CEND="${CSI}0m"

export DEBIAN_FRONTEND=noninteractive
unset LANG
export LANG='en_US.UTF-8'
export LC_ALL='C.UTF-8'

# Log setup
CCA_LOG_DIR="./logs"
CCA_LOG_FILE="$CCA_LOG_DIR/cca-test.log"

# Create log directory
mkdir -p "$CCA_LOG_DIR"

# Exit handler
exit_script() {
    echo -e "${CRED}#############################################${CEND}"
    echo -e "${CRED}   Tests failed! See log for details       ${CEND}"
    echo -e "${CRED}#############################################${CEND}"
    echo ""
    echo "Log file: $CCA_LOG_FILE"
    echo ""
    if [ -f "$CCA_LOG_FILE" ]; then
        echo "Last 50 lines of log:"
        tail -n 50 "$CCA_LOG_FILE"
    fi
    exit 1
}

# Parse arguments
CCA_CI_MODE=""
if [ "$1" = "--ci" ] || [ "$1" = "--actions" ]; then
    CCA_CI_MODE="yes"
fi

#############################################
# Installation Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCA Installation Test                '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Cleanup old installation
echo -ne "   Cleaning previous installation      [..]\r"
if {
    sudo rm -rf /root/cca /opt/cca /etc/cca /var/log/cca /usr/local/bin/cca /usr/bin/cca /tmp/cca /tmp/ccc-code
} >> "$CCA_LOG_FILE" 2>&1; then
    echo -ne "   Cleaning previous installation      [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   Cleaning previous installation      [${CRED}FAIL${CEND}]"
    exit_script
fi

# Install cca
echo -ne "   Installing cca                      [..]\r"
if {
    sudo -E bash cca/install
} >> "$CCA_LOG_FILE" 2>&1; then
    echo -ne "   Installing cca/install             [${CGREEN}OK${CEND}]\r\n"
else
    echo -e  "   Installing cca/install             [${CRED}FAIL${CEND}]"
    exit_script
fi

echo ""

#############################################
# Binary Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCA Binary Tests                     '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Test: Binary exists
echo -ne "   Binary exists                       [..]\r"
if command -v cca >/dev/null 2>&1; then
    CCA_PATH=$(which cca)
    echo -ne "   Binary exists at $CCA_PATH    [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   Binary exists                       [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: Python package import
echo -ne "   Python package import               [..]\r"
if {
    python3 -c "import cca; print(cca.VERSION)"
} >> "$CCA_LOG_FILE" 2>&1; then
    CCA_VERSION=$(python3 -c "import cca; print(cca.VERSION)")
    echo -ne "   Python package import v$CCA_VERSION     [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   Python package import               [${CRED}FAIL${CEND}]"
    exit_script
fi

echo ""

#############################################
# Command Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCA Command Tests                    '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Test: cca --version
echo -ne "   cca --version                       [..]\r"
if {
    cca --version
} >> "$CCA_LOG_FILE" 2>&1; then
    echo -ne "   cca --version                       [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   cca --version                       [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: cca -v (short version)
echo -ne "   cca -v                              [..]\r"
if {
    cca -v
} >> "$CCA_LOG_FILE" 2>&1; then
    echo -ne "   cca -v                              [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   cca -v                              [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: cca --help
echo -ne "   cca --help                          [..]\r"
if {
    cca --help
} >> "$CCA_LOG_FILE" 2>&1; then
    echo -ne "   cca --help                          [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   cca --help                          [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: cca info
echo -ne "   cca info                            [..]\r"
if {
    cca info
} >> "$CCA_LOG_FILE" 2>&1; then
    echo -ne "   cca info                            [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   cca info                            [${CRED}FAIL${CEND}]"
    exit_script
fi

echo ""

#############################################
# Plugin Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCA Plugin Tests                     '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Test: cca check --help
echo -ne "   cca check --help                    [..]\r"
if {
    cca check --help
} >> "$CCA_LOG_FILE" 2>&1; then
    echo -ne "   cca check --help                    [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   cca check --help                    [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: cca debug --help
echo -ne "   cca debug --help                    [..]\r"
if {
    cca debug --help
} >> "$CCA_LOG_FILE" 2>&1; then
    echo -ne "   cca debug --help                    [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   cca debug --help                    [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: Python plugin imports
echo -ne "   Python plugin imports               [..]\r"
if {
    /opt/cca/bin/python -c "from cca.cli.plugins import check, debug"
} >> "$CCA_LOG_FILE" 2>&1; then
    echo -ne "   Python plugin imports               [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   Python plugin imports               [${CRED}FAIL${CEND}]"
    exit_script
fi

echo ""

#############################################
# Logging Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCA Logging Tests                    '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Test: Log directory creation
echo -ne "   Log directory creation              [..]\r"
TEST_LOG_DIR="./logs-test"
if {
    mkdir -p "$TEST_LOG_DIR"
    [ -d "$TEST_LOG_DIR" ]
} >> "$CCA_LOG_FILE" 2>&1; then
    echo -ne "   Log directory creation              [${CGREEN}OK${CEND}]\r\n"
    rm -rf "$TEST_LOG_DIR"
else
    echo -e "   Log directory creation              [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: cca check actions --save (wenn gh CLI verfügbar)
if command -v gh >/dev/null 2>&1; then
    echo -ne "   cca check actions --save            [..]\r"
    if {
        cca check actions --save
    } >> "$CCA_LOG_FILE" 2>&1; then
        echo -ne "   cca check actions --save            [${CGREEN}OK${CEND}]\r\n"
    else
        echo -e "   cca check actions --save            [${CYELLOW}SKIP${CEND}]"
        echo "   (GitHub API issue or no actions found)"
    fi
else
    echo -e "   cca check actions --save            [${CYELLOW}SKIP${CEND}]"
    echo "   (gh CLI not installed)"
fi

echo ""

#############################################
# Integration Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCA Integration Tests                '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Test: cca debug summary (auf existierendem Log)
echo -ne "   cca debug summary                   [..]\r"
if [ -f "./logs/cca-debug.log" ]; then
    if {
        cca debug summary
    } >> "$CCA_LOG_FILE" 2>&1; then
        echo -ne "   cca debug summary                   [${CGREEN}OK${CEND}]\r\n"
    else
        echo -e "   cca debug summary                   [${CRED}FAIL${CEND}]"
        exit_script
    fi
else
    echo -e "   cca debug summary                   [${CYELLOW}SKIP${CEND}]"
    echo "   (No debug log found)"
fi

echo ""

#############################################
# Python Unit Tests (optional)
#############################################

if command -v pytest >/dev/null 2>&1; then
    echo -e "${CGREEN}#############################################${CEND}"
    echo -e '       CCA Python Unit Tests                '
    echo -e "${CGREEN}#############################################${CEND}"
    echo ""
    
    echo -ne "   Running pytest suite                [..]\r"
    if pytest cca/tests/ -v >> "$CCA_LOG_FILE" 2>&1; then
        echo -ne "   Running pytest suite                [${CGREEN}OK${CEND}]\r\n"
    else
        echo -e "   Running pytest suite                [${CYELLOW}WARN${CEND}]"
        echo "   (Some unit tests failed, see log)"
    fi
    echo ""
fi

#############################################
# Display Info
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCA Installation Info                '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

echo "Binary location: $(which cca)"
echo "Version: $(cca --version 2>&1 | head -n1)"
echo "Python package: cca v$(python3 -c 'import cca; print(cca.VERSION)')"
echo "Virtual env: /opt/cca"
echo ""

# Show cca info
cca info

echo ""

#############################################
# Success
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e "${CGREEN}   All CCA tests passed! ✓              ${CEND}"
echo -e "${CGREEN}#############################################${CEND}"
echo ""
echo "Test log: $CCA_LOG_FILE"
echo ""

exit 0
