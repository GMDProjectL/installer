import { getLanguageStrings, getString } from "./lang";
import { GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, GDLInput } from "./components";
import installInfo from "./stores/install-info";
import type { InstallInfo } from "./stores/install-info";
import { getTimezones, getDrives, getPartitions, checkInternetConnection, startInstallation } from "./api";
import type { TimezonesResponse, DrivesResponse, PartitionsResponse } from "./api";
import bytesToReadable from "./utils/size";


export { 
    getLanguageStrings, getString, 
    GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
    GDLInput,
    installInfo,
    getTimezones, getDrives, getPartitions,
    bytesToReadable,
    checkInternetConnection, startInstallation
};

export type {
    InstallInfo,
    TimezonesResponse, DrivesResponse, PartitionsResponse
};