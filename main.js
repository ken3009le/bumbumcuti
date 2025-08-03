const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 800,
    icon: path.join(__dirname, 'e-A69.ico'),
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
      webSecurity: false,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  win.loadFile('index.html');
  // win.webContents.openDevTools(); // Uncomment if needed
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});


ipcMain.handle('upload-media', async (event, { filePath, folder, name, mediaType }) => {
  try {
    const ext = path.extname(filePath);
    const targetDir = path.join(__dirname, folder);

    if (!fs.existsSync(targetDir)) fs.mkdirSync(targetDir, { recursive: true });

    const destPath = path.join(targetDir, name);
    fs.copyFileSync(filePath, destPath);

    const mediaJsonPath = path.join(__dirname, 'media2.json');
    const mediaData = JSON.parse(fs.readFileSync(mediaJsonPath, 'utf-8'));

    const relativePath = path.posix.join(folder, name);

    if (!mediaData[folder]) mediaData[folder] = { images: [], videos: [] };
    if (!mediaData[folder][mediaType]) mediaData[folder][mediaType] = [];

    mediaData[folder][mediaType].push({ path: relativePath });

    fs.writeFileSync(mediaJsonPath, JSON.stringify(mediaData, null, 2));
    console.log(`[+] Đã lưu file ${name} vào thư mục ${folder} và cập nhật media2.json`);

    return { success: true };
  } catch (err) {
    return { success: false, error: err.message };
  }
});
