import { writable } from "svelte/store";

type FeaturesInfo = {
    enableMultilibRepo: boolean,
    installSteam: boolean,
    installWine: boolean,
    installWinetricks: boolean,
    vulkanNvidia: boolean,
    vulkanAmd: boolean,
    vulkanIntel: boolean,
    installGnomeDisks: boolean,
    installIntelMedia: boolean,
    setupBluetooth: boolean,
    setupCachyosKernel: boolean,
    runRussianReflector: boolean,
    installLact: boolean,
    de: string,
    username: string,
    doOsProber: boolean
}

type InstallInfo = FeaturesInfo & {
    language: string,
    computerName: string,
    password: string,
    password2: string,
    timezoneRegion: string,
    timezoneInfo: string,
    selectedDrive: string,
    method: string,
    bootPartition: string,
    rootPartition: string,
    formatBootPartition: boolean
}

type UpdateFlags = FeaturesInfo & {
    dontCopyKde: boolean
    dontUpdateGrub: boolean
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
    installIntelMedia: false,
    setupBluetooth: false,
    setupCachyosKernel: true,
    runRussianReflector: false,
    installLact: true,
    de: 'kde',
    doOsProber: true
});

let updateInfo = writable<UpdateFlags>({
    username: '',
    enableMultilibRepo: false,
    installSteam: false,
    installWine: false,
    installWinetricks: false,
    vulkanNvidia: false,
    vulkanAmd: false,
    vulkanIntel: false,
    installGnomeDisks: false,
    installIntelMedia: false,
    setupBluetooth: false,
    setupCachyosKernel: true,
    runRussianReflector: false,
    installLact: true,
    de: 'kde',
    dontCopyKde: false,
    dontUpdateGrub: false,
    doOsProber: true
});

export default installInfo;  // Export the store
export { updateInfo }
export type { InstallInfo, UpdateFlags };  // Export the type definition