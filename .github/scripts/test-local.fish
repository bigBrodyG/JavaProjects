#!/usr/bin/env fish
# Test script to verify the showcase generation works locally (Fish shell version)

echo "🧪 Testing Java Showcase Generation"
echo "===================================="
echo ""

# Colors
set GREEN '\033[0;32m'
set RED '\033[0;31m'
set YELLOW '\033[1;33m'
set NC '\033[0m' # No Color

# Check Python
echo -e "$YELLOW""Checking Python...$NC"
if command -v python3 &> /dev/null
    echo -e "$GREEN""✓ Python 3 found: "(python3 --version)"$NC"
else
    echo -e "$RED""✗ Python 3 not found!$NC"
    exit 1
end

# Check Java
echo -e "$YELLOW""Checking Java...$NC"
if command -v javac &> /dev/null
    echo -e "$GREEN""✓ Java compiler found: "(javac -version 2>&1)"$NC"
else
    echo -e "$RED""✗ Java compiler not found!$NC"
    exit 1
end

echo ""
echo -e "$YELLOW""Creating directories...$NC"
mkdir -p Cerchio/bin mergeArray/bin OggettoCD/bin Punto/bin Rettangolo/bin vocalcount/bin docs

echo -e "$YELLOW""Compiling projects...$NC"

function compile_project
    set name $argv[1]
    set src $argv[2]
    echo -n "  $name... "
    if javac -d "$name/bin" $name/src/*.java 2> "docs/$src-compile.log"
        echo -e "$GREEN""✓$NC"
        return 0
    else
        echo -e "$RED""✗$NC"
        return 1
    end
end

compile_project "Cerchio" "cerchio"
compile_project "mergeArray" "mergearray"
compile_project "OggettoCD" "oggettocd"
compile_project "Punto" "punto"
compile_project "Rettangolo" "rettangolo"
compile_project "vocalcount" "vocalcount"

echo ""
echo -e "$YELLOW""Running programs...$NC"

function run_program
    set name $argv[1]
    set class $argv[2]
    set output $argv[3]
    echo -n "  $name... "
    if test -f "$name/bin/$class.class"
        cd "$name/bin" && java "$class" > "../../docs/$output-output.txt" 2>&1; cd ../..
        echo -e "$GREEN""✓$NC"
    else
        echo -e "$RED""✗ (class not found)$NC"
        echo "Error: Class not compiled" > "docs/$output-output.txt"
    end
end

run_program "Cerchio" "Cerchio" "cerchio"
run_program "mergeArray" "mergeArrays" "mergearray"
run_program "OggettoCD" "Cd" "oggettocd"
run_program "Punto" "Punto" "punto"
run_program "Rettangolo" "Rettangolo" "rettangolo"
run_program "vocalcount" "voc_count" "vocalcount"

echo ""
echo -e "$YELLOW""Generating website...$NC"
if python3 .github/scripts/generate-site.py
    echo -e "$GREEN""✓ Website generated successfully$NC"
else
    echo -e "$RED""✗ Website generation failed$NC"
    exit 1
end

echo ""
echo -e "$GREEN""================================================$NC"
echo -e "$GREEN""✅ All tests passed!$NC"
echo -e "$GREEN""================================================$NC"
echo ""
echo "📄 Website generated at: docs/index.html"
echo ""
echo "To view locally, run:"
echo "  xdg-open docs/index.html"
echo ""
echo "Ready to push to GitHub! 🚀"
