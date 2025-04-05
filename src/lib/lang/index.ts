import enStrings from './EN.json';
import ruStrings from './RU.json';


const getLanguageStrings = (lang: string) => {
    if (lang === "en") return enStrings;
    if (lang === "ru") return ruStrings;
    return enStrings;
}


const getString = (lang: string, key: string) : string => {
    const langStrings = getLanguageStrings(lang);

    // @ts-ignore
    return langStrings[key] ?? key;
}

const getRegionString = (lang: string, key: string) : string => {
    const langStrings = getLanguageStrings(lang);

    if (!('regions-translations' in langStrings)) {
        return key;
    }
    
    // @ts-ignore
    return langStrings['regions-translations'][key] ?? key;
}

const getCityString = (lang: string, key: string) : string => {
    const langStrings = getLanguageStrings(lang);

    if (!('cities-translations' in langStrings)) {
        return key;
    }
    
    // @ts-ignore
    return langStrings['cities-translations'][key] ?? key;
}


export { getString, getLanguageStrings, getRegionString, getCityString };