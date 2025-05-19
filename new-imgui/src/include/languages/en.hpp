#pragma once
#include <string>
#include <unordered_map>


namespace Languages {
    inline std::unordered_map<std::string, std::string> g_englishStrings = {
        {"lang_name", "English"},
        {"welcome", "Welcome to Project GDL Installer!"},
        {"welcome_subtitle", "Easy-to-use Linux distribution."},
        {"lang_title", "First, select the language:"},
        {"back", "Back"},
        {"next", "Next"},
        {"introduce_yourself", "Introduce yourself"},
        {"username", "Username"},
        {"hostname", "Computer name"},
        {"password", "Password"},
        {"password2", "Repeat password"},
        {"where_are_you", "Where are you?"},
        {"youre_in", "You're timezone is:"},
        {"select_region", "Select region first."},
        {"desktop_environment", "Desktop Environment"},
        {"kde_description", "KDE Plasma is a desktop environment from\nthe KDE community. It\'s very customizable\nand has a lot of features. Highly recommended for gaming."},
        {"gnome_description", "GNOME is a desktop environment from the\nGNOME community. It\'s strict and determined.\nHighly recommended for productivity."},
        {"you_selected", "You selected:"},
        {"kde", "KDE"},
        {"gnome", "GNOME"},
        {"additional_software", "Additional Software"},
        {"enable_multilib_repo", "Enable multilib repository"},
        {"install_steam", "Install Steam"},
        {"install_wine", "Install WineHQ to run Windows applications"},
        {"install_winetricks", "Install Winetricks"},
        {"install_gnome_disks", "Install Gnome Disks (for managing disks)"},
        {"install_intel_media", "Install Intel Media (QSV, VA-API, etc.)"},
        {"setup_bluetooth", "Setup Bluetooth"},
        
        {"selected_drive", "Selected drive"},
        {"boot_partition", "Boot partition"},
        {"root_partition", "Root partition"},
        {"format_boot_partition", "Format boot partition"}
    };
}