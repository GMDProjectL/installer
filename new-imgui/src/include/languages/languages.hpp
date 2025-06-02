#pragma once
#include <string>
#include <map>
#include "en.hpp"
#include "ru.hpp"

namespace Languages {
    inline std::string g_currentLanguage = "en";
    
    std::string getCurrentLanguage();
    void changeLanguage(const std::string& language);
    std::string getLanguageString(std::string key);
    std::string getTimezoneTranslation(std::string countryName);
    std::string getRegionTranslation(std::string regionName);

    inline std::map<std::string, std::unordered_map<std::string, std::string>> langsMap = {
        {"en", g_englishStrings},
        {"ru", g_russianStrings}
    };

    inline std::unordered_map<std::string, std::unordered_map<std::string, std::string>> cityLangsMap {
        {"ru", russianCitiesTranslations}
    };

    inline std::unordered_map<std::string, std::unordered_map<std::string, std::string>> regionLangsMap {
        {"ru", russianRegionsTranslations}
    };
}