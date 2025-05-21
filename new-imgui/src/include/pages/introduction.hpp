#pragma once

#include "basepage.hpp"

class Introduction : public BasePage {
    
    
public:
    static Introduction* getInstance() {
        static Introduction instance;
        return &instance;
    }

    void render() override;
};