//
// Created by shine on 4/6/25.
//
#define IMGUI_DEFINE_MATH_OPERATORS

#include "hoverbutton.hpp"
#include <algorithm>

constexpr int hoverSmoothFactorScaling = 5;
constexpr int activeSmoothFactorScaling = 10;

inline ImVec4 ImLerpColor(const ImVec4& firstColor, const ImVec4& secondColor, const float& smoothFactor) {
    return firstColor + (secondColor - firstColor) * smoothFactor;
}

bool Components::HoverButton(const char* label, const ImVec2& size_arg, bool disable, ImVec4& disableColor) {
    const auto& window = ImGui::GetCurrentWindow();
    const auto& style = ImGui::GetStyle();
    const auto  id = window->GetID(label);

    const auto labelSize = ImGui::CalcTextSize(label);
    const auto pos = window->DC.CursorPos;
    const auto size = ImGui::CalcItemSize(size_arg, labelSize.x + style.FramePadding.x * 2.0f, labelSize.y + style.FramePadding.y * 2.0f);

    const ImRect bb(pos, pos + size);
    ImGui::ItemSize(bb, style.FramePadding.y);

    if (!disable && !ImGui::ItemAdd(bb, id))
        return false;

    bool hover, held;

    const auto isClicked = ImGui::ButtonBehavior(bb, id, &hover, &held);
    const auto dt = ImGui::GetIO().DeltaTime;

    if (disable && !smoothFactorStore.contains(id)) {
        smoothFactorStore[id].disableSmoothFactor = 1.0f; // Skips the color transition if disabled from the first call or on language change
    }

    auto& item = smoothFactorStore[id];
    if (!item.isUsed) item.isUsed = true;

    item.hoverSmoothFactor += (hover ? 1.0f : -1.0f) * dt * hoverSmoothFactorScaling;
    item.hoverSmoothFactor = std::clamp(item.hoverSmoothFactor, 0.f, 1.0f);

    item.activeSmoothFactor += (held ? 1.0f : -1.0f) * dt * activeSmoothFactorScaling;
    item.activeSmoothFactor = std::clamp(item.activeSmoothFactor, 0.0f, 1.0f);

    item.disableSmoothFactor += (disable ? 1.0f : -1.0f) * dt * activeSmoothFactorScaling;
    item.disableSmoothFactor = std::clamp(item.disableSmoothFactor, 0.0f, 1.0f);

    RenderHoverButton(label, bb, labelSize, item.hoverSmoothFactor, item.activeSmoothFactor, item.disableSmoothFactor, disableColor);

    return isClicked;
}

void Components::RenderHoverButton(const char *label, const ImRect &bb, const ImVec2 &labelSize, float hoverSmooth, float activeSmooth, float disabledSmooth, ImVec4 disableColor) {
    const auto& style = ImGui::GetStyle();

    auto normalColor = ImGui::GetStyleColorVec4(ImGuiCol_Button);   normalColor.w *= style.Alpha;
    auto hoverColor = ImGui::GetStyleColorVec4(ImGuiCol_ButtonHovered); hoverColor.w *= style.Alpha;
    auto activeColor = ImGui::GetStyleColorVec4(ImGuiCol_ButtonActive); activeColor.w *= style.Alpha;
    auto textColor = ImGui::GetStyleColorVec4(ImGuiCol_Text);   textColor.w *= style.Alpha;
    auto disableTextColor = StyleShit::g_ButtonDisabledTextColor; disableTextColor.w *= style.Alpha;
    disableColor.w *= style.Alpha;

    const auto hover = ImLerpColor(normalColor, hoverColor, hoverSmooth);
    const auto active = ImLerpColor(hover, activeColor, activeSmooth);
    const auto finalColor = ImLerpColor(active, disableColor, disabledSmooth);
    const auto textFinalColor = ImLerpColor(textColor, disableTextColor, disabledSmooth);

    const auto drawList = ImGui::GetWindowDrawList();
    drawList->AddRectFilled(bb.Min, bb.Max, ImColor(finalColor), style.FrameRounding);
    drawList->AddText(
        ImVec2(
            bb.GetCenter().x - labelSize.x / 2,
            bb.GetCenter().y - labelSize.y / 2
        ),
        ImColor(textFinalColor),
        label
    );
}

void Components::CleanupHover() {
    for (auto it = smoothFactorStore.begin(); it != smoothFactorStore.end();) {
        auto& isUsed = it->second.isUsed;
        if (isUsed) isUsed = false;
        else {
            it = smoothFactorStore.erase(it);
            continue;
        }
        ++it;
    }
}