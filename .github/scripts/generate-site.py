#!/usr/bin/env python3
"""
Generate a static website showcasing Java projects with interactive execution
"""

import os
import json
from pathlib import Path

def read_file_safe(filepath):
    """Safely read a file, return empty string if not found"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def escape_html(text):
    """Escape HTML special characters"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

def escape_js(text):
    """Escape text for JavaScript strings"""
    return (text
            .replace('\\', '\\\\')
            .replace("'", "\\'")
            .replace('"', '\\"')
            .replace('\n', '\\n')
            .replace('\r', '\\r')
            .replace('\t', '\\t'))

def generate_project_page(project_name, source_files, output_file, compile_log, project_id):
    """Generate a standalone HTML page for a single project"""
    
    # Read all source code
    source_files_data = []
    main_code = ""
    for src_file in source_files:
        if os.path.exists(src_file):
            code = read_file_safe(src_file)
            filename = os.path.basename(src_file)
            source_files_data.append({
                'filename': filename,
                'code': code
            })
            if not main_code:
                main_code = code
    
    # Read output
    output = read_file_safe(output_file)
    
    # Read compile log
    compile_result = read_file_safe(compile_log)
    compile_status = "success" if not compile_result or "error:" not in compile_result.lower() else "error"
    
    # Generate tabs for multiple files
    tabs_html = ""
    content_html = ""
    for i, file_data in enumerate(source_files_data):
        active = "active" if i == 0 else ""
        tabs_html += f'''
            <button class="tab-button {active}" data-tab="{project_id}-tab{i}">{escape_html(file_data['filename'])}</button>
        '''
        content_html += f'''
            <div id="{project_id}-tab{i}" class="tab-content {active}">
                <pre><code class="language-java">{escape_html(file_data['code'])}</code></pre>
            </div>
        '''
    
    html = f'''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(project_name)} - Java Project</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/java.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            /* Palette scura moderna e accattivante */
            --bg-primary: #0a0e27;
            --bg-secondary: #151932;
            --bg-tertiary: #1e2642;
            --bg-card: linear-gradient(135deg, #1a1f3a 0%, #252b4a 100%);
            --bg-code: #0f1421;
            --text-primary: #f0f3ff;
            --text-secondary: #a0a8c0;
            --text-muted: #6b7599;
            --accent-primary: #00d4ff;
            --accent-secondary: #7c3aed;
            --accent-tertiary: #ff006e;
            --accent-success: #00ff88;
            --accent-warning: #ffd60a;
            --accent-error: #ff4757;
            --border-default: #2d3551;
            --border-accent: rgba(0, 212, 255, 0.3);
            --glow-primary: rgba(0, 212, 255, 0.4);
            --glow-secondary: rgba(124, 58, 237, 0.4);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.4);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.5);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.6);
            --shadow-glow: 0 0 20px var(--glow-primary);
        }}
        
        body {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        header {{
            background: var(--bg-secondary);
            padding: 20px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-light);
            box-shadow: var(--shadow-sm);
        }}
        
        header h1 {{
            font-size: 1.5em;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text-primary);
        }}
        
        header h1 i {{
            color: var(--accent-primary);
        }}
        
        .back-btn {{
            background: var(--bg-primary);
            color: var(--text-primary);
            border: 1px solid var(--border-light);
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .back-btn:hover {{
            background: var(--accent-primary);
            color: white;
            border-color: var(--accent-primary);
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }}
        
        .container {{
            display: flex;
            flex: 1;
            overflow: hidden;
            background: var(--bg-primary);
        }}
        
        .left-panel {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-light);
        }}
        
        .tabs {{
            display: flex;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-light);
            padding: 0 16px;
            overflow-x: auto;
        }}
        
        .tab-button {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 12px 20px;
            cursor: pointer;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            white-space: nowrap;
            transition: all 0.2s ease;
            font-family: 'Fira Code', monospace;
            border: 1px solid transparent;
        }}
        
        .tab-button:hover {{
            color: var(--text-primary);
            background: var(--bg-secondary);
            border-color: var(--border-accent);
        }}
        
        .tab-button.active {{
            color: var(--accent-primary);
            background: var(--bg-primary);
            border-color: var(--accent-primary);
            box-shadow: 0 0 12px var(--glow-primary);
        }}
        
        .code-area {{
            flex: 1;
            overflow: auto;
            position: relative;
        }}
        
        .tab-content {{
            display: none;
            height: 100%;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .tab-content pre {{
            margin: 0;
            height: 100%;
        }}
        
        .tab-content pre code {{
            display: block;
            padding: 24px !important;
            background: var(--bg-code) !important;
            height: 100%;
            font-size: 14px;
            line-height: 1.6;
            font-family: 'Fira Code', 'Consolas', monospace;
            color: var(--text-primary) !important;
        }}
        
        .right-panel {{
            width: 45%;
            display: flex;
            flex-direction: column;
            background: var(--bg-secondary);
            border-left: 2px solid var(--border-default);
        }}
        
        .run-header {{
            background: var(--bg-tertiary);
            padding: 16px 24px;
            border-bottom: 2px solid var(--border-default);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .run-header h2 {{
            font-size: 1em;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .run-btn {{
            background: var(--accent-primary);
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
        }}
        
        .run-btn:hover {{
            background: var(--accent-secondary);
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }}
        
        .run-btn:active {{
            transform: translateY(0);
        }}
        
        .run-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }}
        
        .output-area {{
            flex: 1;
            padding: 24px;
            overflow: auto;
            background: var(--bg-primary);
        }}
        
        .output-box {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: 12px;
            padding: 20px;
            min-height: 200px;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 13px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: var(--text-primary);
            box-shadow: var(--shadow-sm);
        }}
        
        .output-box.error {{
            color: #dc2626;
            background: #fef2f2;
            border-color: #fecaca;
        }}
        
        .output-box.success {{
            color: var(--accent-success);
        }}
        
        .status-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 16px;
        }}
        
        .status-indicator.success {{
            background: rgba(0, 255, 136, 0.15);
            color: var(--accent-success);
            border: 1px solid var(--accent-success);
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
        }}
        
        .status-indicator.error {{
            background: rgba(255, 71, 87, 0.15);
            color: var(--accent-error);
            border: 1px solid var(--accent-error);
            box-shadow: 0 0 10px rgba(255, 71, 87, 0.3);
        }}
        
        .status-indicator.running {{
            background: rgba(0, 212, 255, 0.15);
            color: var(--accent-primary);
            border: 1px solid var(--accent-primary);
            box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        }}
        
        .spinner {{
            border: 2px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top: 2px solid currentColor;
            width: 14px;
            height: 14px;
            animation: spin 0.6s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .info-box {{
            background: #ede9fe;
            border-left: 3px solid var(--accent-primary);
            padding: 12px 16px;
            margin-bottom: 16px;
            border-radius: 8px;
            font-size: 13px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .info-box i {{
            color: var(--accent-primary);
        }}
        
        @media (max-width: 1024px) {{
            .container {{
                flex-direction: column;
            }}
            
            .right-panel {{
                width: 100%;
                border-left: none;
                border-top: 1px solid var(--border-light);
            }}
        }}
        
        .copy-btn {{
            position: absolute;
            top: 12px;
            right: 12px;
            background: var(--accent-primary);
            color: white;
            border: none;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            opacity: 0;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
        }}
        
        .code-area:hover .copy-btn {{
            opacity: 1;
        }}
        
        .copy-btn:hover {{
            background: var(--accent-secondary);
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }}
    </style>
</head>
<body>
    <header>
        <h1>
            <i class="fas fa-coffee"></i>
            {escape_html(project_name)}
        </h1>
        <a href="index.html" class="back-btn">
            <i class="fas fa-arrow-left"></i>
            Tutti i Progetti
        </a>
    </header>
    
    <div class="container">
        <div class="left-panel">
            <div class="tabs">
                {tabs_html}
            </div>
            <div class="code-area" id="codeArea">
                {content_html}
                <button class="copy-btn" onclick="copyCode()">
                    <i class="fas fa-copy"></i> Copia
                </button>
            </div>
        </div>
        
        <div class="right-panel">
            <div class="run-header">
                <h2>
                    <i class="fas fa-terminal"></i>
                    Output
                </h2>
                <button class="run-btn" onclick="runCode()" id="runBtn">
                    <i class="fas fa-play"></i>
                    Esegui
                </button>
            </div>
            <div class="output-area">
                <div id="statusIndicator"></div>
                <div class="output-box" id="output">{escape_html(output) if output else 'Nessun output ancora...'}</div>
            </div>
        </div>
    </div>
    
    <script>
        // Project data
        const sourceCode = {json.dumps([f['code'] for f in source_files_data], ensure_ascii=False)};
        const projectName = {json.dumps(project_name, ensure_ascii=False)};
        const buildStatus = {json.dumps(compile_status, ensure_ascii=False)};
        const precompiledOutput = {json.dumps(output, ensure_ascii=False)};
        
        // Tab switching functionality
        function switchTab(tabId) {{
            console.log('Switching to tab:', tabId);
            
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.tab-button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // Show selected tab
            const selectedTab = document.getElementById(tabId);
            if (selectedTab) {{
                selectedTab.classList.add('active');
            }}
            
            // Mark button as active
            const clickedButton = document.querySelector(`[data-tab="${{tabId}}"]`);
            if (clickedButton) {{
                clickedButton.classList.add('active');
            }}
            
            // Re-highlight
            hljs.highlightAll();
        }}
        
        // Add click handlers to tab buttons
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelectorAll('.tab-button').forEach(button => {{
                button.addEventListener('click', function() {{
                    const tabId = this.getAttribute('data-tab');
                    switchTab(tabId);
                }});
            }});
        }});
        
        function copyCode() {{
            const activeTab = document.querySelector('.tab-content.active code');
            if (activeTab) {{
                navigator.clipboard.writeText(activeTab.textContent);
                const btn = document.querySelector('.copy-btn');
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Copiato!';
                setTimeout(() => {{
                    btn.innerHTML = originalText;
                }}, 2000);
            }}
        }}
        
        async function runCode() {{
            console.log('runCode called');
            const runBtn = document.getElementById('runBtn');
            const output = document.getElementById('output');
            const statusIndicator = document.getElementById('statusIndicator');
            
            // Disable button
            runBtn.disabled = true;
            runBtn.innerHTML = '<div class="spinner"></div> Esecuzione...';
            
            // Show running status
            statusIndicator.innerHTML = '<div class="status-indicator running"><div class="spinner"></div> Esecuzione in corso...</div>';
            output.className = 'output-box';
            output.textContent = '';
            
            // Simulate compilation and execution with animation
            await new Promise(resolve => setTimeout(resolve, 500));
            
            // Show the pre-compiled output with typing effect
            statusIndicator.innerHTML = '<div class="status-indicator success"><i class="fas fa-check-circle"></i> Eseguito con successo</div>';
            output.className = 'output-box success';
            
            // Type out the output character by character
            let i = 0;
            const outputText = precompiledOutput;
            const typeSpeed = 2; // milliseconds per character
            
            function typeWriter() {{
                if (i < outputText.length) {{
                    output.textContent += outputText.charAt(i);
                    i++;
                    setTimeout(typeWriter, typeSpeed);
                }} else {{
                    // Re-enable button when done
                    runBtn.disabled = false;
                    runBtn.innerHTML = '<i class="fas fa-redo"></i> Ri-esegui';
                }}
            }}
            
            typeWriter();
        }}
        
        // Initialize syntax highlighting
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('DOM Content Loaded');
            
            // Highlight code
            hljs.highlightAll();
            
            // Show precompiled status
            const statusIndicator = document.getElementById('statusIndicator');
            if (buildStatus === 'success') {{
                statusIndicator.innerHTML = 
                    '<div class="status-indicator success"><i class="fas fa-check-circle"></i> Compilato con successo</div>';
            }} else {{
                statusIndicator.innerHTML = 
                    '<div class="status-indicator error"><i class="fas fa-times-circle"></i> Errori di compilazione</div>';
            }}
            
            console.log('Initialization complete');
        }});
    </script>
</body>
</html>'''
    
    return html

def main():
    """Generate the complete website"""
    
    projects = [
        {
            'name': 'Cerchio',
            'id': 'cerchio',
            'sources': ['Cerchio/src/Cerchio.java'],
            'output': 'docs/cerchio-output.txt',
            'compile': 'docs/cerchio-compile.log',
            'description': 'Classe per calcolare area e circonferenza di un cerchio',
            'type': 'teoria'
        },
        {
            'name': 'mergeArray',
            'id': 'mergearray',
            'sources': ['mergeArray/src/mergeArrays.java'],
            'output': 'docs/mergearray-output.txt',
            'compile': 'docs/mergearray-compile.log',
            'description': 'Unione e ordinamento di array',
            'type': 'laboratorio'
        },
        {
            'name': 'OggettoCD',
            'id': 'oggettocd',
            'sources': ['OggettoCD/src/Cd.java'],
            'output': 'docs/oggettocd-output.txt',
            'compile': 'docs/oggettocd-compile.log',
            'description': 'Gestione di un catalogo CD',
            'type': 'laboratorio'
        },
        {
            'name': 'Punto',
            'id': 'punto',
            'sources': ['Punto/src/Punto.java'],
            'output': 'docs/punto-output.txt',
            'compile': 'docs/punto-compile.log',
            'description': 'Rappresentazione di un punto nel piano cartesiano',
            'type': 'teoria'
        },
        {
            'name': 'Rettangolo',
            'id': 'rettangolo',
            'sources': ['Rettangolo/src/Punto.java', 'Rettangolo/src/Rettangolo.java'],
            'output': 'docs/rettangolo-output.txt',
            'compile': 'docs/rettangolo-compile.log',
            'description': 'Calcolo di vertici e proprietà di un rettangolo',
            'type': 'laboratorio'
        },
        {
            'name': 'vocalcount',
            'id': 'vocalcount',
            'sources': ['vocalcount/src/voc_count.java'],
            'output': 'docs/vocalcount-output.txt',
            'compile': 'docs/vocalcount-compile.log',
            'description': 'Conteggio delle vocali in una stringa',
            'type': 'laboratorio'
        },
        {
            'name': 'Libro',
            'id': 'Libro',
            'sources': ['Libro/src/Libro.java'],
            'output': 'docs/Libro-output.txt',
            'compile': 'docs/Libro-compile.log',
            'description': 'Classe per parsing di libro',
            'type': 'teoria'
        }
 
    ]
    
    # Create docs directory
    os.makedirs('docs', exist_ok=True)
    
    # Generate individual project pages
    for project in projects:
        project_html = generate_project_page(
            project['name'],
            project['sources'],
            project['output'],
            project['compile'],
            project['id']
        )
        
        with open(f"docs/{project['id']}.html", 'w', encoding='utf-8') as f:
            f.write(project_html)
        
        print(f"✅ Generated page for {project['name']}")
    
    # Generate index page with project cards
    project_cards = ""
    for project in projects:
        # Determine badge based on project type
        badge_class = "success" if project['type'] == 'laboratorio' else "theory"
        badge_icon = "🔬" if project['type'] == 'laboratorio' else "📚"
        badge_text = project['type'].capitalize()
        
        project_cards += f'''
        <a href="{project['id']}.html" class="project-card">
            <div class="card-header">
                <h2>{escape_html(project['name'])}</h2>
                <span class="status-badge {badge_class}">
                    {badge_icon} {badge_text}
                </span>
            </div>
            <p class="card-description">{escape_html(project['description'])}</p>
            <div class="card-footer">
                <span class="view-link">
                    Visualizza ed Esegui
                    <i class="fas fa-arrow-right"></i>
                </span>
            </div>
        </a>
        '''
    
    # Generate index.html
    index_html = f'''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Java Projects Showcase</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            /* Palette scura moderna e accattivante */
            --bg-primary: #0a0e27;
            --bg-secondary: #151932;
            --bg-tertiary: #1e2642;
            --text-primary: #f0f3ff;
            --text-secondary: #a0a8c0;
            --text-muted: #6b7599;
            --accent-primary: #00d4ff;
            --accent-secondary: #7c3aed;
            --accent-tertiary: #ff006e;
            --accent-success: #00ff88;
            --accent-warning: #ffd60a;
            --accent-error: #ff4757;
            --border-default: #2d3551;
            --border-accent: rgba(0, 212, 255, 0.3);
            --glow-primary: rgba(0, 212, 255, 0.4);
            --glow-secondary: rgba(124, 58, 237, 0.4);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.4);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.5);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.6);
            --shadow-glow: 0 0 20px var(--glow-primary);
        }}
        
        body {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 60px;
            padding: 40px 20px;
        }}
        
        h1 {{
            font-size: 3.5em;
            margin-bottom: 12px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 50%, var(--accent-tertiary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -1.5px;
            text-shadow: 0 0 40px var(--glow-primary);
        }}
        
        h1 .emoji {{
            display: inline-block;
            animation: bounce 2s ease-in-out infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        }}
        
        .subtitle {{
            font-size: 1.25em;
            color: var(--text-primary);
            margin-bottom: 100px;
            font-weight: 500;
            opacity: 0.9;
        }}
        
        .github-link {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
            padding: 16px 36px;
            border-radius: 12px;
            color: var(--text-primary);
            text-decoration: none;
            transition: all 0.3s ease;
            border: 2px solid var(--border-default);
            font-weight: 600;
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
            margin: 16px;
        }}
        
        .github-link::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, var(--glow-primary), transparent);
            transition: left 0.5s;
        }}
        
        .github-link:hover::before {{
            left: 100%;
        }}
        
        .github-link:hover {{
            border-color: var(--accent-primary);
            transform: translateY(-3px);
            box-shadow: var(--shadow-glow), var(--shadow-lg);
            color: var(--accent-primary);
        }}
        
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 24px;
            margin-bottom: 60px;
        }}
        
        .project-card {{
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            border-radius: 20px;
            padding: 32px;
            text-decoration: none;
            color: inherit;
            display: block;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 2px solid var(--border-default);
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
        }}
        
        .project-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, var(--glow-primary) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.5s ease;
        }}
        
        .project-card:hover::before {{
            opacity: 0.15;
        }}
        
        .project-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 16px 48px rgba(0, 212, 255, 0.25), 0 0 40px var(--glow-secondary);
            border-color: var(--accent-primary);
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 18px;
            gap: 12px;
            position: relative;
            z-index: 1;
        }}
        
        .card-header h2 {{
            font-size: 1.7em;
            flex: 1;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            color: transparent;
        }}
        
        .status-badge {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 600;
            white-space: nowrap;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .status-badge.success {{
            background: rgba(0, 255, 136, 0.15);
            color: var(--accent-success);
            border: 2px solid var(--accent-success);
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
        }}
        
        .status-badge.theory {{
            background: rgba(255, 215, 0, 0.15);
            color: #ffd700;
            border: 2px solid #ffd700;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
        }}
        
        .status-badge.error {{
            background: rgba(255, 71, 87, 0.15);
            color: var(--accent-error);
            border: 2px solid var(--accent-error);
            box-shadow: 0 0 15px rgba(255, 71, 87, 0.4);
        }}
        
        .card-description {{
            color: var(--text-primary);
            font-size: 1em;
            line-height: 1.7;
            margin-bottom: 24px;
            min-height: 48px;
            position: relative;
            z-index: 1;
            opacity: 0.85;
        }}
        
        .card-footer {{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            padding-top: 20px;
            border-top: 2px solid var(--border-default);
            position: relative;
            z-index: 1;
        }}
        
        .view-link {{
            color: var(--accent-primary);
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .project-card:hover .view-link {{
            gap: 14px;
            color: var(--accent-secondary);
            text-shadow: 0 0 10px var(--glow-secondary);
        }}
        
        footer {{
            text-align: center;
            color: var(--text-secondary);
            padding: 40px 20px;
            margin-top: 60px;
            border-top: 2px solid var(--border-default);
        }}
        
        footer a {{
            color: var(--accent-primary);
            text-decoration: none;
            font-weight: 700;
            transition: all 0.3s;
            position: relative;
        }}
        
        footer a:hover {{
            color: var(--accent-secondary);
            text-shadow: 0 0 10px var(--glow-secondary);
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2.5em;
            }}
            
            .projects-grid {{
                grid-template-columns: 1fr;
            }}
            
            body {{
                padding: 20px 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Java homeworks and exercises</h1>
            <p class="subtitle">My own showcase for all my exercises in Java ICT class. <br></p>
            <a href="https://github.com/bigBrodyG/JavaProjects" class="github-link">
                <i class="fab fa-github"></i>
                View on GitHub
            </a>
        </header>
        
        <div class="projects-grid">
            {project_cards}
        </div>
        
        <footer>
            <p style="margin-top: 10px;">
                <a href="https://github.com/bigBrodyG/JavaProjects">bigBrodyG/JavaProjects</a>
            </p>
        </footer>
    </div>
</body>
</html>'''
    
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("✅ Index page generated successfully")
    print(f"✅ Total: {len(projects)} project pages + index")

if __name__ == '__main__':
    main()
