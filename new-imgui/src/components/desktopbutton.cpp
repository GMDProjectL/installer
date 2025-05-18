//
// Created by shine on 4/6/25.
//
#define IMGUI_DEFINE_MATH_OPERATORS

#include <GL/glew.h>

#include "desktopbutton.hpp"

#include "utils.hpp"

#include <algorithm>

constexpr int hoverSmoothFactorScaling = 5;
constexpr int activeSmoothFactorScaling = 10;
constexpr float imagePadding = 40.f;

using namespace SmoothFactor;

bool Components::DesktopButton(const char* label, const char* imagePath, const ImVec2& size_arg, bool disable, const ImVec4& disableColor) {
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

    item.isUsed = true;
    item.hoverSmoothFactor += (hover ? 1.0f : -1.0f) * dt * hoverSmoothFactorScaling;
    item.hoverSmoothFactor = std::clamp(item.hoverSmoothFactor, 0.f, 1.0f);

    item.activeSmoothFactor += (held ? 1.0f : -1.0f) * dt * activeSmoothFactorScaling;
    item.activeSmoothFactor = std::clamp(item.activeSmoothFactor, 0.0f, 1.0f);

    item.disableSmoothFactor += (disable ? 1.0f : -1.0f) * dt * activeSmoothFactorScaling;
    item.disableSmoothFactor = std::clamp(item.disableSmoothFactor, 0.0f, 1.0f);

    if (auto it = DesktopButtonEx::textureStorage.find(imagePath); it != DesktopButtonEx::textureStorage.end()) {
        DesktopButtonEx::RenderDesktopButton(label, &it->second, bb, labelSize, item, disableColor);

        return isClicked;
    }

    auto texture = &DesktopButtonEx::textureStorage[imagePath];

    if (!Backend::Utils::loadTexture(imagePath, &texture->textureID, &texture->width, &texture->height)) {
        return isClicked;
    }

    DesktopButtonEx::RenderDesktopButton(label, texture, bb, labelSize, item, disableColor);
    return isClicked;
}

void Components::DesktopButtonEx::RenderDesktopButton(const char* label, const Texture* texture, const ImRect& bb, const ImVec2& labelSize, SmoothFactorItem& smoothItem, ImVec4 disableColor) {
    const auto& style = ImGui::GetStyle();

    auto normalColor = ImGui::GetStyleColorVec4(ImGuiCol_Button);   normalColor.w *= style.Alpha;
    auto hoverColor = ImGui::GetStyleColorVec4(ImGuiCol_ButtonHovered); hoverColor.w *= style.Alpha;
    auto activeColor = ImGui::GetStyleColorVec4(ImGuiCol_ButtonActive); activeColor.w *= style.Alpha;
    auto textColor = ImGui::GetStyleColorVec4(ImGuiCol_Text);   textColor.w *= style.Alpha;
    auto disableTextColor = StyleShit::g_ButtonDisabledTextColor; disableTextColor.w *= style.Alpha;
    disableColor.w *= style.Alpha;

    const auto hover = ImLerp(normalColor, hoverColor, smoothItem.hoverSmoothFactor);
    const auto active = ImLerp(hover, activeColor, smoothItem.activeSmoothFactor);
    const auto finalColor = ImLerp(active, disableColor, smoothItem.disableSmoothFactor);
    const auto textFinalColor = ImLerp(textColor, disableTextColor, smoothItem.disableSmoothFactor);

    const auto drawList = ImGui::GetWindowDrawList();

    drawList->AddRectFilled(bb.Min, bb.Max, ImColor(finalColor), style.FrameRounding);

    drawList->AddImageRounded(texture->textureID,
        {bb.Min.x + imagePadding, bb.Min.y + imagePadding},
        {bb.Max.x - imagePadding, bb.Max.y - (bb.GetSize().y / 4)},
        {0, 0},
        {1, 1},
        ImColor(1.f, 1.f, 1.f, style.Alpha),
        style.FrameRounding
    );

    drawList->AddText(
        ImVec2(
            bb.GetCenter().x - labelSize.x / 2,
            bb.GetCenter().y - labelSize.y / 2 + (bb.GetSize().y / 2.75)
        ),
        ImColor(textFinalColor),
        label
    );
}

void Components::DesktopButtonEx::PreloadDETextures() {
    for (auto it : textures) {
        auto item = &textureStorage[it];
        Backend::Utils::loadTexture(it, &item->textureID, &item->width, &item->height);
    }
}