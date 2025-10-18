#!/usr/bin/env bash
# CCA Alpha Purge Script bevore running Testing Script
# Based on CCC CODE tests/travis.sh pattern
# Usage:
#   sudo bash cca/tests/purge.sh           # Vorsicht: Löscht unwiederruflich alle vorhanden Web-Sites!!!!
#   sudo bash cca/tests/travis.sh          # Full test suite
#   sudo bash cca/tests/travis.sh --ci     # CI optimized

#echo "Cleaning up old test sites..."
#wo site list | while read site; do
#    wo site delete "$site" --no-prompt 2>/dev/null || true
#done

#!/usr/bin/env bash
#
# CCA Alpha Purge Script before running Testing Script
# Based on CCC CODE tests/travis.sh pattern
#
# Usage:
#   sudo bash cca/tests/purge.sh           # Vorsicht: Löscht unwiederruflich Test Web-Sites!!!!
#   sudo bash cca/tests/travis.sh          # Full test suite
#   sudo bash cca/tests/travis.sh --ci     # CI optimized
#

#!/usr/bin/env bash
#
# CCA Alpha Purge Script before running Testing Script
# Based on CCC CODE tests/travis.sh pattern
#
# Usage:
#   sudo bash cca/tests/purge.sh           # Vorsicht: Löscht unwiederruflich Test Web-Sites!!!!
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

# ==============================================================================
# TEST SITES ARRAY
# ==============================================================================
# Diese Sites werden vom travis.sh Testskript angelegt und können gelöscht werden
# Manuelle Sites werden NICHT gelöscht!
# ==============================================================================
TEST_SITES=(
    # Basic sites
    "html.net"
    "php.net"
    "mysql.net"
    
    # PHP version specific sites
    "php74.net"
    "php80.net"
    "php81.net"
    "php82.net"
    "php83.net"
    "php84.net"
    
    # WordPress sites with different cache backends
    "wp.net"
    "wpfc.net"
    "wpsc.net"
    "wpredis.net"
    "wpce.net"
    "wprocket.net"
    
    # WordPress Multisite
    "wpsubdomain.net"
    "wpsubdir.net"
    
    # Special configurations
    "ngxblocker.net"
    "proxy.net"
    "alias.net"
    
    # .io domain sites
    "wp.io"
    "wpsubdirwpfc.io"
    "wpsubdirwpsc.io"
    "wpsubdirwpce.io"
    "wpsubdirwprocket.io"
    "wpsubdirwpredis.io"
    "wpsubdomainwpfc.io"
    "wpsubdomainwpsc.io"
    "wpsubdomainwpce.io"
    "wpsubdomainwprocket.io"
    "wpsubdomainwpredis.io"
)

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

# Get all existing sites
mapfile -t EXISTING_SITES < <(wo site list 2>/dev/null)

# Create associative array for faster lookup
declare -A TEST_SITES_MAP
for site in "${TEST_SITES[@]}"; do
    TEST_SITES_MAP["$site"]=1
done

# Filter: Only test sites that actually exist
TO_DELETE=()
MANUAL_SITES=()

for site in "${EXISTING_SITES[@]}"; do
    # Skip empty lines
    [ -z "$site" ] && continue
    
    # Check if this site is in our test sites array
    if [[ -n "${TEST_SITES_MAP[$site]}" ]]; then
        TO_DELETE+=("$site")
    else
        MANUAL_SITES+=("$site")
    fi
done

# Check if there are test sites to delete
if [ ${#TO_DELETE[@]} -eq 0 ]; then
    echo -e "${GREEN}No test sites found. Nothing to delete.${NC}"
    
    if [ ${#MANUAL_SITES[@]} -gt 0 ]; then
        echo -e "${BLUE}Found ${#MANUAL_SITES[@]} manual site(s) (will NOT be deleted):${NC}"
        printf '%s\n' "${MANUAL_SITES[@]}" | sed 's/^/  - /'
    fi
    
    exit 0
fi

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
