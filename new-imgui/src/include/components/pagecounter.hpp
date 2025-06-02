#pragma once
#include <deque>
#include <vector>

namespace Components {
    struct AnimationItem {
        int pageNum = 0;
        bool increase;
    };

    namespace {
        inline std::vector<float> circleRadius;
        inline std::deque<AnimationItem> animationQueue;
        inline bool initDone = false;
        inline int previousPage = 0;
    }

    inline constexpr float maxSize = 4.00f;
    inline constexpr float minSize = 2.00f;
    inline constexpr float spacing = 15.0f;
    void PageCounter(int page, int total);
}

namespace Components::PageCounterEx {
    void queueAnimation(int previousPage, int currentPage);
    void updateAnimation();
}
