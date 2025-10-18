#!/usr/bin/env bash
#
# CCA Alpha Purge Script before running Testing Script
# Based on CCC CODE tests/travis.sh pattern
#
# Usage:
#   sudo bash cca/tests/purge.sh           # Vorsicht: Löscht unwiederruflich Test Web-Sites!!!!
#   sudo bash cca/tests/purge.sh --debug   # Mit Debug-Output
#   sudo bash cca/tests/travis.sh          # Full test suite
#   sudo bash cca/tests/travis.sh --ci     # CI optimized
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Debug mode
DEBUG=false
if [[ "$1" == "--debug" ]]; then
    DEBUG=true
fi

debug_log() {
    if [[ "$DEBUG" == "true" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $*" >&2
    fi
}

# ==============================================================================
# TEST SITES ARRAY
# ==============================================================================
# Diese Sites werden vom travis.sh Testskript angelegt und können gelöscht werden
# Manuelle Sites werden NICHT gelöscht!
# ==============================================================================

# Alternative robustere Array-Definition ohne Kommentare dazwischen
TEST_SITES=()
TEST_SITES+=("html.net")
TEST_SITES+=("php.net")
TEST_SITES+=("mysql.net")
TEST_SITES+=("php74.net")
TEST_SITES+=("php80.net")
TEST_SITES+=("php81.net")
TEST_SITES+=("php82.net")
TEST_SITES+=("php83.net")
TEST_SITES+=("php84.net")
TEST_SITES+=("wp.net")
TEST_SITES+=("wpfc.net")
TEST_SITES+=("wpsc.net")
TEST_SITES+=("wpredis.net")
TEST_SITES+=("wpce.net")
TEST_SITES+=("wprocket.net")
TEST_SITES+=("wpsubdomain.net")
TEST_SITES+=("wpsubdir.net")
TEST_SITES+=("ngxblocker.net")
TEST_SITES+=("proxy.net")
TEST_SITES+=("alias.net")
TEST_SITES+=("wp.io")
TEST_SITES+=("wpsubdirwpfc.io")
TEST_SITES+=("wpsubdirwpsc.io")
TEST_SITES+=("wpsubdirwpce.io")
TEST_SITES+=("wpsubdirwprocket.io")
TEST_SITES+=("wpsubdirwpredis.io")
TEST_SITES+=("wpsubdomainwpfc.io")
TEST_SITES+=("wpsubdomainwpsc.io")
TEST_SITES+=("wpsubdomainwpce.io")
TEST_SITES+=("wpsubdomainwprocket.io")
TEST_SITES+=("wpsubdomainwpredis.io")

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Error: This script must be run as root${NC}" 
   exit 1
fi

# Check if WordOps is installed
if ! command -v wo &> /dev/null; then
    echo -e "${RED}Error: WordOps (wo) is not installed${NC}"
    exit 1
fi

debug_log "TEST_SITES array has ${#TEST_SITES[@]} entries"
debug_log "First 3 TEST_SITES: ${TEST_SITES[0]}, ${TEST_SITES[1]}, ${TEST_SITES[2]}"

# Function to check if a site is in the TEST_SITES array
is_test_site() {
    local site="$1"
    local test_site
    for test_site in "${TEST_SITES[@]}"; do
        if [[ "$site" == "$test_site" ]]; then
            return 0  # true - is a test site
        fi
    done
    return 1  # false - not a test site
}

# Function to clean site name from any formatting
clean_site_name() {
    local site="$1"
    # Remove ANSI color codes
    site=$(echo "$site" | sed 's/\x1b\[[0-9;]*m//g')
    # Remove all whitespace (spaces, tabs, newlines)
    site=$(echo "$site" | tr -d '[:space:]')
    # Remove any non-printable characters
    site=$(echo "$site" | tr -cd '[:print:]')
    echo "$site"
}

# Get all existing sites and separate test sites from manual sites
TO_DELETE=()
MANUAL_SITES=()

debug_log "Getting site list from 'wo site list'..."

if [[ "$DEBUG" == "true" ]]; then
    debug_log "Raw output with visible special chars:"
    wo site list 2>/dev/null | head -n 3 | cat -A >&2
fi

# Robustere Parsing-Methode
while IFS= read -r raw_site; do
    # Skip empty lines
    [[ -z "$raw_site" ]] && continue
    
    # Clean the site name
    site=$(clean_site_name "$raw_site")
    
    # Skip if still empty after cleaning
    [[ -z "$site" ]] && continue
    
    debug_log "Raw: '$raw_site' -> Cleaned: '$site' (length: ${#site})"
    
    # Check if this site is a test site
    if is_test_site "$site"; then
        TO_DELETE+=("$site")
        debug_log "  -> MATCH (test site)"
    else
        MANUAL_SITES+=("$site")
        debug_log "  -> NO MATCH (manual site)"
    fi
done < <(wo site list 2>/dev/null)

debug_log "Classification complete:"
debug_log "  Test sites to delete: ${#TO_DELETE[@]}"
debug_log "  Manual sites to preserve: ${#MANUAL_SITES[@]}"

if [[ "$DEBUG" == "true" ]]; then
    debug_log "TO_DELETE array contents:"
    for site in "${TO_DELETE[@]}"; do
        debug_log "  - '$site'"
    done
    debug_log "MANUAL_SITES array contents:"
    for site in "${MANUAL_SITES[@]}"; do
        debug_log "  - '$site'"
    done
fi

# Check if there are test sites to delete
if [ ${#TO_DELETE[@]} -eq 0 ]; then
    echo -e "${GREEN}No test sites found. Nothing to delete.${NC}"
    
    if [ ${#MANUAL_SITES[@]} -gt 0 ]; then
        echo -e "${BLUE}Found ${#MANUAL_SITES[@]} manual site(s) (will NOT be deleted):${NC}"
        printf '%s\n' "${MANUAL_SITES[@]}" | sed 's/^/  - /'
    fi
    
    exit 0
fi

# NOW display the warning with correct site lists
echo -e "${RED}═══════════════════════════════════════════════════════════${NC}"
echo -e "${RED}  WARNING: DESTRUCTIVE OPERATION${NC}"
echo -e "${RED}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}"
echo "This script will DELETE ONLY TEST SITES created by travis.sh!"
echo ""
echo "Test sites to be deleted:"
printf '%s\n' "${TO_DELETE[@]}" | sed 's/^/  - /'
echo ""
echo "What will be deleted for each test site:"
echo "  - Website files in /var/www/<testsite>/"
echo "  - Nginx configuration in /etc/nginx/sites-*/<testsite>"
echo "  - Databases (if created by WordOps)"
echo "  - SSL certificates"
echo ""
echo -e "${GREEN}✓ Manual sites in /var/www/ will be PRESERVED!${NC}"
echo -e "${GREEN}✓ Only sites listed in TEST_SITES array are affected!${NC}"
echo -e "${YELLOW}"
echo "This action CANNOT be undone!"
echo -e "${NC}"

# Display sites to be deleted
echo -e "${YELLOW}Found ${#TO_DELETE[@]} test site(s) to delete:${NC}"
printf '%s\n' "${TO_DELETE[@]}" | sed 's/^/  - /'
echo ""

# Show manual sites that will be preserved
if [ ${#MANUAL_SITES[@]} -gt 0 ]; then
    echo -e "${BLUE}Found ${#MANUAL_SITES[@]} manual site(s) that will be PRESERVED:${NC}"
    printf '%s\n' "${MANUAL_SITES[@]}" | sed 's/^/  ✓ /'
    echo ""
fi

# Sicherheitsnetz: Der SysOps muss exakt den Text eingeben
REQUIRED_CONFIRMATION="Yes, delete all test sites"

echo -e "${RED}To confirm deletion of ${#TO_DELETE[@]} test site(s), type exactly:${NC}"
echo -e "${GREEN}${REQUIRED_CONFIRMATION}${NC}"
echo ""
read -p "Confirmation: " USER_INPUT

if [ "$USER_INPUT" != "$REQUIRED_CONFIRMATION" ]; then
    echo -e "${RED}Confirmation does not match. Aborting.${NC}"
    echo -e "${YELLOW}You typed: '${USER_INPUT}'${NC}"
    echo -e "${YELLOW}Expected:  '${REQUIRED_CONFIRMATION}'${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Confirmation accepted. Starting deletion...${NC}"
echo ""

# Cleanup function
cleanup_sites() {
    local deleted=0
    local failed=0
    
    echo "Deleting test sites..."
    
    for site in "${TO_DELETE[@]}"; do
        echo -n "Deleting ${site}... "
        if wo site delete "$site" --no-prompt 2>/dev/null; then
            echo -e "${GREEN}OK${NC}"
            ((deleted++))
        else
            echo -e "${RED}FAILED${NC}"
            ((failed++))
        fi
    done
    
    echo ""
    echo -e "${GREEN}Deletion complete!${NC}"
    echo "  Successfully deleted: ${deleted} site(s)"
    
    if [ $failed -gt 0 ]; then
        echo -e "${YELLOW}  Failed: ${failed} site(s)${NC}"
    fi
    
    if [ ${#MANUAL_SITES[@]} -gt 0 ]; then
        echo -e "${BLUE}  Preserved (manual): ${#MANUAL_SITES[@]} site(s)${NC}"
    fi
}

# Execute cleanup
cleanup_sites

# Verify cleanup
echo -e "${GREEN}Verifying cleanup...${NC}"

# Check which test sites still remain
REMAINING_TEST_SITES=()
for site in "${TEST_SITES[@]}"; do
    if wo site info "$site" &>/dev/null; then
        REMAINING_TEST_SITES+=("$site")
    fi
done

if [ ${#REMAINING_TEST_SITES[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All test sites successfully removed${NC}"
else
    echo -e "${YELLOW}⚠ Warning: ${#REMAINING_TEST_SITES[@]} test site(s) still remain${NC}"
    echo "Remaining test sites:"
    printf '%s\n' "${REMAINING_TEST_SITES[@]}" | sed 's/^/  - /'
fi

# Show current status
echo ""
echo -e "${BLUE}Current site list:${NC}"
CURRENT_SITES=$(wo site list 2>/dev/null | wc -l)
if [ "$CURRENT_SITES" -eq 0 ]; then
    echo "  (no sites)"
else
    wo site list | sed 's/^/  - /'
fi

echo ""
echo -e "${GREEN}Purge script completed.${NC}"
