#include "basepage.hpp"

class InvalidPage : public BasePage {
    static InvalidPage* instance;

public:
    static InvalidPage* getInstance() {
        static InvalidPage instance;
        return &instance;
    }
    void render() override;
};