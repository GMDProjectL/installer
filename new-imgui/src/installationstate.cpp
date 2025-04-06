#include "installationstate.hpp"

#include <font_awesome.h>
#include <format>

#include "hoverbutton.hpp"
#include "languages/languages.hpp"

void InstallationState::goBack(int count) {
    page--;
    if (page == 0)
    {
        auto iter = Components::buttonsSmoothFactor.find(std::format(
            "{}   {}", ICON_FA_CHEVRON_CIRCLE_LEFT, Languages::getLanguageString("back")
        ));
        if (iter != Components::buttonsSmoothFactor.end())
        {
            Components::buttonsSmoothFactor.erase(iter);
        }
    }
}

void InstallationState::goNext(int count) {
    page++;
}