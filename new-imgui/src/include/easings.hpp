#include <cmath>

namespace Easings {
    inline float easeInExpo(float t) {
        return t == 0 ? 0 : pow(2, 10 * (t - 1));
    }

    inline float easeOutExpo(float t) {
        return t == 1 ? 1 : 1 - pow(2, -10 * t);
    }

    inline float easeInOutCubic(float t) {
        return t < 0.5
            ? 4 * t * t * t
            : 1 - pow(-2 * t + 2, 3) / 2;
    }
}