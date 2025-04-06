#pragma once
#include <vector>

namespace Components {
    inline std::vector<float> circleRadius;
    inline std::vector<std::pair<int, bool>> jobIndexes;
    inline bool initDone = false;
    inline int previousPage = 0;

    void PageCounter(int page, int total);

}
