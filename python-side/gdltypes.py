from dataclasses import dataclass

@dataclass
class InstallInfo:
    language: str
    username: str
    computerName: str
    password: str
    password2: str
    timezoneRegion: str
    timezoneInfo: str
    selectedDrive: str
    method: str
    bootPartition: str
    rootPartition: str
    formatBootPartition: bool
    enableMultilibRepo: bool
    installSteam: bool
    installWine: bool
    installWinetricks: bool
    vulkanNvidia: bool
    vulkanAmd: bool
    vulkanIntel: bool
    installGnomeDisks: bool
    installIntelMedia: bool
    setupBluetooth: bool
    de: str