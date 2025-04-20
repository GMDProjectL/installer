//
// Created by shine on 4/6/25.
//

#pragma once


#include "styleshit.hpp"
#include <imgui.h>
#include <imgui_internal.h>
#include <unordered_map>

namespace Components {
    struct SmoothFactorItem {
        float hoverSmoothFactor = 0;
        float activeSmoothFactor = 0;
        float disableSmoothFactor = 0;
        bool isUsed = true;
    };
    
    inline std::unordered_map<ImGuiID, SmoothFactorItem> smoothFactorStore;

    [[nodiscard]]
    bool HoverButton(const char* label, const ImVec2& size = {0, 0}, bool disabled = false, ImVec4& disableColor = StyleShit::g_ButtonDisabledColor);
}

namespace Components::HoverButtonEx {
    void RenderHoverButton(const char* label, const ImRect& bb, const ImVec2& labelSize, float hoverSmooth, float activeSmooth, float disableSmooth, ImVec4 disableColor);
    void CleanupHover();
}
