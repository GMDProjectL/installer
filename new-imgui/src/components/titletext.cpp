#include "components/titletext.hpp"
#include "imgui.h"
#include "styleshit.hpp"


void Components::TitleText(const char *text) {
    auto font = StyleShit::g_fonts[StyleShit::Fonts::titleFont];
    ImGui::PushFont(font);
    ImGui::SetCursorPosX((ImGui::GetWindowWidth() - ImGui::CalcTextSize(text).x) / 2);
    ImGui::Text("%s", text);
    ImGui::PopFont();
}
