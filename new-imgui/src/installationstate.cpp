#include "installationstate.hpp"

#include <font_awesome.h>
#include "welcome.hpp"
#include "introduction.hpp"
#include "invalidpage.hpp"
#include "location.hpp"
#include "depage.hpp"

void InstallationState::goBack(int count) {
    page--;
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
        case 2:
            return Location::getInstance();
        case 3:
            return DEPage::getInstance();
        default:
            return InvalidPage::getInstance();
    }
}