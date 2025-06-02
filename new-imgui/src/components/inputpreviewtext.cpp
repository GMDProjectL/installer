#include "inputpreviewtext.hpp"
#include "imgui.h"

void Components::InputPreviewText(const char* text, const char* buf) {
    const auto draw = ImGui::GetWindowDrawList();
    const auto& style = ImGui::GetStyle();

    if(!ImGui::IsItemActive() && strlen(buf) == 0) {
        auto min = ImGui::GetItemRectMin();
        auto size = ImGui::GetItemRectSize();
        auto labelSize = ImGui::CalcTextSize(text);

        auto color = ImGui::GetStyleColorVec4(ImGuiCol_TextDisabled);
        color.w *= style.Alpha;

        draw->AddText(
            {
                min.x + style.FramePadding.x,
                min.y + (size.y - labelSize.y) / 2
            },
            ImColor(color),
            text
        );
    }
}