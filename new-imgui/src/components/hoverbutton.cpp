//
// Created by shine on 4/6/25.
//

#include "components/hoverbutton.h"
#include <unordered_map>

std::unordered_map<std::string, float> buttonsSmoothFactor;

bool Components::HoverButton(std::string label, const ImVec2& size)
{
    auto colorFrom = ImGui::GetStyleColorVec4(ImGuiCol_Button);
    auto colorInto = ImGui::GetStyleColorVec4(ImGuiCol_ButtonHovered);
    auto colorActivated = ImGui::GetStyleColorVec4(ImGuiCol_ButtonActive);

    float smoothFactor = 0;
    if (buttonsSmoothFactor.contains(label))
    {
        smoothFactor = buttonsSmoothFactor[label];
    } else
    {
        buttonsSmoothFactor[label] = smoothFactor;
    }

    auto transparent = ImVec4(0, 0, 0, 0);
    ImGui::PushStyleColor(ImGuiCol_Button, transparent);
    ImGui::PushStyleColor(ImGuiCol_ButtonHovered, transparent);
    ImGui::PushStyleColor(ImGuiCol_ButtonActive, transparent);
    auto ret = ImGui::Button(label.c_str(), size);
    ImGui::PopStyleColor(3);

    auto isHovered = ImGui::IsItemHovered();
    auto deltaTime = ImGui::GetIO().DeltaTime;

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


    auto drawList = ImGui::GetWindowDrawList();
    auto buttonMin = ImGui::GetItemRectMin();
    auto buttonMax = ImGui::GetItemRectMax();
    auto center = ImVec2(buttonMax.x - buttonMin.x, buttonMax.y - buttonMin.y);
    auto textSize = ImGui::CalcTextSize(label.c_str());
    auto rounding = ImGui::GetStyle().FrameRounding;

    drawList->AddRectFilled(ImVec2(buttonMin.x + rounding, buttonMin.y + rounding), ImVec2(buttonMax.x - rounding, buttonMax.y - rounding), ImColor(currentColor));
    drawList->AddRectFilled(ImVec2(buttonMin.x, buttonMin.y + rounding), ImVec2(buttonMin.x + rounding, buttonMax.y - rounding), ImColor(currentColor));
    drawList->AddRectFilled(ImVec2(buttonMin.x + rounding, buttonMin.y), ImVec2(buttonMax.x - rounding, buttonMin.y + rounding), ImColor(currentColor));
    drawList->AddRectFilled(ImVec2(buttonMin.x + rounding, buttonMax.y), ImVec2(buttonMax.x - rounding, buttonMax.y - rounding), ImColor(currentColor));
    drawList->AddRectFilled(ImVec2(buttonMax.x - rounding, buttonMin.y + rounding), ImVec2(buttonMax.x, buttonMax.y - rounding), ImColor(currentColor));

    drawList->AddCircleFilled(ImVec2(buttonMin.x + rounding, buttonMin.y + rounding), rounding, ImColor(currentColor));
    drawList->AddCircleFilled(ImVec2(buttonMin.x + rounding, buttonMax.y - rounding), rounding, ImColor(currentColor));
    drawList->AddCircleFilled(ImVec2(buttonMax.x - rounding, buttonMax.y - rounding), rounding, ImColor(currentColor));
    drawList->AddCircleFilled(ImVec2(buttonMax.x - rounding, buttonMin.y + rounding), rounding, ImColor(currentColor));
    drawList->AddText(ImVec2(buttonMin.x + center.x / 2 - textSize.x / 2, buttonMin.y + center.y / 2 - textSize.y / 2), ImColor(ImGui::GetStyleColorVec4(ImGuiCol_Text)), label.c_str());

    return ret;
}
