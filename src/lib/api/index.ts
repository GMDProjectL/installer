const API_BASE_PATH = 'http://localhost:669'


type TimezonesResponse = {
    [string: string]: Array<string>
};


const getTimezones = async() : Promise<TimezonesResponse> => {
    const request = await fetch(API_BASE_PATH + '/get_timezones');
    const response = await request.json();

    return response as TimezonesResponse;
}


export { getTimezones }
export type { TimezonesResponse }