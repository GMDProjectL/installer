#pragma once
#include "imgui.h"

namespace StyleShit {

    inline ImFont* g_titleFont;
    inline ImFont* g_boldFont;
    inline ImFont* g_fontAwesome;

    void setupStyles();
    void setupSizes();
    void setupColors();

}