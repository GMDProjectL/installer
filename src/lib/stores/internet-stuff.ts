import { writable } from "svelte/store";

let currentInternetDevice = writable<Record<string, any> | undefined>(undefined);
let doSkippedInternetSetup = writable<boolean>(false);
let internetDevices = writable<Array<Record<string, any>>>([]);

export { currentInternetDevice, doSkippedInternetSetup, internetDevices };