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


export { getTimezones, getDrives, getPartitions }
export type { TimezonesResponse, DrivesResponse, PartitionsResponse }