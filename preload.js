const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  saveMediaJson: (filename, data) =>
    ipcRenderer.invoke('save-media-json', { filename, data })
});
