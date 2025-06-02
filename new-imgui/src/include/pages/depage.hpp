#include "basepage.hpp"

class DEPage : public BasePage {
public:
    INSTANCE_FUNC(DEPage);

    void render() override;
};