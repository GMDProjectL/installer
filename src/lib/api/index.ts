import type { InstallInfo, UpdateFlags } from "$lib/stores/install-info";
import type { InstallationProgress } from "$lib/stores/install-progress";

const API_BASE_PATH = 'http://localhost:669'


type TimezonesResponse = {
    [string: string]: Array<string>
};

type Drive = {
    model: string,
    size: number
}

type DrivesResponse = {
    [string: string]: Drive
};

type Partition = {
    size: number,
    start: number
};

type PartitionsResponse = {
    [string: string]: Partition
}


const getTimezones = async() : Promise<TimezonesResponse> => {
    const request = await fetch(API_BASE_PATH + '/get_timezones');
    const response = await request.json();

    return response as TimezonesResponse;
}

const getDrives = async() : Promise<DrivesResponse> => {
    const request = await fetch(API_BASE_PATH + '/get_drives');
    const response = await request.json();

    return response as DrivesResponse;
}

const getPartitions = async(drive: string) : Promise<PartitionsResponse> => {
    const request = await fetch(API_BASE_PATH + '/get_partitions/' + drive);
    const response = await request.json();

    return response as PartitionsResponse;
}

const checkInternetConnection = async() : Promise<boolean> => {
    const request = await fetch(API_BASE_PATH + '/check_internet_connection');
    const response = await request.json();

    return response['ok'];
}

const startInstallation = async(installation: InstallInfo) => {
    await fetch(API_BASE_PATH + '/install', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(installation)
    });
}

const startUpdate = async(updateInfo: UpdateFlags) => {
    await fetch(API_BASE_PATH + '/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateInfo)
    });
}


const getInstallationEvents = async(): Promise<Array<string>> => {
    const request = await fetch(API_BASE_PATH + '/get_installation_events');
    const response = await request.json();

    return response['events'] as Array<string>;
}

const getInstallationProgress = async(): Promise<InstallationProgress> => {
    const request = await fetch(API_BASE_PATH + '/get_installation_progress');
    const response = await request.json();

    return response as InstallationProgress;
}

const reboot = async() => {
    const request = await fetch('/reboot');
}

const getSystemLanguage = async(): Promise<string> => {
    const request = await fetch(API_BASE_PATH + '/get_system_language');
    const response = await request.json();

    return (response["lang"] as string).slice(0, 2)
}

const getUsername = async(): Promise<string> => {
    const request = await fetch('/get-username');
    const response = await request.json();

    return response["username"] as string
}

const getDE = async(): Promise<string> => {
    const request = await fetch('/get-de');
    const response = await request.json();

    return response["de"] as string
}


export { 
    getTimezones, getDrives, getPartitions, getUsername, getDE,
    checkInternetConnection, startInstallation, getInstallationEvents, startUpdate,
    reboot, getInstallationProgress, getSystemLanguage
}
export type { TimezonesResponse, DrivesResponse, PartitionsResponse }