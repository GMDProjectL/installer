#include "basepage.hpp"

class AdditionalSoftPage : public BasePage {
public:
    INSTANCE_FUNC(AdditionalSoftPage);

    void render() override;
};