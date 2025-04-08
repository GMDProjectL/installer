#pragma once
#include <string>
#include <map>


namespace Languages {
    inline std::map<std::string, std::string> g_englishStrings = {
        {"lang_name", "English"},
        {"welcome", "Welcome to Project GDL Installer!"},
        {"welcome_subtitle", "Easy-to-use Linux distribution."},
        {"back", "Back"},
        {"next", "Next"},
        {"introduce_yourself", "Introduce yourself"},
        {"username", "Username"},
        {"hostname", "Computer name"},
        {"password", "Password"},
        {"password2", "Repeat password"},
        {"timezone", "Timezone"},
        {"timezone_region", "Region"},
        {"timezone_info", "Timezone info"},
        {"selected_drive", "Selected drive"},
        {"boot_partition", "Boot partition"},
        {"root_partition", "Root partition"},
        {"format_boot_partition", "Format boot partition"},
        {"enable_multilib_repo", "Enable multilib repo"},
        {"install_steam", "Install Steam"},
        {"install_wine", "Install Wine"},
        {"install_winetricks", "Install Winetricks"},
        {"vulkan_nvidia", "Vulkan Nvidia drivers"},
        {"vulkan_amd", "Vulkan AMD drivers"},
        {"vulkan_intel", "Vulkan Intel drivers"},
        {"install_gnome_disks", "Install Gnome Disks"},
        {"install_intel_media", "Install Intel Media Drivers"},
        {"setup_bluetooth", "Setup Bluetooth"}
    };
}