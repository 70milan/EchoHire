with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the controls div and add Start/Stop Session buttons
for i in range(len(lines)):
    if '<button id="btn-end-session"' in lines[i]:
        # Insert Start and Stop Session buttons before End Session
        indent = '      '
        lines.insert(i, f'{indent}<button id="btn-start-session-timer" class="btn">▶️ Start Session</button>\r\n')
        lines.insert(i+1, f'{indent}<button id="btn-stop-session-timer" class="btn">⏸️ Stop Session</button>\r\n')
        break

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Added Start/Stop Session buttons")
