#!/usr/bin/env python3
"""Add session features to index.html"""
import re

# Read the file in binary mode to preserve exact line endings
with open('frontend/index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# 1. Add setup.css link
content = content.replace(
    '  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>',
    '  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>\r\n  <link rel="stylesheet" href="setup.css">'
)

# 2. Add setup overlay
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

# 3. Add session controls
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

# 4. Add setup.js script
# Find the closing script tag and body tag
pattern = r'(  </script>\r\n)(</body>)'
replacement = r'\1  <script src="setup.js"></script>\r\n\2'
content = re.sub(pattern, replacement, content)

# Write back in binary mode
with open('frontend/index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("Done - added session features")
