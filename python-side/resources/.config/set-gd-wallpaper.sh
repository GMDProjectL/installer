#!/bin/sh
dbus-send --dest=org.kde.plasmashell --print-reply --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript string:'
    var allDesktops = desktops();
    print (allDesktops);
    for (i=0;i<allDesktops.length;i++) {{
        d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper",
                                     "org.kde.image",
                                     "General");
        d.writeConfig("Image", "file:///home/myuser/.config/pgd-bg.png")
    }}
'
