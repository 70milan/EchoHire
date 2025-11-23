# Interview Assistant

## How to Run

### Terminal 1 - Backend:
```bash
python backend/main.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run electron
```

Keep both terminals open while using the app.

## Keyboard Shortcuts

**Audio Capture:**
- `Ctrl+R` - System audio
- `Ctrl+M` - Microphone

**AI Features:**
- `Ctrl+K` - Screenshot
- `Ctrl+G` - Generate AI answer
- `Ctrl+F` - Maximize AI response

**Window Control:**
- `Ctrl+Q` - Toggle mini mode
- `Ctrl+Shift+O` - Reset to default size
- `Ctrl+Shift++` / `Ctrl+Shift+-` - Resize
- `Ctrl+Alt+Arrows` - Move window
- `Ctrl+Backspace` - Clear transcript
- `Ctrl+Shift+Q` - Quit

## Setup

Add your OpenAI API key to `backend/.env`:
```
OPENAI_API_KEY=your_key_here
```
