//
// Created by shine on 4/6/25.
//

#include "components/hoverbutton.hpp"
#include <unordered_map>

bool Components::HoverButton(const std::string& label, const ImVec2& size)
{
    const auto colorFrom = ImGui::GetStyleColorVec4(ImGuiCol_Button);
    const auto colorInto = ImGui::GetStyleColorVec4(ImGuiCol_ButtonHovered);
    const auto colorActivated = ImGui::GetStyleColorVec4(ImGuiCol_ButtonActive);

    float smoothFactor = 0;
    if (buttonsSmoothFactor.contains(label))
    {
        smoothFactor = buttonsSmoothFactor[label];
    } else
    {
        buttonsSmoothFactor[label] = smoothFactor;
    }

    constexpr auto transparent = ImVec4(0, 0, 0, 0);
    ImGui::PushStyleColor(ImGuiCol_Button, transparent);
    ImGui::PushStyleColor(ImGuiCol_ButtonHovered, transparent);
    ImGui::PushStyleColor(ImGuiCol_ButtonActive, transparent);
    ImGui::PushStyleColor(ImGuiCol_Text, transparent);
    auto ret = ImGui::Button(label.c_str(), size);
    ImGui::PopStyleColor(4);

    const auto isHovered = ImGui::IsItemHovered();
    const auto deltaTime = ImGui::GetIO().DeltaTime;

    if (isHovered) {
        smoothFactor += deltaTime * 5;
        if (smoothFactor > 1.0f)
            smoothFactor = 1.0f;
    } else {
        smoothFactor -= deltaTime * 5;
        if (smoothFactor < 0.0f)
            smoothFactor = 0.0f;
    }

    buttonsSmoothFactor[label] = smoothFactor;

    ImVec4 currentColor = ImVec4(
        colorFrom.x + (colorInto.x - colorFrom.x) * smoothFactor,
        colorFrom.y + (colorInto.y - colorFrom.y) * smoothFactor,
        colorFrom.z + (colorInto.z - colorFrom.z) * smoothFactor,
        colorFrom.w + (colorInto.w - colorFrom.w) * smoothFactor
    );

    if (ImGui::IsItemActive())
        currentColor = colorActivated;


    const auto drawList = ImGui::GetWindowDrawList();
    const auto buttonMin = ImGui::GetItemRectMin();
    const auto buttonMax = ImGui::GetItemRectMax();
    const auto center = ImVec2(buttonMax.x - buttonMin.x, buttonMax.y - buttonMin.y);
    const auto textSize = ImGui::CalcTextSize(label.c_str());
    const auto rounding = ImGui::GetStyle().FrameRounding;

    drawList->AddRectFilled(buttonMin, buttonMax, ImColor(currentColor), rounding);
    drawList->AddText(ImVec2(buttonMin.x + (center.x - textSize.x) / 2, buttonMin.y + (center.y - textSize.y) / 2), ImColor(ImGui::GetStyleColorVec4(ImGuiCol_Text)), label.c_str());

    return ret;
}
