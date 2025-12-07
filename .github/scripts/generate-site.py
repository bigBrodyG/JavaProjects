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
            --bg: #03060f;
            --panel: #0a101f;
            --panel-alt: #121a30;
            --border: rgba(255, 255, 255, 0.07);
            --text: #f5f6ff;
            --muted: #9aa4c6;
            --accent: #6bb8ff;
            --accent-strong: #4a92ff;
            --success: #38d98a;
            --error: #f48b9c;
        }}
        
        *, *::before, *::after {{
            box-sizing: border-box;
        }}
        
        html, body {{
            height: 100%;
        }}
        
        body {{
            margin: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg);
            color: var(--text);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        header {{
            flex-shrink: 0;
            background: rgba(10, 16, 31, 0.96);
            border-bottom: 1px solid var(--border);
            padding: 16px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        header h1 {{
            font-size: 1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        header h1 i {{
            color: var(--accent);
        }}
        
        .back-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 5px;
            border: 1px solid var(--border);
            color: var(--text);
            text-decoration: none;
            font-size: 0.82rem;
        }}
        
        .back-btn:hover {{
            border-color: var(--accent);
            color: var(--accent);
        }}
        
        .container {{
            flex: 1;
            display: flex;
            border-top: 1px solid var(--border);
            min-height: 0;
            overflow: hidden;
        }}
        
        .left-panel {{
            flex: 1;
            min-width: 0;
            min-height: 0;
            display: flex;
            flex-direction: column;
            background: var(--panel);
            border-right: 1px solid var(--border);
        }}
        
        .tabs {{
            display: flex;
            padding: 0 12px;
            border-bottom: 1px solid var(--border);
            overflow-x: auto;
        }}
        
        .tab-button {{
            border: none;
            background: none;
            font-family: 'Fira Code', monospace;
            font-size: 0.8rem;
            padding: 10px 12px;
            color: var(--muted);
            cursor: pointer;
            border-bottom: 2px solid transparent;
        }}
        
        .tab-button:hover {{
            color: var(--text);
        }}
        
        .tab-button.active {{
            color: var(--accent);
            border-color: var(--accent);
        }}
        
        .code-area {{
            position: relative;
            flex: 1;
            min-height: 0;
            overflow: hidden;
            background: var(--panel-alt);
        }}
        
        .tab-content {{
            display: none;
            height: 100%;
        }}
        
        .tab-content.active {{
            display: block;
            height: 100%;
        }}
        
        pre {{
            height: 100%;
            margin: 0;
        }}
        
        pre code {{
            display: block;
            height: 100%;
            padding: 16px !important;
            background: #060a17 !important;
            color: #eaf0ff !important;
            font-size: 13px;
            line-height: 1.5;
            overflow: auto;
        }}
        
        .copy-btn {{
            position: absolute;
            top: 12px;
            right: 12px;
            border: 1px solid var(--border);
            background: rgba(3, 6, 15, 0.85);
            color: var(--text);
            border-radius: 4px;
            padding: 4px 9px;
            cursor: pointer;
            font-size: 0.75rem;
        }}
        
        .copy-btn:hover {{
            border-color: var(--accent);
            color: var(--accent);
        }}
        
        .right-panel {{
            width: 32%;
            min-width: 280px;
            min-height: 0;
            background: var(--panel);
            display: flex;
            flex-direction: column;
        }}
        
        .run-header {{
            padding: 14px 18px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .run-header h2 {{
            font-size: 0.9rem;
        }}
        
        .run-btn {{
            border: none;
            background: linear-gradient(120deg, var(--accent-strong), var(--accent));
            color: #fff;
            border-radius: 5px;
            padding: 7px 14px;
            cursor: pointer;
            font-weight: 500;
            font-size: 0.82rem;
        }}
        
        .run-btn:disabled {{
            opacity: 0.45;
            cursor: not-allowed;
        }}
        
        .output-area {{
            padding: 16px;
            flex: 1;
            min-height: 0;
            overflow: auto;
            background: var(--panel-alt);
        }}
        
        .output-box {{
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px;
            min-height: 130px;
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            white-space: pre-wrap;
            background: rgba(4, 8, 20, 0.92);
            color: var(--muted);
        }}
        
        .output-box.success {{
            border-color: rgba(56, 217, 138, 0.45);
            color: var(--success);
        }}
        
        .output-box.error {{
            border-color: rgba(244, 139, 156, 0.45);
            color: var(--error);
        }}
        
        .status-indicator {{
            font-size: 0.75rem;
            margin-bottom: 10px;
            padding: 6px 9px;
            border-radius: 4px;
            border: 1px solid var(--border);
            display: inline-flex;
            gap: 6px;
            align-items: center;
            color: var(--muted);
        }}
        
        .status-indicator.success {{
            color: var(--success);
            border-color: rgba(56, 217, 138, 0.35);
        }}
        
        .status-indicator.error {{
            color: var(--error);
            border-color: rgba(244, 139, 156, 0.35);
        }}
        
        .status-indicator.running {{
            color: var(--accent);
            border-color: rgba(107, 184, 255, 0.35);
        }}
        
        .spinner {{
            width: 0.8rem;
            height: 0.8rem;
            border-radius: 999px;
            border: 2px solid rgba(107, 184, 255, 0.2);
            border-top-color: var(--accent);
            animation: spin 0.6s linear infinite;
        }}
        
        @keyframes spin {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        .info-box {{
            border-left: 3px solid var(--accent);
            padding: 7px 10px;
            background: rgba(107, 184, 255, 0.08);
            font-size: 0.78rem;
            color: var(--muted);
            margin-bottom: 10px;
        }}
        
        @media (max-width: 960px) {{
            body {{
                overflow: auto;
            }}
            .container {{
                flex-direction: column;
                height: auto;
            }}
            .right-panel {{
                width: 100%;
                border-left: none;
                border-top: 1px solid var(--border);
            }}
        }}
        
        @media (max-width: 640px) {{
            header {{
                padding: 14px 16px;
                flex-direction: column;
                align-items: flex-start;
                gap: 6px;
            }}
            .tabs {{
                padding: 0 8px;
            }}
            .tab-button {{
                font-size: 0.75rem;
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
            'sources': ['Esercizi/Cerchio/src/Cerchio.java'],
            'output': 'docs/cerchio-output.txt',
            'compile': 'docs/cerchio-compile.log',
            'description': 'Classe per calcolare area e circonferenza di un cerchio',
            'type': 'teoria'
        },
        {
            'name': 'mergeArray',
            'id': 'mergearray',
            'sources': ['Laboratorio/mergeArray/src/mergeArrays.java'],
            'output': 'docs/mergearray-output.txt',
            'compile': 'docs/mergearray-compile.log',
            'description': 'Unione e ordinamento di array',
            'type': 'laboratorio'
        },
        {
            'name': 'OggettoCD',
            'id': 'oggettocd',
            'sources': ['Laboratorio/OggettoCD/src/Cd.java', 'Laboratorio/OggettoCD/src/PortaCD.java'],
            'output': 'docs/oggettocd-output.txt',
            'compile': 'docs/oggettocd-compile.log',
            'description': 'Gestione di un catalogo CD',
            'type': 'laboratorio'
        },
        {
            'name': 'Punto',
            'id': 'punto',
            'sources': ['Esercizi/Punto/src/Punto.java'],
            'output': 'docs/punto-output.txt',
            'compile': 'docs/punto-compile.log',
            'description': 'Rappresentazione di un punto nel piano cartesiano',
            'type': 'teoria'
        },
        {
            'name': 'Triangolo',
            'id': 'triangolo',
            'sources': ['Esercizi/Triangolo/src/Punto.java', 'Esercizi/Triangolo/src/Triangolo.java'],
            'output': 'docs/triangolo-output.txt',
            'compile': 'docs/triangolo-compile.log',
            'description': 'Gestione di triangoli e confronto tra forme congruenti',
            'type': 'teoria'
        },
        {
            'name': 'Rettangolo',
            'id': 'rettangolo',
            'sources': ['Laboratorio/Rettangolo/src/Punto.java', 'Laboratorio/Rettangolo/src/Rettangolo.java'],
            'output': 'docs/rettangolo-output.txt',
            'compile': 'docs/rettangolo-compile.log',
            'description': 'Calcolo di vertici e proprietà di un rettangolo',
            'type': 'laboratorio'
        },
        {
            'name': 'vocalcount',
            'id': 'vocalcount',
            'sources': ['Laboratorio/vocalcount/src/voc_count.java'],
            'output': 'docs/vocalcount-output.txt',
            'compile': 'docs/vocalcount-compile.log',
            'description': 'Conteggio delle vocali in una stringa',
            'type': 'laboratorio'
        },
        {
            'name': 'Libro',
            'id': 'libro',
            'sources': ['Esercizi/Libro/src/Libro.java'],
            'output': 'docs/libro-output.txt',
            'compile': 'docs/libro-compile.log',
            'description': 'Gestione di oggetti libro con calcolo del prezzo',
            'type': 'teoria'
        },
        {
            'name': 'Orario',
            'id': 'orario',
            'sources': ['Esercizi/Orario/src/Orario.java', 'Esercizi/Orario/src/TestOrario.java'],
            'output': 'docs/orario-output.txt',
            'compile': 'docs/orario-compile.log',
            'description': 'Gestione e manipolazione di orari',
            'type': 'teoria'
        },
        {
            'name': 'Software',
            'id': 'software',
            'sources': ['Esercizi/Software/src/Software.java'],
            'output': 'docs/software-output.txt',
            'compile': 'docs/software-compile.log',
            'description': 'Gestione software con programmi e contenitori',
            'type': 'teoria'
        },
        {
            'name': 'SpeseManager',
            'id': 'spesemanager',
            'sources': ['Laboratorio/SpeseManager/src/Main.java', 'Laboratorio/SpeseManager/src/SpesaManager.java', 'Laboratorio/SpeseManager/src/Spese.java'],
            'output': 'docs/spesemanager-output.txt',
            'compile': 'docs/spesemanager-compile.log',
            'description': 'Gestore spese personali con statistiche',
            'type': 'laboratorio'
        },
        {
            'name': '01_Verifica_teoria',
            'id': '01_verifica_teoria',
            'sources': ['01_Verifica_teoria/src/Main.java', '01_Verifica_teoria/src/SchedaSim.java', '01_Verifica_teoria/src/Telefonata.java'],
            'output': 'docs/01_verifica_teoria-output.txt',
            'compile': 'docs/01_verifica_teoria-compile.log',
            'description': 'Verifica teoria: gestione scheda SIM e telefonate',
            'type': 'teoria'
        },
        {
            'name': '02_Verifica_lab',
            'id': '02_verifica_lab',
            'sources': ['02_Verifica_lab/src/MacchinaDistributrice.java', '02_Verifica_lab/src/Main.java', '02_Verifica_lab/src/Prodotto.java'],
            'output': 'docs/02_verifica_lab-output.txt',
            'compile': 'docs/02_verifica_lab-compile.log',
            'description': 'Verifica lab: macchina distributrice con prodotti',
            'type': 'laboratorio'
        },
        {
            'name': 'Abbonamento',
            'id': 'abbonamento',
            'sources': ['Esercizi/Abbonamento/src/Cd.java', 'Esercizi/Abbonamento/src/Main.java', 'Esercizi/Abbonamento/src/PortaCD.java'],
            'output': 'docs/abbonamento-output.txt',
            'compile': 'docs/abbonamento-compile.log',
            'description': 'Gestione CD e porta CD con abbonamenti',
            'type': 'teoria'
        },
        {
            'name': 'Ereditarietà',
            'id': 'ereditarietà',
            'sources': ['Esercizi/Ereditarietà/src/Docente.java', 'Esercizi/Ereditarietà/src/Main.java', 'Esercizi/Ereditarietà/src/Persona.java', 'Esercizi/Ereditarietà/src/Studente.java'],
            'output': 'docs/ereditarietà-output.txt',
            'compile': 'docs/ereditarietà-compile.log',
            'description': 'Ereditarietà: persone, docenti e studenti',
            'type': 'teoria'
        },
        {
            'name': 'Immobili',
            'id': 'immobili',
            'sources': ['Esercizi/Immobili/src/Abitazione.java', 'Esercizi/Immobili/src/Appartamento.java', 'Esercizi/Immobili/src/Test.java', 'Esercizi/Immobili/src/Villa.java'],
            'output': 'docs/immobili-output.txt',
            'compile': 'docs/immobili-compile.log',
            'description': 'Gestione immobili: appartamenti e ville',
            'type': 'teoria'
        },
        {
            'name': 'Playlist',
            'id': 'playlist',
            'sources': ['Laboratorio/Playlist/src/Brano.java', 'Laboratorio/Playlist/src/LibreriaMusicale.java', 'Laboratorio/Playlist/src/Main.java'],
            'output': 'docs/playlist-output.txt',
            'compile': 'docs/playlist-compile.log',
            'description': 'Libreria musicale con brani e playlist',
            'type': 'laboratorio'
        },
        {
            'name': 'Autonoleggio',
            'id': 'autonoleggio',
            'sources': [
                'Esercizi/Autonoleggio/src/Main.java',
                'Esercizi/Autonoleggio/src/Veicolo.java',
                'Esercizi/Autonoleggio/src/Autovettura.java',
                'Esercizi/Autonoleggio/src/Furgone.java',
                'Esercizi/Autonoleggio/src/Noleggio.java',
                'Esercizi/Autonoleggio/src/GestioneAutonoleggio.java'
            ],
            'output': 'docs/autonoleggio-output.txt',
            'compile': 'docs/autonoleggio-compile.log',
            'description': 'Sistema gestione autonoleggio con calcolo costi',
            'type': 'teoria'
        },
        {
            'name': 'GestionePC',
            'id': 'gestionepc',
            'sources': [
                'Esercizi/GestionePC/src/Main.java',
                'Esercizi/GestionePC/src/PC.java',
                'Esercizi/GestionePC/src/Desktop.java',
                'Esercizi/GestionePC/src/Notebook.java',
                'Esercizi/GestionePC/src/Server.java',
                'Esercizi/GestionePC/src/Palmare.java',
                'Esercizi/GestionePC/src/PCFisso.java',
                'Esercizi/GestionePC/src/PCPortatile.java',
                'Esercizi/GestionePC/src/InventarioPC.java'
            ],
            'output': 'docs/gestionepc-output.txt',
            'compile': 'docs/gestionepc-compile.log',
            'description': 'Inventario PC con gerarchia classi',
            'type': 'teoria'
        },
        {
            'name': 'Treni',
            'id': 'treni',
            'sources': [
                'Esercizi/Treni/src/Main.java',
                'Esercizi/Treni/src/Vagone.java',
                'Esercizi/Treni/src/VagonePasseggeri.java',
                'Esercizi/Treni/src/VagoneMerci.java',
                'Esercizi/Treni/src/Treno.java'
            ],
            'output': 'docs/treni-output.txt',
            'compile': 'docs/treni-compile.log',
            'description': 'Composizione treni con vagoni passeggeri e merci',
            'type': 'teoria'
        },
        {
            'name': 'BiblioOverride',
            'id': 'bibliooverride',
            'sources': [
                'Laboratorio/BiblioOverride/src/Main.java',
                'Laboratorio/BiblioOverride/src/Pubblicazione.java',
                'Laboratorio/BiblioOverride/src/Libro.java',
                'Laboratorio/BiblioOverride/src/Rivista.java',
                'Laboratorio/BiblioOverride/src/Biblioteca.java'
            ],
            'output': 'docs/bibliooverride-output.txt',
            'compile': 'docs/bibliooverride-compile.log',
            'description': 'Biblioteca con override durata prestito',
            'type': 'laboratorio'
        },
        {
            'name': 'Biblioteca',
            'id': 'biblioteca',
            'sources': [
                'Laboratorio/Biblioteca/src/Main.java',
                'Laboratorio/Biblioteca/src/Pubblicazione.java',
                'Laboratorio/Biblioteca/src/Libro.java',
                'Laboratorio/Biblioteca/src/Rivista.java',
                'Laboratorio/Biblioteca/src/Biblioteca.java'
            ],
            'output': 'docs/biblioteca-output.txt',
            'compile': 'docs/biblioteca-compile.log',
            'description': 'Sistema gestione biblioteca',
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
            --bg: #03060f;
            --panel: #0b111f;
            --panel-soft: #121a2f;
            --border: rgba(255, 255, 255, 0.08);
            --text: #f5f6ff;
            --muted: #98a2c1;
            --accent: #69b4ff;
            --accent-soft: rgba(105, 180, 255, 0.15);
            --theory: #39d98a;
            --lab: #f5b453;
        }}
        
        *, *::before, *::after {{
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            min-height: 100vh;
            background: var(--bg);
            color: var(--text);
            padding: 36px 16px 54px;
        }}
        
        .container {{
            max-width: 1050px;
            margin: 0 auto;
        }}
        
        .hero {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 26px;
            margin-bottom: 22px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .hero .eyebrow {{
            font-size: 0.7rem;
            letter-spacing: 0.28em;
            text-transform: uppercase;
            color: var(--muted);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        
        .hero h1 {{
            margin: 0;
            font-size: 2rem;
            letter-spacing: -0.35px;
        }}
        
        .hero-subtitle {{
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.45;
        }}
        
        .hero-actions {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 6px;
        }}
        
        .button {{
            border-radius: 8px;
            padding: 8px 14px;
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid transparent;
            font-size: 0.9rem;
        }}
        
        .button.primary {{
            background: linear-gradient(120deg, #4e8eff, #7ac6ff);
            color: #050713;
        }}
        
        .button.primary:hover {{
            opacity: 0.9;
        }}
        
        .button.ghost {{
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(255, 255, 255, 0.08);
            color: var(--text);
        }}
        
        .button.ghost:hover {{
            border-color: var(--accent);
            color: var(--accent);
        }}
        
        .stats-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
        }}
        
        .stats-card {{
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px;
            background: var(--panel-soft);
        }}
        
        .stats-label {{
            font-size: 0.72rem;
            letter-spacing: 0.12em;
            color: var(--muted);
        }}
        
        .stats-value {{
            font-size: 1.4rem;
            font-weight: 600;
            margin-top: 4px;
        }}
        
        .controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}
        
        .filters {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        
        .filter-button {{
            border-radius: 999px;
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.02);
            color: var(--muted);
            padding: 6px 12px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
            font-size: 0.82rem;
        }}
        
        .filter-button span {{
            background: var(--accent-soft);
            border-radius: 999px;
            padding: 2px 6px;
            font-size: 0.72rem;
            color: var(--accent);
        }}
        
        .filter-button.active {{
            border-color: var(--accent);
            color: var(--accent);
        }}
        
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 14px;
        }}
        
        .project-card {{
            text-decoration: none;
            color: inherit;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: var(--panel);
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            transition: border 0.2s ease, transform 0.2s ease;
        }}
        
        .project-card:hover {{
            border-color: var(--accent);
            transform: translateY(-2px);
        }}
        
        .project-card.is-hidden {{
            opacity: 0;
            pointer-events: none;
        }}
        
        .card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .project-icon {{
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: grid;
            place-items: center;
            background: var(--accent-soft);
            color: var(--accent);
            font-size: 1rem;
        }}
        
        .project-icon.laboratorio {{
            background: rgba(245, 180, 83, 0.14);
            color: var(--lab);
        }}
        
        .status-pill {{
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.7rem;
            letter-spacing: 0.04em;
            border: 1px solid var(--border);
        }}
        
        .status-pill.success {{
            color: var(--lab);
            border-color: rgba(245, 180, 83, 0.35);
        }}
        
        .status-pill.theory {{
            color: var(--theory);
            border-color: rgba(57, 217, 138, 0.35);
        }}
        
        .card-content h2 {{
            margin: 0;
            font-size: 1.2rem;
        }}
        
        .card-description {{
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.4;
        }}
        
        .card-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.82rem;
            color: var(--muted);
        }}
        
        .card-arrow {{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 1px solid var(--border);
            display: grid;
            place-items: center;
        }}
        
        .view-link {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-weight: 600;
            color: var(--accent);
        }}
        
        .footer {{
            margin-top: 22px;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
            background: var(--panel);
            text-align: center;
            color: var(--muted);
        }}
        
        .footer .social-links {{
            margin-top: 8px;
            display: flex;
            justify-content: center;
            gap: 10px;
        }}
        
        .footer .social-links a {{
            color: var(--accent);
            text-decoration: none;
        }}
        
        @media (max-width: 640px) {{
            body {{
                padding: 26px 12px 40px;
            }}
            
            .hero {{
                padding: 20px;
            }}
            
            .hero h1 {{
                font-size: 1.7rem;
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
