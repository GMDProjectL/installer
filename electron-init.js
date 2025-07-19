import { app, BrowserWindow, Menu } from 'electron';

const urlFlagIndex = process.argv.indexOf('--url');
const urlToOpen = (urlFlagIndex !== -1 && process.argv[urlFlagIndex + 1]) || 'http://localhost:4173';

const iconFlagIndex = process.argv.indexOf('--icon');
const icon = (iconFlagIndex !== -1 && process.argv[iconFlagIndex + 1]) || '/usr/share/projectgdl-logo.png';

app.whenReady().then(() => {
  Menu.setApplicationMenu(null);

  const win = new BrowserWindow({
    width: 1280, height: 720,
    show: false, title: "Project GDL Installer",
    icon: icon
  });

  win.loadURL(urlToOpen);
  win.once('ready-to-show', () => {
    win.show()
  });
});