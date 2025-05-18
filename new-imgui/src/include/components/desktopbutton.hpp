//
// Created by shine on 4/6/25.
//

#pragma once

#include "styleshit.hpp"
#include <imgui.h>
#include <imgui_internal.h>
#include "smoothfactor.hpp"
#include <array>
#include <string>

namespace Components {
    [[nodiscard]]
    bool DesktopButton(const char* label, const char* imagePath, const ImVec2& size = {0, 0}, bool disabled = false, const ImVec4& disableColor = StyleShit::g_ButtonDisabledColor);
}

namespace Components::DesktopButtonEx {
    struct Texture {
        unsigned int textureID;
        int width = 0, height = 0;
    };
    
    namespace {
        std::array<const char*, 2> textures = {
            "./resources/images/kde.png",
            "./resources/images/gnome.png"
        };
        inline std::unordered_map<std::string, Texture> textureStorage;
    }

    void RenderDesktopButton(const char* label, const Texture* texture, const ImRect& bb, const ImVec2& labelSize, SmoothFactor::SmoothFactorItem& smoothItem, ImVec4 disableColor);
    void CleanupHover();
    void PreloadDETextures();
}
