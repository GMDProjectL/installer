#include "languages.hpp"
#include <map>

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