#include "installationstate.hpp"

#include <font_awesome.h>
#include <format>

#include "hoverbutton.hpp"
#include "languages/languages.hpp"
#include "welcome.hpp"
#include "introduction.hpp"
#include "invalidpage.hpp"

void InstallationState::goBack(int count) {
    page--;
    if (page == 0)
    {
        auto iter = Components::buttonsSmoothFactor.find(std::format(
            "{}   {}", ICON_FA_CHEVRON_CIRCLE_LEFT, Languages::getLanguageString("back")
        ));
        if (iter != Components::buttonsSmoothFactor.end()) {
            Components::buttonsSmoothFactor.erase(iter);
        }
    }
    globalView.changePageWithTransition(getPageForNum(page)); 
}

void InstallationState::goNext(int count) {
    page++;
    globalView.changePageWithTransition(getPageForNum(page));
}

BasePage* InstallationState::getPageForNum(int num) {
    switch (InstallationState::page) {
        case 0:
            return Welcome::getInstance();
        case 1:
            return Introduction::getInstance();
        default:
            return InvalidPage::getInstance();
    }
}