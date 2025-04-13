#include "installationstate.hpp"

#include <font_awesome.h>
#include "welcome.hpp"
#include "introduction.hpp"
#include "invalidpage.hpp"

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
        default:
            return InvalidPage::getInstance();
    }
}