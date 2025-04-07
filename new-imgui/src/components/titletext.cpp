#include "components/titletext.hpp"
#include "imgui.h"
#include "styleshit.hpp"


void Components::TitleText(const char *text) {
    ImGui::PushFont(StyleShit::g_titleFont);
    ImGui::SetCursorPosX((ImGui::GetWindowWidth() - ImGui::CalcTextSize(text).x) / 2);
    ImGui::Text("%s", text);
    ImGui::PopFont();
}
