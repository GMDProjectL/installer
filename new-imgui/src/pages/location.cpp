#define IMGUI_DEFINE_MATH_OPERATORS

#include "location.hpp"

#include "hoverbutton.hpp"
#include "imgui.h"
#include "installationstate.hpp"
#include "styleshit.hpp"
#include "windowstate.hpp"
#include "languages.hpp"
#include "font_awesome.h"
#include <format>
#include "titletext.hpp"
#include "utils.hpp"
#include "centeredtext.hpp"
#include "navigation.hpp"

Location* Location::instance = nullptr;
constexpr float padding = 100.f;
constexpr ImVec2 regionAndCityWindowsSize = { 350.0, 400.0 };

void Location::render() {
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, opacity);
    ImGui::Begin("#Welcome", NULL, StyleShit::g_defaultWindowFlags);

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowSize(globalWindowSize, ImGuiCond_Always);

    ImGui::SetWindowPos(
        {
            transitionX,
            0
        }, 
        ImGuiCond_Always
    );

    auto region = InstallationState::info.timezoneRegion;
    std::string regionStr = "";
    auto pos = region.find("/");
    if (pos != region.npos) {
        regionStr = region.substr(0, pos);
        region.erase(0, pos + 1);
    }
    pos = region.find("/");
    if (pos != region.npos) {
        region.erase(0, pos + 1);
    }

    ImGui::SetCursorPosY(40);
    Components::TitleText(std::format("{}  {}",
        ICON_FA_GLOBE,
        Languages::getLanguageString("where_are_you")
    ).c_str());

    ImGui::SetCursorPosY(ImGui::GetCursorPosY() + 20);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 40.0});

    Components::CenteredText(std::format("{}  {} {}{}",
        ICON_FA_USER,
        Languages::getLanguageString("youre_in"),
        Languages::getCityTranslation(region),
        (regionStr.empty()) ? "" : ", " + Languages::getRegionTranslation(regionStr)
    ).c_str(), true);
    
    ImGui::PopStyleVar();

    ImGui::SetNextWindowPos({
        globalWindowSize.x / 2 - regionAndCityWindowsSize.x - padding / 2 + transitionX,
        (globalWindowSize.y - regionAndCityWindowsSize.y) / 2 
    });

    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {0, 20});

    ImGui::BeginChild("#Regions", regionAndCityWindowsSize, 1, 
        ImGuiWindowFlags_NoTitleBar |
        ImGuiWindowFlags_NoResize |
        ImGuiWindowFlags_NoCollapse |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoNav |
        ImGuiWindowFlags_NoBringToFrontOnFocus |
        ImGuiWindowFlags_AlwaysUseWindowPadding |
        ImGuiWindowFlags_NoBackground
    );

    for (auto regionButton : regionButtonStore) {
        regionButton();
    }
    
    ImGui::EndChild();

    ImGui::SetNextWindowPos({
        (globalWindowSize.x + padding) / 2 + transitionX,
        (globalWindowSize.y - regionAndCityWindowsSize.y) / 2 
    });

    ImGui::BeginChild("#Countries", regionAndCityWindowsSize, 1, 
        ImGuiWindowFlags_NoTitleBar |
        ImGuiWindowFlags_NoResize |
        ImGuiWindowFlags_NoCollapse |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoNav |
        ImGuiWindowFlags_NoBringToFrontOnFocus |
        ImGuiWindowFlags_AlwaysUseWindowPadding |
        ImGuiWindowFlags_NoBackground
    );

    if (!currentRegion) {
        ImGui::SetCursorPos((regionAndCityWindowsSize - ImGui::CalcTextSize(Languages::getLanguageString("select_region").c_str())) / 2);
        ImGui::Text("%s", Languages::getLanguageString("select_region").c_str());
    } else {
        for (auto countryButton : *currentRegion) {
            countryButton();
        }
    }

    ImGui::EndChild();

#ifndef PASS_INSTALLER_CHECKS
    if (InstallationState::info.timezoneRegion.empty()) {
        Components::NavigationEx::disableNext = true;
    }
#endif

    ImGui::PopStyleVar(2);
    ImGui::End();
}

void Location::getRegionButton(const std::string buttonLabel, const std::string region) {
    ImGui::PushID(region.c_str());

    auto clicked = Components::HoverButton(Languages::getRegionTranslation(region).c_str(), {-1, 0});
    ImGui::PopID();

    if (clicked){
        if(auto it = countryButtonMap.find(region); it != countryButtonMap.end()) {
            currentRegion = &it->second;
            return;
        }

        currentRegion = &noCities;
        InstallationState::info.timezoneRegion = region;
    }
}

void Location::getLocationButton(std::string buttonLabel, const std::string location) {
    auto pos = buttonLabel.find("/");
    if (pos != buttonLabel.npos)
        buttonLabel.erase(0, pos + 1);

    ImGui::PushID(location.c_str());
    if(Components::HoverButton(Languages::getCityTranslation(buttonLabel).c_str(), {-1, 0})) {
        InstallationState::info.timezoneRegion = location;
    }
    ImGui::PopID();
}

void Location::getEmptyCityText() {
    ImGui::SetCursorPos((regionAndCityWindowsSize - ImGui::CalcTextSize(Languages::getLanguageString("no_city").c_str())) / 2);
    ImGui::Text("%s", Languages::getLanguageString("no_city").c_str());
}

void Location::initRegions() {
    auto parsedRegions = Backend::Utils::getTimezones();

    for (auto [region, countries] : parsedRegions) {

        regionButtonStore.push_back(std::bind(&Location::getRegionButton, this, region, region));
        
        for (auto country : countries) {
            countryButtonMap[region].push_back(std::bind(
                &Location::getLocationButton,
                this, 
                country, 
                region + "/" + country
            ));
        }

    }
}