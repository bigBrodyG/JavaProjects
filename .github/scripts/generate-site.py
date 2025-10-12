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
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #1e1e1e;
            color: #d4d4d4;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        
        header h1 {{
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .back-btn {{
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            transition: background 0.3s;
        }}
        
        .back-btn:hover {{
            background: rgba(255,255,255,0.3);
        }}
        
        .container {{
            display: flex;
            flex: 1;
            overflow: hidden;
        }}
        
        .left-panel {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #252526;
            border-right: 1px solid #3e3e42;
        }}
        
        .tabs {{
            display: flex;
            background: #2d2d30;
            border-bottom: 1px solid #3e3e42;
            overflow-x: auto;
        }}
        
        .tab-button {{
            background: transparent;
            border: none;
            color: #969696;
            padding: 12px 20px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            font-size: 13px;
            white-space: nowrap;
            transition: all 0.2s;
        }}
        
        .tab-button:hover {{
            color: #d4d4d4;
            background: #2a2d2e;
        }}
        
        .tab-button.active {{
            color: white;
            border-bottom-color: #667eea;
            background: #1e1e1e;
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
            padding: 20px !important;
            background: #1e1e1e !important;
            height: 100%;
            font-size: 14px;
            line-height: 1.6;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        }}
        
        .right-panel {{
            width: 500px;
            display: flex;
            flex-direction: column;
            background: #1e1e1e;
        }}
        
        .run-header {{
            background: #2d2d30;
            padding: 15px 20px;
            border-bottom: 1px solid #3e3e42;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .run-header h2 {{
            font-size: 1.1em;
            color: #cccccc;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .run-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .run-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
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
            padding: 20px;
            overflow: auto;
            background: #1e1e1e;
        }}
        
        .output-box {{
            background: #0e0e0e;
            border: 1px solid #3e3e42;
            border-radius: 8px;
            padding: 15px;
            min-height: 200px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #d4d4d4;
        }}
        
        .output-box.error {{
            color: #f48771;
            border-color: #f48771;
        }}
        
        .output-box.success {{
            color: #4ec9b0;
        }}
        
        .status-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 15px;
            border-radius: 5px;
            font-size: 13px;
            margin-bottom: 15px;
        }}
        
        .status-indicator.success {{
            background: rgba(78, 201, 176, 0.1);
            color: #4ec9b0;
            border: 1px solid rgba(78, 201, 176, 0.3);
        }}
        
        .status-indicator.error {{
            background: rgba(244, 135, 113, 0.1);
            color: #f48771;
            border: 1px solid rgba(244, 135, 113, 0.3);
        }}
        
        .status-indicator.running {{
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            border: 1px solid rgba(102, 126, 234, 0.3);
        }}
        
        .spinner {{
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            border-top: 2px solid #667eea;
            width: 16px;
            height: 16px;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .info-box {{
            background: #2d2d30;
            border-left: 3px solid #667eea;
            padding: 12px 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            font-size: 13px;
            color: #cccccc;
        }}
        
        @media (max-width: 1024px) {{
            .container {{
                flex-direction: column;
            }}
            
            .right-panel {{
                width: 100%;
                border-left: none;
                border-top: 1px solid #3e3e42;
            }}
        }}
        
        .copy-btn {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(102, 126, 234, 0.8);
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            opacity: 0;
            transition: opacity 0.2s, background 0.2s;
        }}
        
        .code-area:hover .copy-btn {{
            opacity: 1;
        }}
        
        .copy-btn:hover {{
            background: rgba(102, 126, 234, 1);
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
                <div class="info-box">
                    <i class="fas fa-info-circle"></i>
                    Il codice è già compilato ed eseguito. Premi "Esegui" per vedere l'output animato.
                </div>
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
            'description': 'Classe per calcolare area e circonferenza di un cerchio'
        },
        {
            'name': 'mergeArray',
            'id': 'mergearray',
            'sources': ['mergeArray/src/mergeArrays.java'],
            'output': 'docs/mergearray-output.txt',
            'compile': 'docs/mergearray-compile.log',
            'description': 'Unione e ordinamento di array'
        },
        {
            'name': 'OggettoCD',
            'id': 'oggettocd',
            'sources': ['OggettoCD/src/Cd.java'],
            'output': 'docs/oggettocd-output.txt',
            'compile': 'docs/oggettocd-compile.log',
            'description': 'Gestione di un catalogo CD'
        },
        {
            'name': 'Punto',
            'id': 'punto',
            'sources': ['Punto/src/Punto.java'],
            'output': 'docs/punto-output.txt',
            'compile': 'docs/punto-compile.log',
            'description': 'Rappresentazione di un punto nel piano cartesiano'
        },
        {
            'name': 'Rettangolo',
            'id': 'rettangolo',
            'sources': ['Rettangolo/src/Punto.java', 'Rettangolo/src/Rettangolo.java'],
            'output': 'docs/rettangolo-output.txt',
            'compile': 'docs/rettangolo-compile.log',
            'description': 'Calcolo di vertici e proprietà di un rettangolo'
        },
        {
            'name': 'vocalcount',
            'id': 'vocalcount',
            'sources': ['vocalcount/src/voc_count.java'],
            'output': 'docs/vocalcount-output.txt',
            'compile': 'docs/vocalcount-compile.log',
            'description': 'Conteggio delle vocali in una stringa'
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
        compile_result = read_file_safe(project['compile'])
        status = "success" if not compile_result or "error:" not in compile_result.lower() else "error"
        status_icon = "✅" if status == "success" else "❌"
        status_text = "Compilato" if status == "success" else "Errori"
        
        project_cards += f'''
        <a href="{project['id']}.html" class="project-card">
            <div class="card-header">
                <h2>{escape_html(project['name'])}</h2>
                <span class="status-badge {status}">
                    {status_icon} {status_text}
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
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            color: white;
            margin-bottom: 50px;
            padding: 40px 20px;
        }}
        
        h1 {{
            font-size: 3.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .subtitle {{
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        
        .github-link {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 25px;
            color: white;
            text-decoration: none;
            transition: background 0.3s;
            margin-top: 10px;
        }}
        
        .github-link:hover {{
            background: rgba(255,255,255,0.3);
        }}
        
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 50px;
        }}
        
        .project-card {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            text-decoration: none;
            color: inherit;
            display: block;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .project-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
            gap: 15px;
        }}
        
        .card-header h2 {{
            color: #764ba2;
            font-size: 1.8em;
            flex: 1;
        }}
        
        .status-badge {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            white-space: nowrap;
        }}
        
        .status-badge.success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-badge.error {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .card-description {{
            color: #666;
            font-size: 1em;
            line-height: 1.6;
            margin-bottom: 20px;
            min-height: 48px;
        }}
        
        .card-footer {{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            padding-top: 15px;
            border-top: 2px solid #f0f0f0;
        }}
        
        .view-link {{
            color: #667eea;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: gap 0.3s;
        }}
        
        .project-card:hover .view-link {{
            gap: 12px;
        }}
        
        footer {{
            text-align: center;
            color: white;
            padding: 30px;
            margin-top: 30px;
        }}
        
        footer a {{
            color: white;
            text-decoration: none;
            font-weight: bold;
        }}
        
        footer a:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2.5em;
            }}
            
            .projects-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>☕ Java Projects</h1>
            <p class="subtitle">Progetti scolastici interattivi</p>
            <a href="https://github.com/bigBrodyG/JavaProjects" class="github-link">
                <i class="fab fa-github"></i>
                View on GitHub
            </a>
        </header>
        
        <div class="projects-grid">
            {project_cards}
        </div>
        
        <footer>
            <p>Generato automaticamente con GitHub Actions</p>
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
