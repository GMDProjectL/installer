//
// Created by shine on 4/6/25.
//

#include "hoverbutton.hpp"
#include <unordered_map>

bool Components::HoverButton(const std::string& label, const ImVec2& size)
{
    auto buttonNormalColor = ImGui::GetStyleColorVec4(ImGuiCol_Button);
    auto buttonHoverColor = ImGui::GetStyleColorVec4(ImGuiCol_ButtonHovered);
    auto buttonActivatedColor = ImGui::GetStyleColorVec4(ImGuiCol_ButtonActive);
    auto textColor = ImGui::GetStyleColorVec4(ImGuiCol_Text);

    const auto style = ImGui::GetStyle();
    const auto opacity = style.Alpha;

    buttonNormalColor.w *= opacity;
    buttonHoverColor.w *= opacity;
    buttonActivatedColor.w *= opacity;
    textColor.w *= opacity;

    float& smoothFactor = buttonsSmoothFactor[label];

    constexpr auto transparent = ImVec4(0, 0, 0, 0);
    ImGui::PushStyleColor(ImGuiCol_Button, transparent);
    ImGui::PushStyleColor(ImGuiCol_ButtonHovered, transparent);
    ImGui::PushStyleColor(ImGuiCol_ButtonActive, transparent);
    ImGui::PushStyleColor(ImGuiCol_Text, transparent);
    auto isClicked = ImGui::Button(label.c_str(), size);
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

    ImVec4 buttonHoverTransition = ImVec4(
        buttonNormalColor.x + (buttonHoverColor.x - buttonNormalColor.x) * smoothFactor,
        buttonNormalColor.y + (buttonHoverColor.y - buttonNormalColor.y) * smoothFactor,
        buttonNormalColor.z + (buttonHoverColor.z - buttonNormalColor.z) * smoothFactor,
        buttonNormalColor.w + (buttonHoverColor.w - buttonNormalColor.w) * smoothFactor
    );

    if (ImGui::IsItemActive())
        buttonHoverTransition = buttonActivatedColor;

    const auto drawList = ImGui::GetWindowDrawList();
    const auto buttonMin = ImGui::GetItemRectMin();
    const auto buttonMax = ImGui::GetItemRectMax();
    const auto buttonCenterPoint = ImVec2(buttonMax.x - buttonMin.x, buttonMax.y - buttonMin.y);
    const auto textSize = ImGui::CalcTextSize(label.c_str());
    const auto rounding = style.FrameRounding;

    drawList->AddRectFilled(buttonMin, buttonMax, ImColor(buttonHoverTransition), rounding);
    drawList->AddText(ImVec2(buttonMin.x + (buttonCenterPoint.x - textSize.x) / 2, buttonMin.y + (buttonCenterPoint.y - textSize.y) / 2), ImColor(textColor), label.c_str());

    return isClicked;
}
