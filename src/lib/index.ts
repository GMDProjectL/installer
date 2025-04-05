import { getLanguageStrings, getString, getCityString, getRegionString } from "./lang";
import { GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, GDLInput } from "./components";

import installInfo from "./stores/install-info";
import installationPage from "./stores/installation-page";
import installProgress from "./stores/install-progress";

import type { InstallInfo } from "./stores/install-info";
import { 
    getTimezones, getDrives, getPartitions, 
    checkInternetConnection, startInstallation, getInstallationEvents,
    reboot, getInstallationProgress
} from "./api";
import type { TimezonesResponse, DrivesResponse, PartitionsResponse } from "./api";
import bytesToReadable from "./utils/size";
import type InstallationProgress from "./stores/install-progress";


export { 
    getLanguageStrings, getString, 
    GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
    GDLInput,
    installInfo, installationPage, reboot,
    getTimezones, getDrives, getPartitions,
    bytesToReadable,
    checkInternetConnection, startInstallation, getInstallationEvents,
    getCityString, getRegionString, getInstallationProgress, installProgress
};

export type {
    InstallInfo,
    TimezonesResponse, DrivesResponse, PartitionsResponse
};