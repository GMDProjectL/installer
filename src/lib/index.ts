import { getLanguageStrings, getString, getCityString, getRegionString } from "./lang";
import { GDLButton, SetupPage, SetupPageTitle, AdditionalFeaturesContent, SetupPageBottom, GDLInput } from "./components";

import installInfo, { updateInfo } from "./stores/install-info";
import installationPage from "./stores/installation-page";
import installProgress from "./stores/install-progress";

import type { InstallInfo } from "./stores/install-info";
import { 
    getTimezones, getDrives, getPartitions, getUsername, startUpdate,
    checkInternetConnection, startInstallation, getInstallationEvents,
    reboot, getInstallationProgress, getSystemLanguage, getDE
} from "./api";
import type { TimezonesResponse, DrivesResponse, PartitionsResponse } from "./api";
import bytesToReadable from "./utils/size";
import type InstallationProgress from "./stores/install-progress";
import { currentInternetDevice, doSkippedInternetSetup, internetDevices } from "./stores/internet-stuff";


export { 
    getLanguageStrings, getString, getDE,
    GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, AdditionalFeaturesContent,
    GDLInput,
    installInfo, installationPage, reboot, getSystemLanguage, startUpdate,
    getTimezones, getDrives, getPartitions,
    bytesToReadable, getUsername, updateInfo,
    checkInternetConnection, startInstallation, getInstallationEvents,
    getCityString, getRegionString, getInstallationProgress, installProgress, currentInternetDevice, doSkippedInternetSetup, internetDevices
};

export type {
    InstallInfo,
    TimezonesResponse, DrivesResponse, PartitionsResponse
};