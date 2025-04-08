#include "basepage.hpp"

class InvalidPage : public BasePage {
    static InvalidPage* instance;

public:
    static InvalidPage* getInstance() {
        if (!instance) {
            instance = new InvalidPage();
        }
        return instance;
    }
    void render() override;
};