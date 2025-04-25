#pragma once

#include "basepage.hpp"
#include <functional>
#include <map>
#include <string>
#include <vector>

class Location : public BasePage {
    static Location* instance;
    
public:
    static Location* getInstance() {
        if(!instance) {
            instance = new Location();
        }
        return instance;
    }

    const std::vector<std::function<void()>> noCities = {
        {&getEmptyCityText}
    };

    std::vector<std::function<void()>> regionButtonStore;
    const std::vector<std::function<void()>>* currentRegion = nullptr;
    std::map<std::string, std::vector<std::function<void()>>> countryButtonMap;

    void render() override;
    void initRegions();
    void getRegionButton(const std::string buttonLabel, const std::string region);
    void getLocationButton(std::string buttonLabel, const std::string location);
    static void getEmptyCityText();
};