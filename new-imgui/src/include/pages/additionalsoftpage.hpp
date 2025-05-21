#include "basepage.hpp"

class AdditionalSoftPage : public BasePage {
    
public:

    static BasePage* getInstance() {
        static AdditionalSoftPage instance;
        return &instance;
    }

    void render() override;
};