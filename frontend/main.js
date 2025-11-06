const { app, BrowserWindow, Tray, Menu, nativeImage, globalShortcut, screen } = require('electron');
const path = require('path');

let tray = null;
let win = null;
let isRecording = false;
let isCollapsed = false;

function centerTop(width = 400, height = 500) {
  const { width: sw, height: sh } = screen.getPrimaryDisplay().workAreaSize;
  const x = Math.round((sw - width) / 2);
  const y = 0;                 // <-- anchor to absolute top
  return { x, y, width, height };
}

function createWindow() {
  const bounds = centerTop();
  win = new BrowserWindow({
    ...bounds,
    show: false,
    frame: false,
    alwaysOnTop: true,
    skipTaskbar: true,
    transparent: true,
    backgroundColor: '#1e1e1eAA',
    opacity: 0.92,
    resizable: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });
  win.loadFile(path.join(__dirname, 'index.html'));
}

app.whenReady().then(() => {
  createWindow();

  /* ---- move left / right ---- */
  globalShortcut.register('CommandOrControl+Left', () => {
    if (!win) return;
    const [x, y] = win.getPosition();
    win.setPosition(x - 50, y); // move 50px left
  });

  globalShortcut.register('CommandOrControl+Right', () => {
    if (!win) return;
    const [x, y] = win.getPosition();
    win.setPosition(x + 50, y); // move 50px right
  });

  /* ---- record / transcribe only ---- */
  globalShortcut.register('CommandOrControl+A', () => {
    if (!win) return;
    if (!isRecording) {
      console.log('🎙️ start record');
      win.webContents.executeJavaScript(`
        if (window.startRecordingOnly) { startRecordingOnly(); }
        else document.getElementById('recordBtn').click();
      `);
      isRecording = true;
    } else {
      console.log('🛑 stop record');
      win.webContents.executeJavaScript(`
        if (window.stopRecordingOnly) { stopRecordingOnly(); }
        else document.getElementById('recordBtn').click();
      `);
      isRecording = false;
    }
  });

  /* ---- generate AI from transcript ---- */
  globalShortcut.register('CommandOrControl+G', () => {
    if (!win) return;
    console.log('🤖 generate AI reply');
    win.webContents.executeJavaScript(`
      if (window.generateAIOnly) { generateAIOnly(); }
    `);
  });

  /* ---- expand / shrink ---- */
  globalShortcut.register('CommandOrControl+E', () => {
    const { width: sw } = screen.getPrimaryDisplay().workAreaSize;
    const [_, y] = win.getPosition();
    win.setBounds({ x: Math.round((sw - 800) / 2), y, width: 800, height: 500 });
  });

  globalShortcut.register('CommandOrControl+Shift+E', () => {
    const { width: sw } = screen.getPrimaryDisplay().workAreaSize;
    const [_, y] = win.getPosition();
    win.setBounds({ x: Math.round((sw - 400) / 2), y, width: 400, height: 500 });
  });

  /* ---- collapse to heading only ---- */
  globalShortcut.register('CommandOrControl+Shift+Q', () => {
    if (!win) return;
    const [x, y] = win.getPosition();
    if (!isCollapsed) {
      win.setBounds({ x, y, width: 400, height: 60 });
      win.webContents.executeJavaScript(`
        document.body.classList.add('collapsed');
      `);
      isCollapsed = true;
    } else {
      win.setBounds({ x, y, width: 400, height: 500 });
      win.webContents.executeJavaScript(`
        document.body.classList.remove('collapsed');
      `);
      isCollapsed = false;
    }
  });

  /* ---- Tray ---- */
  const iconPath = path.join(__dirname, 'icon.png');
  tray = new Tray(nativeImage.createFromPath(iconPath));
  tray.setToolTip('Interview Assistant');
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Show / Hide', click: () => (win.isVisible() ? win.hide() : win.show()) },
    { type: 'separator' },
    { label: 'Quit', click: () => app.quit() },
  ]);
  tray.setContextMenu(contextMenu);
  tray.on('click', () => (win.isVisible() ? win.hide() : win.show()));

  if (app.dock) app.dock.hide();
});

app.on('will-quit', () => globalShortcut.unregisterAll());
app.on('window-all-closed', e => e.preventDefault());
