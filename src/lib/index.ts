import { getLanguageStrings, getString, getCityString, getRegionString } from "./lang";
import { GDLButton, SetupPage, SetupPageTitle, AdditionalFeaturesContent, SetupPageBottom, GDLInput, autoscroll } from "./components";

import installInfo, { updateInfo } from "./stores/install-info";
import installationPage from "./stores/installation-page";
import installProgress from "./stores/install-progress";

import type { InstallInfo } from "./stores/install-info";
import { 
    getTimezones, getDrives, getPartitions, getUsername, startUpdate,
    checkInternetConnection, startInstallation, getInstallationEvents,
    reboot, getInstallationProgress, getSystemLanguage
} from "./api";
import type { TimezonesResponse, DrivesResponse, PartitionsResponse } from "./api";
import bytesToReadable from "./utils/size";
import type InstallationProgress from "./stores/install-progress";


export { 
    getLanguageStrings, getString, 
    GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, AdditionalFeaturesContent,
    GDLInput,
    installInfo, installationPage, reboot, autoscroll, getSystemLanguage, startUpdate,
    getTimezones, getDrives, getPartitions,
    bytesToReadable, getUsername, updateInfo,
    checkInternetConnection, startInstallation, getInstallationEvents,
    getCityString, getRegionString, getInstallationProgress, installProgress
};

export type {
    InstallInfo,
    TimezonesResponse, DrivesResponse, PartitionsResponse
};