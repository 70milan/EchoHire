with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with </script> before </body>
for i in range(len(lines) - 1, -1, -1):
    if '</script>' in lines[i] and i + 1 < len(lines) and '</body>' in lines[i + 1]:
        # Insert the setup.js script tag after this </script> line
        lines.insert(i + 1, '  <script src="setup.js"></script>\n')
        break

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Added setup.js")
