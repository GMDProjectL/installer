#include "basepage.hpp"

class InvalidPage : public BasePage {
public:
    INSTANCE_FUNC(InvalidPage);

    void render() override;
};