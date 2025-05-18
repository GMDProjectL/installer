#pragma once

#include <imgui.h>
#include <unordered_map>

namespace SmoothFactor {
    struct SmoothFactorItem {
        float hoverSmoothFactor = 0;
        float activeSmoothFactor = 0;
        float disableSmoothFactor = 0;
        bool isUsed = true;
    };
    
    inline std::unordered_map<ImGuiID, SmoothFactorItem> smoothFactorStore;

    inline void Cleanup() {
        for (auto it = smoothFactorStore.begin(); it != smoothFactorStore.end();) {
            if (it->second.isUsed) it->second.isUsed = false;
            else {
                it = smoothFactorStore.erase(it);
                continue;
            }
            ++it;
        }
    }
}