#include "basepage.hpp"

class PartitionPage : public BasePage {
public:
    INSTANCE_FUNC(PartitionPage);

    void render() override;
};