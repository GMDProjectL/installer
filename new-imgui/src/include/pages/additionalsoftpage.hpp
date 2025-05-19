#include "basepage.hpp"

class AdditionalSoftPage : public BasePage {
    static AdditionalSoftPage* instance;
public:

    static BasePage* getInstance() {
        if (!instance) {
            instance = new AdditionalSoftPage();
        }
        return instance;
    }

    void render() override;
};