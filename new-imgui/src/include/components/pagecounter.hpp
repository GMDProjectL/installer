#pragma once
#include <vector>

namespace Components {
    struct JobItem {
        int pageNum = 0;
        bool increase;
    };

    inline std::vector<float> circleRadius;
    inline std::vector<JobItem> animationQueue;
    inline bool initDone = false;
    inline int previousPage = 0;

    void PageCounter(int page, int total);
}

namespace Components::PageCounterEx {
    void queueAnimation(int previousPage, int currentPage);
    void doAnimationStep();
}
