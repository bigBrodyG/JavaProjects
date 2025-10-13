#!/usr/bin/env fish
# Fish shell aliases for Java Projects automation
# Source this file or add to your ~/.config/fish/config.fish

# Quick command to add new projects to the website
alias java-add-project="python3 (git rev-parse --show-toplevel)/.github/scripts/auto-add-project.py"

# Quick command to regenerate the website
alias java-gen-site="python3 (git rev-parse --show-toplevel)/.github/scripts/generate-site.py"

# Combined: compile, run, and show a project
function java-run
    if test (count $argv) -eq 0
        echo "Usage: java-run <ProjectName>"
        return 1
    end
    
    set project $argv[1]
    
    if not test -d $project
        echo "Error: Project '$project' not found"
        return 1
    end
    
    echo "🔨 Compiling $project..."
    javac -d $project/bin $project/src/*.java
    
    if test $status -eq 0
        echo "✅ Compilation successful"
        echo "▶️  Running..."
        echo ""
        java -cp $project/bin (basename $project/src/*.java .java | head -n1)
    else
        echo "❌ Compilation failed"
    end
end

echo "✅ Java Projects automation commands loaded!"
echo ""
echo "Available commands:"
echo "  java-add-project  - Automatically add new projects to website"
echo "  java-gen-site     - Regenerate the website"
echo "  java-run <name>   - Compile and run a project"
