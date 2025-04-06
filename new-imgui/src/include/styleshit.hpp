#pragma once
#include "imgui.h"

namespace StyleShit {

    inline ImFont* g_titleFont;
    inline ImFont* g_boldFont;

    void setupStyles();
    void setupSizes();
    void setupColors();

}