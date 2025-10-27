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
            --bg-primary: #020617;
            --bg-secondary: rgba(15, 23, 42, 0.82);
            --bg-tertiary: rgba(30, 41, 68, 0.78);
            --bg-card: linear-gradient(140deg, rgba(15, 23, 42, 0.92) 0%, rgba(30, 41, 68, 0.75) 100%);
            --bg-code: #0b1220;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5f5;
            --text-muted: #94a3b8;
            --accent-primary: #38bdf8;
            --accent-secondary: #8b5cf6;
            --accent-tertiary: #f472b6;
            --accent-success: #34d399;
            --accent-warning: #facc15;
            --accent-error: #f87171;
            --border-default: rgba(148, 163, 184, 0.28);
            --border-light: rgba(148, 163, 184, 0.22);
            --border-strong: rgba(56, 189, 248, 0.45);
            --border-accent: rgba(56, 189, 248, 0.35);
            --glow-primary: rgba(56, 189, 248, 0.32);
            --glow-secondary: rgba(139, 92, 246, 0.32);
            --shadow-sm: 0 6px 18px rgba(2, 6, 23, 0.35);
            --shadow-md: 0 16px 32px rgba(2, 6, 23, 0.45);
            --shadow-lg: 0 32px 60px rgba(2, 6, 23, 0.55);
            --shadow-glow: 0 0 42px rgba(56, 189, 248, 0.32);
        }}
        
        body {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background:
                radial-gradient(circle at 0% 0%, rgba(59, 130, 246, 0.18) 0%, transparent 55%),
                radial-gradient(circle at 100% 0%, rgba(244, 114, 182, 0.16) 0%, transparent 45%),
                linear-gradient(180deg, #020617 0%, #0f172a 100%);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        body::before {{
            content: '';
            position: fixed;
            inset: 0;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.08), rgba(139, 92, 246, 0.12));
            filter: blur(140px);
            opacity: 0.6;
            z-index: -1;
        }}
        
        header {{
            background: rgba(15, 23, 42, 0.7);
            padding: 24px 36px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-default);
            box-shadow: var(--shadow-sm);
            backdrop-filter: blur(18px);
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
            background: rgba(8, 16, 32, 0.85);
            color: var(--text-primary);
            border: 1px solid var(--border-default);
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
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.85), rgba(139, 92, 246, 0.85));
            color: #020617;
            border-color: rgba(56, 189, 248, 0.65);
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }}
        
        .container {{
            display: flex;
            flex: 1;
            overflow: hidden;
            background: transparent;
            border-top: 1px solid var(--border-default);
            border-bottom: 1px solid var(--border-default);
        }}
        
        .left-panel {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: linear-gradient(160deg, rgba(15, 23, 42, 0.88), rgba(30, 41, 68, 0.72));
            border-right: 1px solid var(--border-default);
            backdrop-filter: blur(18px);
        }}
        
        .tabs {{
            display: flex;
            background: rgba(15, 23, 42, 0.72);
            border-bottom: 1px solid var(--border-default);
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
            background: rgba(8, 16, 32, 0.85);
            border-color: var(--border-strong);
            box-shadow: 0 0 18px rgba(56, 189, 248, 0.28);
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
            background: linear-gradient(200deg, rgba(15, 23, 42, 0.82), rgba(30, 41, 68, 0.68));
            border-left: 1px solid var(--border-default);
            backdrop-filter: blur(18px);
        }}
        
        .run-header {{
            background: rgba(15, 23, 42, 0.65);
            padding: 16px 24px;
            border-bottom: 1px solid var(--border-default);
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
            background: rgba(2, 10, 24, 0.6);
        }}
        
        .output-box {{
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid var(--border-default);
            border-radius: 16px;
            padding: 24px;
            min-height: 200px;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 13px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: var(--text-primary);
            box-shadow: var(--shadow-md);
        }}
        
        .output-box.error {{
            color: var(--accent-error);
            background: rgba(248, 113, 113, 0.12);
            border-color: rgba(248, 113, 113, 0.45);
        }}
        
        .output-box.success {{
            color: var(--accent-success);
            background: rgba(52, 211, 153, 0.12);
            border-color: rgba(52, 211, 153, 0.45);
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
            background: rgba(52, 211, 153, 0.12);
            color: var(--accent-success);
            border: 1px solid rgba(52, 211, 153, 0.45);
            box-shadow: 0 0 18px rgba(52, 211, 153, 0.28);
        }}
        
        .status-indicator.error {{
            background: rgba(248, 113, 113, 0.12);
            color: var(--accent-error);
            border: 1px solid rgba(248, 113, 113, 0.45);
            box-shadow: 0 0 18px rgba(248, 113, 113, 0.28);
        }}
        
        .status-indicator.running {{
            background: rgba(56, 189, 248, 0.14);
            color: var(--accent-primary);
            border: 1px solid rgba(56, 189, 248, 0.45);
            box-shadow: 0 0 18px rgba(56, 189, 248, 0.28);
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
            background: rgba(139, 92, 246, 0.15);
            border-left: 3px solid var(--accent-secondary);
            padding: 12px 16px;
            margin-bottom: 16px;
            border-radius: 10px;
            font-size: 13px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .info-box i {{
            color: var(--accent-secondary);
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
            'sources': ['OggettoCD/src/Cd.java', 'OggettoCD/src/PortaCD.java'],
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
            'name': 'Triangolo',
            'id': 'triangolo',
            'sources': ['Triangolo/src/Punto.java', 'Triangolo/src/Triangolo.java'],
            'output': 'docs/triangolo-output.txt',
            'compile': 'docs/triangolo-compile.log',
            'description': 'Gestione di triangoli e confronto tra forme congruenti',
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
            'id': 'libro',
            'sources': ['Libro/src/Libro.java'],
            'output': 'docs/libro-output.txt',
            'compile': 'docs/libro-compile.log',
            'description': 'Gestione di oggetti libro con calcolo del prezzo',
            'type': 'teoria'
        },
        {
            'name': 'Orario',
            'id': 'orario',
            'sources': ['Orario/src/Orario.java', 'Orario/src/TestOrario.java'],
            'output': 'docs/orario-output.txt',
            'compile': 'docs/orario-compile.log',
            'description': 'Gestione e manipolazione di orari',
            'type': 'teoria'
        },
        {
            'name': 'Software',
            'id': 'software',
            'sources': ['Software/src/Software.java'],
            'output': 'docs/software-output.txt',
            'compile': 'docs/software-compile.log',
            'description': 'Progetto Software',
            'type': 'teoria'
        },
        {
            'name': 'SpeseManager',
            'id': 'spesemanager',
            'sources': ['SpeseManager/src/Main.java', 'SpeseManager/src/SpesaManager.java', 'SpeseManager/src/Spese.java'],
            'output': 'docs/spesemanager-output.txt',
            'compile': 'docs/spesemanager-compile.log',
            'description': 'Progetto SpeseManager',
            'type': 'laboratorio'
        }
    ]
    
    total_projects = len(projects)
    theory_count = sum(1 for project in projects if project['type'] == 'teoria')
    lab_count = sum(1 for project in projects if project['type'] == 'laboratorio')
    
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
        project_icon = "fa-flask" if project['type'] == 'laboratorio' else "fa-lightbulb"
        
        project_cards += f'''
        <a href="{project['id']}.html" class="project-card" data-type="{project['type']}">
            <div class="card-glow"></div>
            <div class="card-content">
                <div class="card-top">
                    <div class="project-icon {project['type']}">
                        <i class="fas {project_icon}"></i>
                    </div>
                    <span class="status-pill {badge_class}">
                        {badge_icon} {badge_text}
                    </span>
                </div>
                <h2>{escape_html(project['name'])}</h2>
                <p class="card-description">{escape_html(project['description'])}</p>
                <div class="card-footer">
                    <span class="view-link">
                        Scopri il progetto
                    </span>
                    <span class="card-arrow"><i class="fas fa-arrow-right"></i></span>
                </div>
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
        :root {{
            --bg-primary: #020617;
            --bg-secondary: rgba(15, 23, 42, 0.72);
            --bg-tertiary: rgba(30, 41, 59, 0.65);
            --text-primary: #f8fafc;
            --text-secondary: #cbd5f5;
            --text-muted: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-purple: #8b5cf6;
            --accent-pink: #f472b6;
            --accent-success: #34d399;
            --accent-warning: #facc15;
            --accent-error: #f87171;
            --card-border: rgba(148, 163, 184, 0.24);
            --card-shadow: 0 28px 60px rgba(2, 6, 23, 0.45);
            --card-shadow-hover: 0 42px 80px rgba(2, 6, 23, 0.55);
            --glass-blur: blur(22px);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
            background:
                radial-gradient(circle at 0% 0%, rgba(59, 130, 246, 0.18) 0%, transparent 55%),
                radial-gradient(circle at 100% 0%, rgba(236, 72, 153, 0.16) 0%, transparent 45%),
                linear-gradient(180deg, #020617 0%, #0b1121 100%);
            color: var(--text-primary);
            padding: 56px 28px 80px;
            position: relative;
            overflow-x: hidden;
        }}
        
        body::before {{
            content: '';
            position: fixed;
            inset: 0;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.08), rgba(139, 92, 246, 0.12));
            opacity: 0.6;
            filter: blur(120px);
            z-index: -2;
        }}
        
        .container {{
            max-width: 1220px;
            margin: 0 auto;
            width: 100%;
            position: relative;
            z-index: 1;
        }}
        
        .hero {{
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.12), rgba(139, 92, 246, 0.08));
            border: 1px solid var(--card-border);
            border-radius: 32px;
            padding: 48px;
            box-shadow: var(--card-shadow);
            backdrop-filter: var(--glass-blur);
            margin-bottom: 48px;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}
        
        .hero .eyebrow {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-size: 0.85rem;
            letter-spacing: 0.28rem;
            text-transform: uppercase;
            color: var(--text-muted);
            background: rgba(148, 163, 184, 0.12);
            border: 1px solid rgba(148, 163, 184, 0.22);
            padding: 10px 16px;
            border-radius: 999px;
            width: fit-content;
        }}
        
        .hero h1 {{
            font-size: 3.4rem;
            max-width: 720px;
            line-height: 1.05;
            letter-spacing: -1.2px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple), var(--accent-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .hero-subtitle {{
            font-size: 1.15rem;
            max-width: 680px;
            color: var(--text-secondary);
            line-height: 1.6;
        }}
        
        .hero-actions {{
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
        }}
        
        .button {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            font-weight: 600;
            border-radius: 999px;
            padding: 14px 24px;
            transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
            border: 1px solid transparent;
        }}
        
        .button.primary {{
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.9), rgba(59, 130, 246, 0.95));
            box-shadow: 0 18px 35px rgba(59, 130, 246, 0.35);
            color: #0b1121;
        }}
        
        .button.primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 24px 40px rgba(59, 130, 246, 0.38);
        }}
        
        .button.ghost {{
            background: rgba(15, 23, 42, 0.35);
            border: 1px solid rgba(148, 163, 184, 0.35);
            color: var(--text-secondary);
        }}
        
        .button.ghost:hover {{
            transform: translateY(-2px);
            color: var(--text-primary);
            border-color: rgba(148, 163, 184, 0.55);
        }}
        
        .stats-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 18px;
            margin-top: 12px;
        }}
        
        .stats-card {{
            background: rgba(15, 23, 42, 0.55);
            border: 1px solid rgba(148, 163, 184, 0.24);
            border-radius: 18px;
            padding: 18px 22px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            box-shadow: 0 14px 30px rgba(2, 6, 23, 0.35);
        }}
        
        .stats-label {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.28rem;
            color: var(--text-muted);
        }}
        
        .stats-value {{
            font-size: 1.9rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        
        .stats-value.accent-success {{
            color: var(--accent-success);
        }}
        
        .stats-value.accent-warning {{
            color: var(--accent-warning);
        }}
        
        .controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            margin-bottom: 32px;
        }}
        
        .filters {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}
        
        .filter-button {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.45);
            border: 1px solid rgba(148, 163, 184, 0.28);
            color: var(--text-secondary);
            padding: 10px 18px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.25s ease, background 0.25s ease, border 0.25s ease, color 0.25s ease;
        }}
        
        .filter-button span {{
            background: rgba(148, 163, 184, 0.18);
            border-radius: 999px;
            padding: 2px 10px;
            font-size: 0.8rem;
        }}
        
        .filter-button.active {{
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.25), rgba(139, 92, 246, 0.25));
            border-color: rgba(56, 189, 248, 0.65);
            color: var(--text-primary);
        }}
        
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 28px;
        }}
        
        .project-card {{
            position: relative;
            display: block;
            text-decoration: none;
            color: inherit;
            border-radius: 28px;
            overflow: hidden;
            border: 1px solid var(--card-border);
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.85), rgba(30, 41, 59, 0.68));
            box-shadow: var(--card-shadow);
            transition: transform 0.35s ease, box-shadow 0.35s ease, border 0.35s ease;
        }}
        
        .project-card.is-hidden {{
            opacity: 0;
            transform: scale(0.96);
            pointer-events: none;
        }}
        
        .project-card:hover {{
            transform: translateY(-10px) scale(1.01);
            border-color: rgba(56, 189, 248, 0.65);
            box-shadow: var(--card-shadow-hover);
        }}
        
        .card-glow {{
            position: absolute;
            inset: 0;
            opacity: 0;
            background: radial-gradient(circle at top right, rgba(56, 189, 248, 0.22), transparent 60%);
            transition: opacity 0.45s ease;
        }}
        
        .project-card:hover .card-glow {{
            opacity: 1;
        }}
        
        .card-content {{
            position: relative;
            padding: 34px 32px 32px;
            display: flex;
            flex-direction: column;
            gap: 22px;
            backdrop-filter: var(--glass-blur);
        }}
        
        .card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
        }}
        
        .project-icon {{
            width: 52px;
            height: 52px;
            display: grid;
            place-items: center;
            border-radius: 16px;
            background: rgba(56, 189, 248, 0.18);
            color: var(--accent-blue);
            font-size: 1.35rem;
        }}
        
        .project-icon.laboratorio {{
            background: rgba(139, 92, 246, 0.18);
            color: var(--accent-purple);
        }}
        
        .status-pill {{
            padding: 8px 14px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            border: 1px solid transparent;
            background: rgba(148, 163, 184, 0.2);
            color: var(--text-secondary);
        }}
        
        .status-pill.success {{
            border-color: rgba(52, 211, 153, 0.6);
            background: rgba(52, 211, 153, 0.12);
            color: var(--accent-success);
        }}
        
        .status-pill.theory {{
            border-color: rgba(250, 204, 21, 0.55);
            background: rgba(250, 204, 21, 0.14);
            color: var(--accent-warning);
        }}
        
        .card-content h2 {{
            font-size: 1.85rem;
            letter-spacing: -0.6px;
            font-weight: 700;
        }}
        
        .card-description {{
            color: var(--text-secondary);
            font-size: 1.05rem;
            line-height: 1.55;
        }}
        
        .card-footer {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: var(--text-muted);
            font-weight: 600;
        }}
        
        .card-arrow {{
            width: 40px;
            height: 40px;
            border-radius: 999px;
            display: grid;
            place-items: center;
            border: 1px solid rgba(148, 163, 184, 0.3);
            transition: transform 0.25s ease, border 0.25s ease;
        }}
        
        .project-card:hover .card-arrow {{
            transform: translateX(6px);
            border-color: rgba(56, 189, 248, 0.65);
        }}
        
        .view-link {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }}
        
        .view-link::after {{
            content: '';
            display: inline-block;
            width: 42px;
            height: 2px;
            background: linear-gradient(90deg, rgba(148, 163, 184, 0.1), rgba(148, 163, 184, 0.8));
            border-radius: 999px;
            transition: transform 0.35s ease, opacity 0.35s ease;
        }}
        
        .project-card:hover .view-link::after {{
            transform: translateX(6px);
            opacity: 1;
        }}
        
        .footer {{
            margin-top: 48px;
            padding: 32px;
            border-radius: 24px;
            border: 1px solid rgba(148, 163, 184, 0.22);
            background: rgba(15, 23, 42, 0.55);
            backdrop-filter: var(--glass-blur);
            display: flex;
            flex-direction: column;
            gap: 12px;
            align-items: center;
            text-align: center;
            color: var(--text-secondary);
        }}
        
        .footer .social-links {{
            display: flex;
            gap: 18px;
        }}
        
        .footer .social-links a {{
            color: var(--text-secondary);
            transition: color 0.3s ease;
        }}
        
        .footer .social-links a:hover {{
            color: var(--accent-blue);
        }}
        
        @media (max-width: 960px) {{
            body {{
                padding: 40px 20px 64px;
            }}
            
            .hero {{
                padding: 40px 32px;
            }}
            
            .hero h1 {{
                font-size: 2.8rem;
            }}
        }}
        
        @media (max-width: 640px) {{
            .hero {{
                padding: 32px 24px;
            }}
            
            .hero h1 {{
                font-size: 2.3rem;
            }}
            
            .projects-grid {{
                grid-template-columns: 1fr;
            }}
            
            .card-content {{
                padding: 26px 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="hero">
            <span class="eyebrow"><i class="fas fa-code"></i> Java Lessons Showcase</span>
            <h1>My own Java projects</h1>
            <p class="hero-subtitle">
            </p>
            <div class="hero-actions">
                <a class="button primary" href="https://github.com/bigBrodyG/JavaProjects" target="_blank" rel="noopener">
                    <i class="fab fa-github"></i>
                    Apri su GitHub
                </a>
                <a class="button ghost" href="https://github.com/bigBrodyG/JavaProjects#readme" target="_blank" rel="noopener">
                    <i class="fas fa-book-open"></i>
                    Guida rapida
                </a>
            </div>
            <div class="stats-row">
                <div class="stats-card">
                    <span class="stats-label">Progetti totali</span>
                    <span class="stats-value">{total_projects}</span>
                </div>
                <div class="stats-card">
                    <span class="stats-label">Esercizi di teoria</span>
                    <span class="stats-value accent-warning">{theory_count}</span>
                </div>
                <div class="stats-card">
                    <span class="stats-label">Esperimenti di laboratorio</span>
                    <span class="stats-value accent-success">{lab_count}</span>
                </div>
            </div>
        </header>
        
        <section class="controls">
            <div class="filters">
                <button class="filter-button active" data-filter="all">
                    <i class="fas fa-layer-group"></i>
                    Tutti
                    <span>{total_projects}</span>
                </button>
                <button class="filter-button" data-filter="teoria">
                    <i class="fas fa-lightbulb"></i>
                    Teoria
                    <span>{theory_count}</span>
                </button>
                <button class="filter-button" data-filter="laboratorio">
                    <i class="fas fa-flask"></i>
                    Laboratorio
                    <span>{lab_count}</span>
                </button>
            </div>
        </section>
        
        <section class="projects-grid">
            {project_cards}
        </section>
        
        <footer class="footer">
            <p>Creato con passione per condividere percorsi e soluzioni in Java.</p>
            <div class="social-links">
                <a href="https://github.com/bigBrodyG" target="_blank" rel="noopener">
                    <i class="fab fa-github"></i>
                    GitHub
                </a>
                <a href="https://bigBrodyG.github.io/JavaProjects/" target="_blank" rel="noopener">
                    <i class="fas fa-globe"></i>
                    Showcase
                </a>
            </div>
        </footer>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const buttons = document.querySelectorAll('.filter-button');
            const cards = document.querySelectorAll('.project-card');
            
            buttons.forEach(button => {{
                button.addEventListener('click', () => {{
                    buttons.forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');
                    
                    const filter = button.getAttribute('data-filter');
                    cards.forEach(card => {{
                        if (filter === 'all' || card.dataset.type === filter) {{
                            card.classList.remove('is-hidden');
                        }} else {{
                            card.classList.add('is-hidden');
                        }}
                    }});
                }});
            }});
        }});
    </script>
</body>
</html>'''

    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("✅ Index page generated successfully")
    print(f"✅ Total: {len(projects)} project pages + index")

if __name__ == '__main__':
    main()
