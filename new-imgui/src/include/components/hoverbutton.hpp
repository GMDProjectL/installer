//
// Created by shine on 4/6/25.
//

#pragma once


#include "styleshit.hpp"
#include <imgui.h>
#include <imgui_internal.h>
#include <unordered_map>

namespace Components {
    inline std::unordered_map<ImGuiID, std::tuple<float, float, float, bool>> buttonsSmoothFactor;
    bool HoverButton(const char* label, const ImVec2& size = {0, 0}, bool disabled = false, ImVec4& disableColor = StyleShit::g_ButtonDisabledColor);
    void RenderHoverButton(const char* label, const ImRect& bb, const ImVec2& labelSize, float hoverSmooth, float activeSmooth, float disableSmooth, ImVec4 disableColor);
    void CleanupHover();
}
