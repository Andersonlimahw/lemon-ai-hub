#!/usr/bin/env bash
# ============================================================================
# Postman Generator — Newman Execution Helper
# ============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

usage() {
    echo "Usage: $0 run <collection_path> [environment_path]"
    echo "       $0 install"
    exit 1
}

check_newman() {
    if command -v newman &> /dev/null; then
        return 0
    else
        return 1
    fi
}

install_newman() {
    echo -e "${YELLOW}Newman not found in PATH.${NC}"
    
    # Try local package.json first
    if [ -f "package.json" ]; then
        echo -e "${CYAN}Found package.json. Installing newman as devDependency...${NC}"
        npm install --save-dev newman || true
    fi
    
    # Check if installed locally or via npx
    if command -v npx &> /dev/null; then
        echo -e "${GREEN}npx is available. Will use 'npx newman'.${NC}"
        return 0
    fi
    
    # Try global installation
    echo -e "${YELLOW}Attempting global installation of newman...${NC}"
    npm install -g newman || {
        echo -e "${RED}Global installation failed. Please install manually: npm install -g newman${NC}"
        exit 1
    }
}

run_tests() {
    local collection="$1"
    local env="${2:-}"
    
    if [ ! -f "$collection" ]; then
        echo -e "${RED}Error: Collection file not found at '$collection'${NC}"
        exit 1
    fi
    
    local cmd="newman"
    if ! check_newman; then
        if command -v npx &> /dev/null; then
            cmd="npx -y newman"
        else
            install_newman
        fi
    fi
    
    local run_args=("run" "$collection")
    if [ -n "$env" ]; then
        if [ ! -f "$env" ]; then
            echo -e "${RED}Error: Environment file not found at '$env'${NC}"
            exit 1
        fi
        run_args+=("-e" "$env")
    fi
    
    # Add beautiful CLI reporter configurations
    run_args+=("--color" "on")
    
    echo -e "${CYAN}🚀 Executing Postman tests via Newman...${NC}"
    echo -e "${CYAN}Command: $cmd ${run_args[*]}${NC}\n"
    
    $cmd "${run_args[@]}"
}

if [ $# -lt 1 ]; then
    usage
fi

cmd="$1"
shift

case "$cmd" in
    install)
        if check_newman; then
            echo -e "${GREEN}Newman is already installed: $(newman --version)${NC}"
        else
            install_newman
            echo -e "${GREEN}Newman setup completed successfully.${NC}"
        fi
        ;;
    run)
        if [ $# -lt 1 ]; then
            echo -e "${RED}Error: Collection file path is required.${NC}"
            usage
        fi
        run_tests "$@"
        ;;
    *)
        usage
        ;;
esac
