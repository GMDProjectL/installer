#include "basepage.hpp"

class DEPage : public BasePage {
    
public:

    static BasePage* getInstance() {
        static DEPage instance;
        return &instance;
    }

    void render() override;
};