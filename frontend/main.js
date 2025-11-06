const { app, BrowserWindow, Tray, Menu } = require('electron');
const path = require('path');

let tray;
let win;

function createWindow() {
  win = new BrowserWindow({
    width: 400,
    height: 300,
    show: false,
    skipTaskbar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.setContentProtection(true);
  win.loadFile('index.html');

  win.on('close', (event) => {
    if (!app.isQuiting) {
      event.preventDefault();
      win.hide();
    }
  });
}

function toggleWindowVisibility() {
  if (!win) return;
  if (win.isVisible()) {
    win.hide();
  } else {
    win.show();
    win.focus();
  }
}

app.whenReady().then(() => {
  createWindow();

  try {
    const iconPath = path.join(__dirname, 'icon.png');
    tray = new Tray(iconPath);
    const menu = Menu.buildFromTemplate([
      { label: 'Toggle Window', click: () => toggleWindowVisibility() },
      { type: 'separator' },
      {
        label: 'Quit',
        click: () => {
          app.isQuiting = true;
          app.quit();
        },
      },
    ]);
    tray.setToolTip('Stealth Interview Assistant');
    tray.setContextMenu(menu);
    tray.on('click', toggleWindowVisibility);
  } catch (err) {
    console.error('Tray icon error:', err);
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  } else if (win) {
    win.show();
    win.focus();
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
