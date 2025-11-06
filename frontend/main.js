const { app, BrowserWindow, Tray, Menu } = require('electron');
const path = require('path');

let tray;
let win;

function createWindow() {
  win = new BrowserWindow({
    width: 400,
    height: 300,
    show: true,  // ✅ set to true for now to confirm it opens
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();

  // Safe tray setup
  try {
    const iconPath = path.join(__dirname, 'icon.png');
    tray = new Tray(iconPath);
    const menu = Menu.buildFromTemplate([
      { label: 'Show Window', click: () => win.show() },
      { label: 'Quit', click: () => app.quit() },
    ]);
    tray.setToolTip('Stealth Interview Assistant');
    tray.setContextMenu(menu);
  } catch (err) {
    console.error('Tray icon error:', err);
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
