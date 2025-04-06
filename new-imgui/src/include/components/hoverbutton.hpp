//
// Created by shine on 4/6/25.
//

#pragma once

#include <imgui.h>
#include <string>
#include <unordered_map>

namespace Components {
    inline std::unordered_map<std::string, float> buttonsSmoothFactor;
    bool HoverButton(std::string label, const ImVec2& size);
}
