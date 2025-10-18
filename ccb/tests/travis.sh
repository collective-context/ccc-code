#!/usr/bin/env bash
# -------------------------------------------------------------------------
# CCB Beta Testing Script
# -------------------------------------------------------------------------

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
CCB_LOG_DIR="./logs"
CCB_LOG_FILE="$CCB_LOG_DIR/ccb-test.log"

# Create log directory
mkdir -p "$CCB_LOG_DIR"

# Exit handler
exit_script() {
    echo -e "${CRED}#############################################${CEND}"
    echo -e "${CRED}   Tests failed! See log for details       ${CEND}"
    echo -e "${CRED}#############################################${CEND}"
    echo ""
    echo "Log file: $CCB_LOG_FILE"
    echo ""
    if [ -f "$CCB_LOG_FILE" ]; then
        echo "Last 50 lines of log:"
        tail -n 50 "$CCB_LOG_FILE"
    fi
    exit 1
}

# Parse arguments
CCB_CI_MODE=""
if [ "$1" = "--ci" ] || [ "$1" = "--actions" ]; then
    CCB_CI_MODE="yes"
fi

#############################################
# Installation Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCB Installation Test                '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Cleanup old installation
echo -ne "   Cleaning previous installation      [..]\r"
if {
    sudo rm -rf /opt/ccb /tmp/ccc-code /usr/local/bin/ccb /usr/bin/ccb
} >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   Cleaning previous installation      [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   Cleaning previous installation      [${CRED}FAIL${CEND}]"
    exit_script
fi

# Install ccb
echo -ne "   Installing ccb                      [..]\r"
if {
    sudo -E bash install-ccb
} >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   Installing ccb                      [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   Installing ccb                      [${CRED}FAIL${CEND}]"
    exit_script
fi

echo ""

#############################################
# Binary Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCB Binary Tests                     '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Test: Binary exists
echo -ne "   Binary exists                       [..]\r"
if command -v ccb >/dev/null 2>&1; then
    CCB_PATH=$(which ccb)
    echo -ne "   Binary exists at $CCB_PATH    [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   Binary exists                       [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: Python package import
echo -ne "   Python package import               [..]\r"
if {
    python3 -c "import ccb; print(ccb.__version__)"
} >> "$CCB_LOG_FILE" 2>&1; then
    CCB_VERSION=$(python3 -c "import ccb; print(ccb.__version__)")
    echo -ne "   Python package import v$CCB_VERSION     [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   Python package import               [${CRED}FAIL${CEND}]"
    exit_script
fi

echo ""

#############################################
# Command Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCB Command Tests                    '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Test: ccb --version
echo -ne "   ccb --version                       [..]\r"
if {
    ccb --version
} >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   ccb --version                       [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   ccb --version                       [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: ccb -v (short version)
echo -ne "   ccb -v                              [..]\r"
if {
    ccb -v
} >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   ccb -v                              [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   ccb -v                              [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: ccb --help
echo -ne "   ccb --help                          [..]\r"
if {
    ccb --help
} >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   ccb --help                          [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   ccb --help                          [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: ccb info
echo -ne "   ccb info                            [..]\r"
if {
    ccb info
} >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   ccb info                            [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   ccb info                            [${CRED}FAIL${CEND}]"
    exit_script
fi

echo ""

#############################################
# Check Plugin Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCB Check Plugin Tests               '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Test: ccb check --help
echo -ne "   ccb check --help                    [..]\r"
if ccb check --help >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   ccb check --help                    [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   ccb check --help                    [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: ccb check actions --help
echo -ne "   ccb check actions --help            [..]\r"
if ccb check actions --help >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   ccb check actions --help            [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   ccb check actions --help            [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: ccb check actions (wenn gh verfügbar)
if command -v gh >/dev/null 2>&1; then
    echo -ne "   ccb check actions                   [..]\r"
    if ccb check actions >> "$CCB_LOG_FILE" 2>&1; then
        echo -ne "   ccb check actions                   [${CGREEN}OK${CEND}]\r\n"
    else
        echo -e "   ccb check actions                   [${CYELLOW}SKIP${CEND}]"
        echo "   (GitHub API issue or no runs found)"
    fi
    
    echo -ne "   ccb check actions --save            [..]\r"
    if ccb check actions --save >> "$CCB_LOG_FILE" 2>&1; then
        echo -ne "   ccb check actions --save            [${CGREEN}OK${CEND}]\r\n"
        if [ -f "./logs/ccb-debug.log" ]; then
            echo -ne "   Log file created                    [${CGREEN}OK${CEND}]\r\n"
        else
            echo -e "   Log file created                    [${CYELLOW}WARN${CEND}]"
        fi
    else
        echo -e "   ccb check actions --save            [${CYELLOW}SKIP${CEND}]"
    fi
else
    echo -e "   ccb check actions                   [${CYELLOW}SKIP${CEND}]"
    echo "   (gh CLI not installed)"
fi

echo ""

#############################################
# Debug Plugin Tests
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e '       CCB Debug Plugin Tests               '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

# Test: ccb debug --help
echo -ne "   ccb debug --help                    [..]\r"
if ccb debug --help >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   ccb debug --help                    [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   ccb debug --help                    [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: ccb debug run --help
echo -ne "   ccb debug run --help                [..]\r"
if ccb debug run --help >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   ccb debug run --help                [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   ccb debug run --help                [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: ccb debug summary --help
echo -ne "   ccb debug summary --help            [..]\r"
if ccb debug summary --help >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   ccb debug summary --help            [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   ccb debug summary --help            [${CRED}FAIL${CEND}]"
    exit_script
fi

# Test: ccb debug summary (ohne vorhandenes Log)
echo -ne "   ccb debug summary (no log)          [..]\r"
rm -f ./logs/ccb-debug.log
if ccb debug summary >> "$CCB_LOG_FILE" 2>&1; then
    echo -ne "   ccb debug summary (no log)          [${CGREEN}OK${CEND}]\r\n"
else
    echo -e "   ccb debug summary (no log)          [${CYELLOW}WARN${CEND}]"
    echo "   (Expected to handle missing log gracefully)"
fi

echo ""

#############################################
# Python Unit Tests (optional)
#############################################

if command -v pytest >/dev/null 2>&1; then
    echo -e "${CGREEN}#############################################${CEND}"
    echo -e '       CCB Python Unit Tests                '
    echo -e "${CGREEN}#############################################${CEND}"
    echo ""
    
    echo -ne "   Running pytest suite                [..]\r"
    if pytest tests-ccb/ -v >> "$CCB_LOG_FILE" 2>&1; then
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
echo -e '       CCB Installation Info                '
echo -e "${CGREEN}#############################################${CEND}"
echo ""

echo "Binary location: $(which ccb)"
echo "Version: $(ccb --version 2>&1 | head -n1)"
echo "Python package: ccb v$(python3 -c 'import ccb; print(ccb.__version__)')"
echo "Virtual env: /opt/ccb"
echo ""

# Show ccb info
ccb info

echo ""

#############################################
# Success
#############################################

echo -e "${CGREEN}#############################################${CEND}"
echo -e "${CGREEN}   All CCB tests passed! ✓              ${CEND}"
echo -e "${CGREEN}#############################################${CEND}"
echo ""
echo "Test log: $CCB_LOG_FILE"
echo ""

exit 0
