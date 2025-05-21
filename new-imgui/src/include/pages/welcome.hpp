#pragma once

#include "basepage.hpp"

class Welcome : public BasePage {

public:
    static Welcome* getInstance() {
        static Welcome instance;
        return &instance;
    }

    void render() override;
};