import { globalLanguage, getLanguageStrings, getString } from "./lang";
import { GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, GDLInput } from "./components";
import installInfo from "./stores/install-info";
import type { InstallInfo } from "./stores/install-info";
import { getTimezones } from "./api";
import type { TimezonesResponse } from "./api";


export { 
    globalLanguage, getLanguageStrings, getString, 
    GDLButton, SetupPage, SetupPageTitle, SetupPageBottom,
    GDLInput,
    installInfo,
    getTimezones
};

export type {
    InstallInfo,
    TimezonesResponse
};