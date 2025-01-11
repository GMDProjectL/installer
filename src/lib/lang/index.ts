import enStrings from './EN.json';
import ruStrings from './RU.json';
import { writable } from 'svelte/store';


let globalLanguage = writable<string>("en");


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


export { globalLanguage, getString, getLanguageStrings };