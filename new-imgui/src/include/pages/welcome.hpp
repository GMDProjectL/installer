#pragma once

#include "basepage.hpp"

class Welcome : public BasePage {
public:
    INSTANCE_FUNC(Welcome);

    void render() override;
};