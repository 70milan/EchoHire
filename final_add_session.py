#!/usr/bin/env python3
"""Add session features to index.html - FINAL VERSION"""

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add setup.css link (only if not already present)
if 'setup.css' not in content:
    content = content.replace(
        '  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>',
        '  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>\r\n  <link rel="stylesheet" href="setup.css">'
    )

# 2. Add setup overlay (only if not already present)
if 'setup-overlay' not in content:
    setup_overlay = '''  <div id="setup-overlay">
    <div class="setup-container">
      <h1>🚀 Interview Assistant Setup</h1>
      <div class="setup-form">
        <label>1. Upload Resume (.docx)</label>
        <input type="file" id="setup-resume" accept=".docx" class="setup-input" />
        <label>2. Job Description</label>
        <textarea id="setup-jobdesc" class="setup-input" placeholder="Paste the job description here..."></textarea>
      </div>
      <div id="setup-status"></div>
      <button id="btn-start-session">Create Session & Start (2h)</button>
    </div>
  </div>

  '''
    
    content = content.replace(
        '  <div id="mini-icon">🎙️</div>',
        setup_overlay + '<div id="mini-icon">🎙️</div>'
    )

# 3. Add session controls (only if not already present)
if 'btn-end-session' not in content:
    old_controls = '''    <div id="controls">
      <button id="btn-system" class="btn">🖥️ System (Ctrl+R)</button>
      <button id="btn-mic" class="btn">🎤 Mic (Ctrl+M)</button>
      <button id="btn-screen" class="btn">📸 Screen (Ctrl+K)</button>
      <button id="btn-generate" class="btn">💡 AI (Ctrl+G)</button>
    </div>'''

    new_controls = '''    <div id="controls">
      <button id="btn-system" class="btn">🖥️ System (Ctrl+R)</button>
      <button id="btn-mic" class="btn">🎤 Mic (Ctrl+M)</button>
      <button id="btn-screen" class="btn">📸 Screen (Ctrl+K)</button>
      <button id="btn-generate" class="btn">💡 AI (Ctrl+G)</button>
      <button id="btn-end-session" class="btn">🛑 End Session</button>
      <div id="session-timer"><span>⏱️</span> 2:00:00</div>
    </div>'''

    content = content.replace(old_controls, new_controls)

# 4. Add setup.js script (only if not already present)
if 'setup.js' not in content:
    # Find </script> followed by </body>
    import re
    content = re.sub(
        r'(  </script>\r\n)(</body>)',
        r'\1  <script src="setup.js"></script>\r\n\2',
        content
    )

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully added session features")
