//
// Created by shine on 4/6/25.
//

#pragma once


#include "styleshit.hpp"
#include <imgui.h>
#include <imgui_internal.h>

namespace Components {
    [[nodiscard]]
    bool HoverButton(const char* label, const ImVec2& size = {0, 0}, bool disabled = false, const ImVec4& disableColor = StyleShit::g_ButtonDisabledColor);
}

namespace Components::HoverButtonEx {
    void RenderHoverButton(const char* label, const ImRect& bb, const ImVec2& labelSize, float hoverSmooth, float activeSmooth, float disableSmooth, ImVec4 disableColor);
}
