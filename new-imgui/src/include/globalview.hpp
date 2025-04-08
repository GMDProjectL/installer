#pragma once

#include "basepage.hpp"

class GlobalView {
    BasePage* currentPage = nullptr;
    BasePage* nextPage = nullptr;

public:
    static GlobalView& getInstance() {
        static GlobalView ret;
        return ret;
    }

    void render();
    void changePage(BasePage* page); 
    void changePageWithTransition(BasePage* page);
};