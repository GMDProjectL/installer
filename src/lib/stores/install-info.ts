import { writable } from "svelte/store";

type InstallInfo = {
    username: string,
    computerName: string,
    password: string,
    password2: string,
    timezoneRegion: string,
    timezoneInfo: string
};

let installInfo = writable<InstallInfo>({
    username: '',
    computerName: '',
    password: '',
    password2: '',
    timezoneRegion: '',
    timezoneInfo: ''
});

export default installInfo;  // Export the store
export type { InstallInfo };  // Export the type definition