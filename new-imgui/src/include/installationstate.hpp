#pragma once
#include "globalview.hpp"
#include "installationinfo.hpp"
#include "basepage.hpp"

inline auto& globalView = GlobalView::getInstance();

namespace InstallationState {

    inline int page = 0;
    inline constexpr int maxPages = 6;
    inline InstallationInfo info;

    void goBack(int count = 1);
    void goNext(int count = 1);

    BasePage* getPageForNum(int num); 
}