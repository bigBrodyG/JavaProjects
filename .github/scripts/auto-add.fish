#!/usr/bin/env fish
# Convenient wrapper script to auto-add Java projects to the website

set script_dir (dirname (status --current-filename))
set project_root (dirname (dirname $script_dir))

echo "🚀 Auto-adding Java projects to website..."
echo ""

cd $project_root
python3 .github/scripts/auto-add-project.py $argv
