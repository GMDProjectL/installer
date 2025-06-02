#include "installationstate.hpp"

#include <font_awesome.h>
#include "welcome.hpp"
#include "introduction.hpp"
#include "invalidpage.hpp"
#include "location.hpp"
#include "depage.hpp"
#include "additionalsoftpage.hpp"
#include "partitionpage.hpp"

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
        case 4:
            return AdditionalSoftPage::getInstance();
        case 5:
            return PartitionPage::getInstance();
        default:
            return InvalidPage::getInstance();
    }
}