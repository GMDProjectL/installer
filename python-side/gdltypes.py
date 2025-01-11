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