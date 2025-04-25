#pragma once

#include <string>
class InstallationInfo {
public:
    std::string language = "en";
    char* username = new char[64]();
    char* hostname = new char[64]();
    char* password = new char[64]();
    char* password2 = new char[64]();
    std::string timezoneRegion = "";
    std::string selectedDrive = "";
    std::string method = "nuke-drive";
    std::string bootPartition = "";
    std::string rootPartition = "";
    bool formatBootPartition = false;
    bool enableMultilibRepo = false;
    bool installSteam = false;
    bool installWine = false;
    bool installWinetricks = false;
    bool vulkanNvidia = false;
    bool vulkanAmd = false;
    bool vulkanIntel = false;
    bool installGnomeDisks = false;
    bool installIntelMedia = false;
    bool setupBluetooth = false;
    std::string de = "kde";

};