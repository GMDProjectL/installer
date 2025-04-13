//
// Created by shine on 4/6/25.
//
#include <iostream>
#define IMGUI_DEFINE_MATH_OPERATORS

#include "hoverbutton.hpp"
#include <algorithm>

constexpr int hoverSmoothFactorScaling = 5;
constexpr int activeSmoothFactorScaling = 10;

template<typename Tuple>
decltype(auto) getLast(Tuple&& tuple) {
    constexpr std::size_t last = std::tuple_size_v<std::remove_reference_t<Tuple>> - 1;
    return std::get<last>(std::forward<Tuple>(tuple));
}

template<typename Tuple, std::size_t N = 0>
void logTuple(Tuple&& tuple, const char* label) {
    if constexpr (N < std::tuple_size_v<std::remove_reference_t<Tuple>>) {
        if (N == 0) std::cout << label << ": ";
        std::cout << std::get<N>(std::forward<Tuple>(tuple)) << " ";
        logTuple<Tuple, N + 1>(std::forward<Tuple>(tuple), label);
    } else {
        std::cout << std::endl;
    }
}

inline ImVec4 ImLerpColor(const ImVec4& firstColor, const ImVec4& secondColor, const float& smoothFactor) {
    return firstColor + (secondColor - firstColor) * smoothFactor;
}

bool Components::HoverButton(const char* label, const ImVec2& size_arg, bool disable, ImVec4& disableColor) {
    const auto window = ImGui::GetCurrentWindow();
    const auto& style = ImGui::GetStyle();
    const auto id = window->GetID(label);

    const auto labelSize = ImGui::CalcTextSize(label);
    const auto pos = window->DC.CursorPos;
    const auto size = ImGui::CalcItemSize(size_arg, labelSize.x + style.FramePadding.x * 2.0f, labelSize.y + style.FramePadding.y * 2.0f);

    const ImRect bb(pos, pos + size);
    ImGui::ItemSize(bb, style.FramePadding.y);
    
    if (!disable)
        if (!ImGui::ItemAdd(bb, id))
            return false;

    bool hover, held;
    auto isClicked = ImGui::ButtonBehavior(bb, id, &hover, &held);

    const auto dt = ImGui::GetIO().DeltaTime;
    auto& [hoverSmoothFactor, activeSmoothFactor, disableSmoothFactor, isUsed] = buttonsSmoothFactor[id];
    if (!isUsed) isUsed = true;

    hoverSmoothFactor += (hover ? 1.0f : -1.0f) * dt * hoverSmoothFactorScaling;
    hoverSmoothFactor = std::clamp(hoverSmoothFactor, 0.f, 1.0f);

    activeSmoothFactor += (held ? 1.0f : -1.0f) * dt * activeSmoothFactorScaling;
    activeSmoothFactor = std::clamp(activeSmoothFactor, 0.0f, 1.0f);

    disableSmoothFactor += (disable ? 1.0f : -1.0f) * dt * activeSmoothFactorScaling;
    disableSmoothFactor = std::clamp(disableSmoothFactor, 0.0f, 1.0f);

    RenderHoverButton(label, bb, labelSize, hoverSmoothFactor, activeSmoothFactor, disableSmoothFactor, disableColor);

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
    for (auto it = buttonsSmoothFactor.begin(); it != buttonsSmoothFactor.end();) {
        auto& isUsed = getLast(it->second);
        if (isUsed) isUsed = false;
        else {
            it = buttonsSmoothFactor.erase(it);
            continue;
        }
        ++it;
    }
}