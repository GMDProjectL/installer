#pragma once
#include "imgui.h"

namespace StyleShit {

    inline ImFont* g_titleFont;
    inline ImFont* g_boldFont;
    inline ImFont* g_fontAwesome;
    inline ImVec4 g_GlobalBgColor = {0.1f, 0.1f, 0.1f, 1.0f};
    inline ImVec4 g_ButtonDisabledColor = {0.12f, 0.12f, 0.12f, 1.0f};
    inline ImVec4 g_ButtonDisabledTextColor = {0.5f, 0.5f, 0.5f, 1.0f};

    void setupStyles();
    void setupSizes();
    void setupColors();

}