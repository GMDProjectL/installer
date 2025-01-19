#!/bin/sh
if [ "$XDG_CURRENT_DESKTOP" = "KDE" ]; then
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
elif [ "$XDG_CURRENT_DESKTOP" = "GNOME" ]; then
    dconf write /org/gnome/desktop/background/picture-uri "file:///home/${HOME}/.config/pgd-bg.png"
    dconf write /org/gnome/desktop/background/picture-uri-dark "file:///home/${HOME}/.config/pgd-bg.png"
    gsettings set org.gnome.desktop.background picture-uri "file://${HOME}/.config/pgd-bg.png"
    gsettings set org.gnome.desktop.background picture-uri-dark "file://${HOME}/.config/pgd-bg.png"
fi