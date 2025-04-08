#pragma once

#include "basepage.hpp"

class Introduction : public BasePage {
    static Introduction* instance;
    
public:
    static Introduction* getInstance() {
        if(!instance) {
            instance = new Introduction();
        }
        return instance;
    }

    void render() override;
};