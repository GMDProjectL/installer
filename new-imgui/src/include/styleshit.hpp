#pragma once
#include "imgui.h"
#include <unordered_map>

namespace StyleShit {
    enum Fonts {
        titleFont,
        boldFont,
        fontAwesome14px,
        fontAwesome24px
    };

    inline std::unordered_map<Fonts, ImFont*> g_fonts;
    inline ImVec4 g_GlobalBgColor = {0.07f, 0.08f, 0.08f, 1.0f};
    inline ImVec4 g_ButtonDisabledColor = {0.15f, 0.15f, 0.16f, 0.75f};
    inline ImVec4 g_ButtonDisabledTextColor = {0.5f, 0.5f, 0.5f, 1.0f};

    void setupStyles();
    void setupSizes();
    void setupColors();
}