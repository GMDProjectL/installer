#include "languages.hpp"

void Languages::changeLanguage(const std::string &language) {
    g_currentLanguage = language;
}

std::string Languages::getCurrentLanguage() {
    return g_currentLanguage;
}

std::string Languages::getLanguageString(std::string key) {
    if (langsMap.find(g_currentLanguage) != langsMap.end() 
        && langsMap[g_currentLanguage].find(key) != langsMap[g_currentLanguage].end()) {
    
        return langsMap[g_currentLanguage][key];
    } else {
        return key;
    }
}

std::string Languages::getTimezoneTranslation(std::string countryName) {
    if (g_currentLanguage == "en" || !cityLangsMap[g_currentLanguage].contains(countryName))
        return countryName;

    return cityLangsMap[g_currentLanguage][countryName];
}

std::string Languages::getRegionTranslation(std::string regionName) {
    if (g_currentLanguage == "en" || !regionLangsMap[g_currentLanguage].contains(regionName))
        return regionName;

    return regionLangsMap[g_currentLanguage][regionName];
}