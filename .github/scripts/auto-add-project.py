#!/usr/bin/env python3
"""
Automatically detect and add new Java projects to the website.
This script:
1. Scans for project directories with src/ folders
2. Compiles and runs the Java code
3. Captures the output
4. Adds the project to generate-site.py
5. Regenerates the website
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def find_java_projects():
    """Find all directories that look like Java projects."""
    projects = []
    workspace_root = Path.cwd()
    
    for item in workspace_root.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            src_dir = item / 'src'
            if src_dir.exists() and src_dir.is_dir():
                # Check if it has .java files
                java_files = list(src_dir.glob('*.java'))
                if java_files:
                    projects.append(item.name)
    
    return sorted(projects)

def find_main_class(src_dir):
    """Find the class with the main method."""
    for java_file in src_dir.glob('*.java'):
        with open(java_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'public static void main' in content:
                return java_file.stem
    return None

def compile_and_run_project(project_name):
    """Compile and run a Java project, return output and status."""
    project_path = Path(project_name)
    src_path = project_path / 'src'
    bin_path = project_path / 'bin'
    
    # Create bin directory
    bin_path.mkdir(exist_ok=True)
    
    # Get all Java files
    java_files = list(src_path.glob('*.java'))
    if not java_files:
        return None, "No Java files found", False
    
    # Compile
    compile_cmd = ['javac', '-d', str(bin_path)] + [str(f) for f in java_files]
    compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
    
    if compile_result.returncode != 0:
        return None, compile_result.stderr, False
    
    # Find main class
    main_class = find_main_class(src_path)
    if not main_class:
        return None, "No main class found", False
    
    # Run
    run_cmd = ['java', '-cp', str(bin_path), main_class]
    run_result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=10)
    
    success = run_result.returncode == 0
    output = run_result.stdout if success else run_result.stderr
    
    return output, compile_result.stderr if compile_result.stderr else "", success

def get_project_info_from_generate_site():
    """Parse generate-site.py to get existing project IDs."""
    script_path = Path('.github/scripts/generate-site.py')
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the projects list - need to match the complete array
    # Look for projects = [ ... ] where ] is at the start of a line
    projects_match = re.search(r'projects = \[(.*?)^\s*\]', content, re.DOTALL | re.MULTILINE)
    if not projects_match:
        return []
    
    projects_section = projects_match.group(1)
    
    # Extract project IDs (more reliable than names for duplicate detection)
    existing_ids = []
    for match in re.finditer(r"'id':\s*'([^']+)'", projects_section):
        existing_ids.append(match.group(1))
    
    return existing_ids

def add_project_to_generate_site(project_name, project_type='teoria'):
    """Add a new project entry to generate-site.py."""
    script_path = Path('.github/scripts/generate-site.py')
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all source files for this project
    src_path = Path(project_name) / 'src'
    source_files = [f"{project_name}/src/{f.name}" for f in sorted(src_path.glob('*.java'))]
    
    # Generate description based on project name
    description = f"Progetto {project_name}"
    
    # Create the new project entry
    new_project = f'''        {{
            'name': '{project_name}',
            'id': '{project_name.lower()}',
            'sources': {source_files},
            'output': 'docs/{project_name.lower()}-output.txt',
            'compile': 'docs/{project_name.lower()}-compile.log',
            'description': '{description}',
            'type': '{project_type}'
        }}'''
    
    # Find the end of the projects list and add before it
    # Look for the last closing brace followed by whitespace and the closing bracket
    pattern = r'(\s+\}\s*)\n(\s+\])'
    
    # Add a comma to the last entry and insert the new one
    replacement = r'\1,\n' + new_project + r'\n\2'
    new_content = re.sub(pattern, replacement, content)
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def save_project_output(project_name, output, compile_log):
    """Save the output and compile log for a project."""
    docs_path = Path('docs')
    docs_path.mkdir(exist_ok=True)
    
    # Save output
    output_file = docs_path / f'{project_name.lower()}-output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output if output else "")
    
    # Save compile log
    log_file = docs_path / f'{project_name.lower()}-compile.log'
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(compile_log if compile_log else "")
    
    print(f"  📄 Saved output to {output_file}")
    print(f"  📄 Saved compile log to {log_file}")

def run_generate_site():
    """Run the generate-site.py script."""
    result = subprocess.run(
        ['python3', '.github/scripts/generate-site.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("\n✅ Website regenerated successfully!")
        print(result.stdout)
        return True
    else:
        print("\n❌ Error regenerating website:")
        print(result.stderr)
        return False

def prompt_project_type():
    """Ask user for project type."""
    while True:
        response = input("  Is this a 'teoria' or 'laboratorio' project? [t/l] (default: t): ").strip().lower()
        if response in ['', 't', 'teoria']:
            return 'teoria'
        elif response in ['l', 'lab', 'laboratorio']:
            return 'laboratorio'
        else:
            print("  Please enter 't' for teoria or 'l' for laboratorio")

def main():
    """Main function to auto-add projects."""
    print("🔍 Scanning for Java projects...\n")
    
    # Find all Java projects
    all_projects = find_java_projects()
    
    if not all_projects:
        print("❌ No Java projects found in the workspace.")
        return
    
    print(f"Found {len(all_projects)} project(s):")
    for p in all_projects:
        print(f"  - {p}")
    print()
    
    # Get existing projects from generate-site.py
    existing_projects = get_project_info_from_generate_site()
    # Convert project names to IDs for comparison
    existing_ids = set(existing_projects)  # existing_projects now contains IDs
    all_project_ids = {p.lower() for p in all_projects}
    
    # Map back to original names for display
    existing_names = [p for p in all_projects if p.lower() in existing_ids]
    
    print(f"📋 Already in website: {len(existing_names)} project(s)")
    for p in existing_names:
        print(f"  ✓ {p}")
    print()
    
    # Find new projects (by ID)
    new_projects = [p for p in all_projects if p.lower() not in existing_ids]
    
    if not new_projects:
        print("✨ All projects are already in the website!")
        print("\n🔄 Regenerating website anyway to ensure everything is up to date...")
        run_generate_site()
        return
    
    print(f"🆕 Found {len(new_projects)} new project(s) to add:")
    for p in new_projects:
        print(f"  + {p}")
    print()
    
    # Process each new project
    for project_name in new_projects:
        print(f"📦 Processing: {project_name}")
        
        # Compile and run
        print(f"  ⚙️  Compiling and running...")
        output, compile_log, success = compile_and_run_project(project_name)
        
        if success:
            print(f"  ✅ Compilation and execution successful!")
            if output:
                print(f"  📤 Output preview:")
                preview = output[:200] + "..." if len(output) > 200 else output
                for line in preview.split('\n')[:5]:
                    print(f"     {line}")
        else:
            print(f"  ⚠️  Warning: Compilation or execution had issues")
            if compile_log:
                print(f"  📋 Compile log: {compile_log[:100]}...")
        
        # Save output and logs
        save_project_output(project_name, output, compile_log)
        
        # Ask for project type
        project_type = prompt_project_type()
        
        # Add to generate-site.py
        print(f"  📝 Adding to generate-site.py...")
        add_project_to_generate_site(project_name, project_type)
        print(f"  ✅ Added {project_name} to site configuration\n")
    
    # Regenerate the website
    print("🔄 Regenerating website...\n")
    run_generate_site()
    
    print("\n" + "="*60)
    print("🎉 All done! New projects have been added to the website!")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
