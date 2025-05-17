#include "basepage.hpp"

class DEPage : public BasePage {
    static DEPage* instance;
public:

    static BasePage* getInstance() {
        if (!instance) {
            instance = new DEPage();
        }
        return instance;
    }

    void render() override;
};