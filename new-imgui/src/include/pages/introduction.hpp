#pragma once

#include "basepage.hpp"

class Introduction : public BasePage {
public:
    INSTANCE_FUNC(Introduction);

    void render() override;
};