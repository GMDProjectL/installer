#pragma once
#include <map>
#include <string>
#include "en.hpp"
#include "ru.hpp"

namespace Languages {
    inline std::string g_currentLanguage = "en";
    
    std::string getCurrentLanguage();
    void changeLanguage(const std::string& language);
    std::string getLanguageString(std::string key);

    inline std::map<std::string, std::map<std::string, std::string>> langsMap = {
        {"en", g_englishStrings},
        {"ru", g_russianStrings}
    };
}