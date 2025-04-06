#include "mutedbutton.hpp"
#include "styleshit.hpp"
#include "hoverbutton.h"


bool Components::MutedButton(std::string label, const ImVec2& size)
{
    ImGui::PushStyleColor(ImGuiCol_Button, StyleShit::g_GlobalBgColor);
    ImGui::PushStyleColor(ImGuiCol_ButtonHovered, {
        StyleShit::g_GlobalBgColor.x + 0.05f,
        StyleShit::g_GlobalBgColor.y + 0.05f,
        StyleShit::g_GlobalBgColor.z + 0.05f,
        StyleShit::g_GlobalBgColor.w
    });
    ImGui::PushStyleColor(ImGuiCol_ButtonActive, {
        StyleShit::g_GlobalBgColor.x + 0.1f,
        StyleShit::g_GlobalBgColor.y + 0.1f,
        StyleShit::g_GlobalBgColor.z + 0.1f,
        StyleShit::g_GlobalBgColor.w
    });

    auto ret = HoverButton(label, size);

    ImGui::PopStyleColor(3);

    return ret;
}
