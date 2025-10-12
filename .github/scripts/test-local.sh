#!/bin/bash
# Test script to verify the showcase generation works locally

set -e  # Exit on error

echo "🧪 Testing Java Showcase Generation"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "${YELLOW}Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"
else
    echo -e "${RED}✗ Python 3 not found!${NC}"
    exit 1
fi

# Check Java
echo -e "${YELLOW}Checking Java...${NC}"
if command -v javac &> /dev/null; then
    echo -e "${GREEN}✓ Java compiler found: $(javac -version 2>&1)${NC}"
else
    echo -e "${RED}✗ Java compiler not found!${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Creating directories...${NC}"
mkdir -p Cerchio/bin mergeArray/bin OggettoCD/bin Punto/bin Rettangolo/bin vocalcount/bin docs

echo -e "${YELLOW}Compiling projects...${NC}"

compile_project() {
    local name=$1
    local src=$2
    echo -n "  $name... "
    if javac -d "$name/bin" $name/src/*.java 2> "docs/${src}-compile.log"; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        return 1
    fi
}

compile_project "Cerchio" "cerchio"
compile_project "mergeArray" "mergearray"
compile_project "OggettoCD" "oggettocd"
compile_project "Punto" "punto"
compile_project "Rettangolo" "rettangolo"
compile_project "vocalcount" "vocalcount"

echo ""
echo -e "${YELLOW}Running programs...${NC}"

run_program() {
    local name=$1
    local class=$2
    local output=$3
    echo -n "  $name... "
    if [ -f "$name/bin/$class.class" ]; then
        (cd "$name/bin" && java "$class" > "../../docs/${output}-output.txt" 2>&1)
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗ (class not found)${NC}"
        echo "Error: Class not compiled" > "docs/${output}-output.txt"
    fi
}

run_program "Cerchio" "Cerchio" "cerchio"
run_program "mergeArray" "mergeArrays" "mergearray"
run_program "OggettoCD" "Cd" "oggettocd"
run_program "Punto" "Punto" "punto"
run_program "Rettangolo" "Rettangolo" "rettangolo"
run_program "vocalcount" "voc_count" "vocalcount"

echo ""
echo -e "${YELLOW}Generating website...${NC}"
if python3 .github/scripts/generate-site.py; then
    echo -e "${GREEN}✓ Website generated successfully${NC}"
else
    echo -e "${RED}✗ Website generation failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✅ All tests passed!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "📄 Website generated at: docs/index.html"
echo ""
echo "To view locally, open docs/index.html in your browser:"
echo "  Linux:   xdg-open docs/index.html"
echo "  macOS:   open docs/index.html"
echo "  Windows: start docs/index.html"
echo ""
echo "Ready to push to GitHub! 🚀"
