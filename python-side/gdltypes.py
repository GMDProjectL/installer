from dataclasses import dataclass

@dataclass
class FeaturesInfo:
    de: str
    setupCachyosKernel: bool
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
    runRussianReflector: bool
    installLact: bool
    fromUpdate: bool
    username: str
    doOsProber: bool

@dataclass
class InstallInfo(FeaturesInfo):
    language: str
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

@dataclass
class UpdateFlags(FeaturesInfo):
    dontCopyKde: bool
    dontUpdateGrub: bool
    

@dataclass
class CommandOutput:
    stdout: str
    stderr: str
    returncode: int