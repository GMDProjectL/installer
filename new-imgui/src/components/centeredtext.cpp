#include "components/centeredtext.hpp"
#include "imgui.h"


void Components::CenteredText(const char *text, bool disable) {
    ImGui::SetCursorPosX((ImGui::GetContentRegionAvail().x - ImGui::CalcTextSize(text).x) / 2 + 5);

    if (!disable) {
        ImGui::Text("%s", text);
    }
    else {
        ImGui::TextDisabled("%s", text);
    }
}