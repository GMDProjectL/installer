import type { InstallInfo, UpdateFlags } from "$lib/stores/install-info";
import type { InstallationProgress } from "$lib/stores/install-progress";

const API_BASE_PATH = 'http://127.0.0.1:669'


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

const getInternetDevices = async(): Promise<Array<Record<string, any>>> => {
    const request = await fetch(API_BASE_PATH + '/get_internet_devices');
    const response = await request.json();

    return Promise.resolve(response)
}

const getAccessPoints = async(device: string): Promise<Array<Record<string, any>>> => {
    const request = await fetch(API_BASE_PATH + `/get_access_points?device=${device}`);
    const response = await request.json();

    return Promise.resolve(response)
}

const checkConnectivity = async (): Promise<number> => {
    const request = await fetch(API_BASE_PATH + '/check_connectivity');
    const response = await request.json();

    return Promise.resolve(response)
};

const addConnection = async (SSID: string, password: string): Promise<Record<string, any>> => {
    const request = await fetch(API_BASE_PATH + '/add_connection', {
        method: 'POST',
        body: JSON.stringify({
            Ssid: SSID,
            password: password
        })
    });

    const response = await request.json();
    return Promise.resolve(response)
};

const activateConnection = async (connection: string, object: string, device: string): Promise<string> => {
    const request = await fetch(API_BASE_PATH + "/activate_connection", {
        method: 'POST',
        body: JSON.stringify({
            connection: connection,
            object: object,
            device: device
        })
    });

    const response = await request.json();
    return Promise.resolve(response)
};

const getActiveConnectionState = async (active_connection: string): Promise<number | string> => {
    const request = await fetch(API_BASE_PATH + `/get_active_connection_state?connection=${active_connection}`);
    const response = await request.json();

    return Promise.resolve(response)
}

const getSavedConnections = async (): Promise<Array<string>> => {
    const request = await fetch(API_BASE_PATH + '/list_connections');
    const response = await request.json();

    return Promise.resolve(response)
};

const getAppliedConnection = async (device: string): Promise<Record<string, any> | string> => {
    const request = await fetch(API_BASE_PATH + `/get_applied_connection?device=${device}`);
    const response = await request.json();

    return Promise.resolve(response)
};

const getConnectionSettings = async (connection: string): Promise<Record<string, any>> => {
    const request = await fetch(API_BASE_PATH + `/get_connection_settings?connection=${connection}`);
    const response = request.json();

    return Promise.resolve(response)
};

const deleteConnection = async (connection: string): Promise<void> => {
    const request = await fetch(API_BASE_PATH + '/delete_connection', {
        method: 'POST',
        body: JSON.stringify({connection: connection})
    });

    return Promise.resolve()
};

const disconnectDevice = async (device: string): Promise<void> => {
    const request = await fetch(API_BASE_PATH + '/disconnect_device', {
        method: 'POST',
        body: JSON.stringify({device: device})
    });

    return Promise.resolve()
};

const updateStatus = async (check_connectivity: boolean = false, list_connections: boolean = false, get_ap: boolean = false, get_applied_connection: boolean = false, device: string = ''): Promise<Record<string, any>> => {
    const request = await fetch(
        API_BASE_PATH + '/update?' +
        `check_connectivity=${check_connectivity}&` +
        `list_connections=${list_connections}&` + 
        `get_ap=${get_ap}&` +
        `get_applied_connection=${get_applied_connection}&` +
        `device=${device}` 
    );
    
    const response = await request.json();
    return Promise.resolve(response)
};

export {
    getTimezones, getDrives, getPartitions, getUsername, getDE,
    checkInternetConnection, startInstallation, getInstallationEvents, startUpdate,
    reboot, getInstallationProgress, getSystemLanguage, getInternetDevices,
    getAccessPoints, checkConnectivity, addConnection, activateConnection, getActiveConnectionState,
    getSavedConnections, getAppliedConnection, getConnectionSettings, deleteConnection, disconnectDevice, updateStatus
}
export type { TimezonesResponse, DrivesResponse, PartitionsResponse }