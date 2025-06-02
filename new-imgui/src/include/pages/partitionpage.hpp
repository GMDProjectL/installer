#include "basepage.hpp"

class PartitionPage : public BasePage {
public:
    static BasePage* getInstance() {
        static PartitionPage instance;
        return &instance;
    }

    void render() override;
};