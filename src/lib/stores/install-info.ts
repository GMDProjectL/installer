import { writable } from "svelte/store";

type InstallInfo = {
    language: string,
    username: string,
    computerName: string,
    password: string,
    password2: string,
    timezoneRegion: string,
    timezoneInfo: string,
    selectedDrive: string,
    method: string,
    bootPartition: string,
    rootPartition: string,
    formatBootPartition: boolean,
    enableMultilibRepo: boolean,
    installSteam: boolean,
    installWine: boolean,
    installWinetricks: boolean,
    vulkanNvidia: boolean,
    vulkanAmd: boolean,
    vulkanIntel: boolean,
    installGnomeDisks: boolean,
    installIntelMedia: boolean
}

let installInfo = writable<InstallInfo>({
    language: 'en',
    username: '',
    computerName: '',
    password: '',
    password2: '',
    timezoneRegion: '',
    timezoneInfo: '',
    selectedDrive: '',
    method: 'nuke-drive',
    bootPartition: '',
    rootPartition: '',
    formatBootPartition: false,
    enableMultilibRepo: false,
    installSteam: false,
    installWine: false,
    installWinetricks: false,
    vulkanNvidia: false,
    vulkanAmd: false,
    vulkanIntel: false,
    installGnomeDisks: false,
    installIntelMedia: false
});

export default installInfo;  // Export the store
export type { InstallInfo };  // Export the type definition