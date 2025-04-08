#pragma once

#include "basepage.hpp"

class Welcome : public BasePage {
    static Welcome* instance;

public:
    static Welcome* getInstance() {
        if (!instance) {
            instance = new Welcome();
        }
        return instance;
    }

    void render() override;
};