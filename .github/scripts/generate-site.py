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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Fira+Code:wght@400;500&display=swap');
        
        :root {{
            --page-bg: #f4f6fb;
            --card-bg: #ffffff;
            --border: #e1e4ec;
            --text: #1f2937;
            --muted: #6b7280;
            --brand: #1f6feb;
            --brand-muted: #aac7ff;
            --success: #008a4e;
            --error: #b42318;
        }}
        
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0;
            min-height: 100vh;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--page-bg);
            color: var(--text);
            display: flex;
            flex-direction: column;
        }}
        
        header {{
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            padding: 20px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        header h1 {{
            font-size: 1.35rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        header h1 i {{
            color: var(--brand);
        }}
        
        .back-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 14px;
            border-radius: 6px;
            border: 1px solid var(--border);
            color: var(--text);
            text-decoration: none;
            font-size: 0.92rem;
            transition: background 0.2s ease;
        }}
        
        .back-btn:hover {{
            background: #f6f8fb;
        }}
        
        .container {{
            flex: 1;
            display: flex;
            border-top: 1px solid var(--border);
        }}
        
        .left-panel {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--card-bg);
            border-right: 1px solid var(--border);
        }}
        
        .tabs {{
            display: flex;
            padding: 0 16px;
            border-bottom: 1px solid var(--border);
            overflow-x: auto;
        }}
        
        .tab-button {{
            border: none;
            background: none;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            padding: 12px 16px;
            color: var(--muted);
            cursor: pointer;
            border-bottom: 2px solid transparent;
        }}
        
        .tab-button:hover {{
            color: var(--text);
        }}
        
        .tab-button.active {{
            color: var(--brand);
            border-color: var(--brand);
        }}
        
        .code-area {{
            position: relative;
            flex: 1;
            overflow: auto;
        }}
        
        .tab-content {{
            display: none;
            height: 100%;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        pre {{
            margin: 0;
        }}
        
        pre code {{
            display: block;
            padding: 20px !important;
            min-height: 100%;
            background: #0b1220 !important;
            color: #f3f4f6 !important;
            font-size: 14px;
        }}
        
        .copy-btn {{
            position: absolute;
            top: 16px;
            right: 16px;
            border: 1px solid var(--border);
            background: #fff;
            color: var(--text);
            border-radius: 5px;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 0.85rem;
        }}
        
        .copy-btn:hover {{
            border-color: var(--brand);
        }}
        
        .right-panel {{
            width: 40%;
            min-width: 360px;
            background: var(--card-bg);
            display: flex;
            flex-direction: column;
        }}
        
        .run-header {{
            padding: 18px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .run-header h2 {{
            font-size: 1rem;
        }}
        
        .run-btn {{
            border: 1px solid var(--brand);
            background: var(--brand);
            color: #fff;
            border-radius: 6px;
            padding: 8px 16px;
            cursor: pointer;
            font-weight: 500;
            font-size: 0.92rem;
            transition: opacity 0.2s ease;
        }}
        
        .run-btn:hover {{
            opacity: 0.9;
        }}
        
        .run-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .output-area {{
            padding: 24px;
            flex: 1;
            overflow: auto;
        }}
        
        .output-box {{
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 18px;
            min-height: 180px;
            font-family: 'Fira Code', monospace;
            font-size: 13px;
            white-space: pre-wrap;
            background: #fcfdff;
        }}
        
        .output-box.success {{
            border-color: var(--success);
            color: var(--success);
        }}
        
        .output-box.error {{
            border-color: var(--error);
            color: var(--error);
        }}
        
        .status-indicator {{
            font-size: 0.88rem;
            margin-bottom: 12px;
            padding: 8px 10px;
            border-radius: 6px;
            border: 1px solid var(--border);
            display: inline-flex;
            gap: 8px;
            align-items: center;
            color: var(--muted);
        }}
        
        .status-indicator.success {{
            color: var(--success);
            border-color: rgba(0, 138, 78, 0.4);
        }}
        
        .status-indicator.error {{
            color: var(--error);
            border-color: rgba(180, 35, 24, 0.4);
        }}
        
        .status-indicator.running {{
            color: var(--brand);
            border-color: rgba(31, 111, 235, 0.4);
        }}
        
        .spinner {{
            width: 1rem;
            height: 1rem;
            border-radius: 50%;
            border: 2px solid rgba(31, 111, 235, 0.2);
            border-top-color: var(--brand);
            animation: spin 0.6s linear infinite;
        }}
        
        @keyframes spin {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        .info-box {{
            border-left: 3px solid var(--brand);
            padding: 10px 14px;
            background: #f5f8ff;
            font-size: 0.88rem;
            color: var(--muted);
            margin-bottom: 14px;
        }}
        
        @media (max-width: 1024px) {{
            .container {{
                flex-direction: column;
            }}
            
            .right-panel {{
                width: 100%;
                min-width: auto;
                border-top: 1px solid var(--border);
            }}
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
        },
        {
            'name': '01_Verifica_teoria',
            'id': '01_verifica_teoria',
            'sources': ['01_Verifica_teoria/src/Main.java', '01_Verifica_teoria/src/SchedaSim.java', '01_Verifica_teoria/src/Telefonata.java'],
            'output': 'docs/01_verifica_teoria-output.txt',
            'compile': 'docs/01_verifica_teoria-compile.log',
            'description': 'Progetto 01_Verifica_teoria',
            'type': 'teoria'
        },
        {
            'name': '02_Verifica_lab',
            'id': '02_verifica_lab',
            'sources': ['02_Verifica_lab/src/MacchinaDistributrice.java', '02_Verifica_lab/src/Main.java', '02_Verifica_lab/src/Prodotto.java'],
            'output': 'docs/02_verifica_lab-output.txt',
            'compile': 'docs/02_verifica_lab-compile.log',
            'description': 'Progetto 02_Verifica_lab',
            'type': 'laboratorio'
        },
        {
            'name': 'Abbonamento',
            'id': 'abbonamento',
            'sources': ['Abbonamento/src/Cd.java', 'Abbonamento/src/Main.java', 'Abbonamento/src/PortaCD.java'],
            'output': 'docs/abbonamento-output.txt',
            'compile': 'docs/abbonamento-compile.log',
            'description': 'Progetto Abbonamento',
            'type': 'laboratorio'
        },
        {
            'name': 'Ereditarietà',
            'id': 'ereditarietà',
            'sources': ['Ereditarietà/src/Docente.java', 'Ereditarietà/src/Main.java', 'Ereditarietà/src/Persona.java', 'Ereditarietà/src/Studente.java'],
            'output': 'docs/ereditarietà-output.txt',
            'compile': 'docs/ereditarietà-compile.log',
            'description': 'Progetto Ereditarietà',
            'type': 'teoria'
        },
        {
            'name': 'Immobili',
            'id': 'immobili',
            'sources': ['Immobili/src/Abitazione.java', 'Immobili/src/Appartamento.java', 'Immobili/src/Test.java', 'Immobili/src/Villa.java'],
            'output': 'docs/immobili-output.txt',
            'compile': 'docs/immobili-compile.log',
            'description': 'Progetto Immobili',
            'type': 'laboratorio'
        },
        {
            'name': 'Playlist',
            'id': 'playlist',
            'sources': ['Playlist/src/Brano.java', 'Playlist/src/LibreriaMusicale.java', 'Playlist/src/Main.java'],
            'output': 'docs/playlist-output.txt',
            'compile': 'docs/playlist-compile.log',
            'description': 'Progetto Playlist',
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --page-bg: #f4f6fb;
            --surface: #ffffff;
            --border: #dce2ef;
            --text: #111827;
            --muted: #6b7280;
            --brand: #1f6feb;
            --brand-soft: #e1ecff;
            --theory: #0f9d58;
            --lab: #b45309;
        }}
        
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0;
            min-height: 100vh;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--page-bg);
            color: var(--text);
            padding: 48px 20px 72px;
        }}
        
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        
        .hero {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 32px;
            margin-bottom: 32px;
            box-shadow: 0 10px 35px rgba(15, 23, 42, 0.08);
            display: flex;
            flex-direction: column;
            gap: 18px;
        }}
        
        .hero .eyebrow {{
            font-size: 0.78rem;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            color: var(--muted);
            display: inline-flex;
            gap: 8px;
            align-items: center;
        }}
        
        .hero h1 {{
            margin: 0;
            font-size: 2.6rem;
            letter-spacing: -0.6px;
        }}
        
        .hero-subtitle {{
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.6;
            max-width: 640px;
        }}
        
        .hero-actions {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .button {{
            border-radius: 8px;
            padding: 10px 18px;
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid transparent;
            transition: background 0.2s ease, border 0.2s ease, color 0.2s ease;
        }}
        
        .button.primary {{
            background: var(--brand);
            color: #fff;
            border-color: var(--brand);
        }}
        
        .button.primary:hover {{
            opacity: 0.9;
        }}
        
        .button.ghost {{
            background: var(--brand-soft);
            color: var(--brand);
            border-color: var(--brand-soft);
        }}
        
        .button.ghost:hover {{
            border-color: var(--brand);
        }}
        
        .stats-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
            margin-top: 8px;
        }}
        
        .stats-card {{
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            background: #f9fbff;
        }}
        
        .stats-label {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: var(--muted);
        }}
        
        .stats-value {{
            font-size: 1.7rem;
            font-weight: 600;
            margin-top: 6px;
        }}
        
        .controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            margin-bottom: 28px;
        }}
        
        .filters {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .filter-button {{
            border-radius: 999px;
            border: 1px solid var(--border);
            background: #fff;
            color: var(--muted);
            padding: 8px 14px;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }}
        
        .filter-button span {{
            background: var(--brand-soft);
            border-radius: 999px;
            padding: 2px 8px;
            font-size: 0.8rem;
            color: var(--brand);
        }}
        
        .filter-button.active {{
            border-color: var(--brand);
            color: var(--brand);
        }}
        
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }}
        
        .project-card {{
            text-decoration: none;
            color: inherit;
            border: 1px solid var(--border);
            border-radius: 16px;
            background: var(--surface);
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            display: block;
        }}
        
        .project-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.1);
        }}
        
        .project-card.is-hidden {{
            opacity: 0;
            pointer-events: none;
        }}
        
        .card-glow {{
            display: none;
        }}
        
        .card-content {{
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        
        .card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .project-icon {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: grid;
            place-items: center;
            background: var(--brand-soft);
            color: var(--brand);
            font-size: 1.2rem;
        }}
        
        .project-icon.laboratorio {{
            background: #fef3c7;
            color: var(--lab);
        }}
        
        .status-pill {{
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border: 1px solid var(--border);
        }}
        
        .status-pill.success {{
            color: var(--lab);
            border-color: rgba(180, 83, 9, 0.35);
        }}
        
        .status-pill.theory {{
            color: var(--theory);
            border-color: rgba(15, 157, 88, 0.35);
        }}
        
        .card-content h2 {{
            margin: 0;
            font-size: 1.4rem;
        }}
        
        .card-description {{
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.5;
        }}
        
        .card-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9rem;
            color: var(--muted);
        }}
        
        .card-arrow {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border: 1px solid var(--border);
            display: grid;
            place-items: center;
        }}
        
        .view-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-weight: 600;
            color: var(--brand);
        }}
        
        .footer {{
            margin-top: 32px;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            background: var(--surface);
            text-align: center;
            color: var(--muted);
        }}
        
        .footer .social-links {{
            margin-top: 12px;
            display: flex;
            justify-content: center;
            gap: 14px;
        }}
        
        .footer .social-links a {{
            color: var(--brand);
            text-decoration: none;
        }}
        
        @media (max-width: 640px) {{
            body {{
                padding: 32px 16px 48px;
            }}
            
            .hero {{
                padding: 24px;
            }}
            
            .hero h1 {{
                font-size: 2rem;
            }}
            
            .projects-grid {{
                grid-template-columns: 1fr;
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
