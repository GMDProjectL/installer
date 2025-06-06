#include "styleshit.hpp"

void StyleShit::setupStyles() {
    setupSizes();
    setupColors();
}

void StyleShit::setupSizes() {
    ImGuiStyle& style = ImGui::GetStyle();

    style.WindowPadding = ImVec2(15, 15);
    style.FramePadding = ImVec2(10, 17);
    style.ItemSpacing = ImVec2(8, 4);
    style.ItemInnerSpacing = ImVec2(6, 6);
    style.IndentSpacing = 22.0f;
    style.ScrollbarSize = 12.0f;
    style.GrabMinSize = 12.0f;
    style.WindowBorderSize = 0.0f;
    style.ChildBorderSize = 0.0f;
    style.PopupBorderSize = 0.0f;
    style.FrameBorderSize = 0.0f;
    style.WindowRounding = 12.0f;
    style.ChildRounding = 7.0f;
    style.FrameRounding = 6.0f;
    style.PopupRounding = 12.0f;
    style.ScrollbarRounding = 10.0f;
    style.GrabRounding = 8.0f;


}

void StyleShit::setupColors() {
    auto colors = ImGui::GetStyle().Colors;
    colors[ImGuiCol_Text]                       = ImVec4(0.80f, 0.79f, 0.76f, 1.00f);
    colors[ImGuiCol_TextDisabled]               = ImVec4(0.63f, 0.63f, 0.66f, 1.00f);
    colors[ImGuiCol_WindowBg]                   = ImVec4(0.00f, 0.00f, 0.00f, 1.00f);
    colors[ImGuiCol_ChildBg]                    = ImVec4(0.00f, 0.00f, 0.00f, 0.50f);
    colors[ImGuiCol_PopupBg]                    = ImVec4(0.08f, 0.08f, 0.08f, 0.94f);
    colors[ImGuiCol_Border]                     = ImVec4(0.43f, 0.43f, 0.50f, 0.50f);
    colors[ImGuiCol_BorderShadow]               = ImVec4(0.00f, 0.00f, 0.00f, 0.00f);
    colors[ImGuiCol_FrameBg]                    = ImVec4(0.21f, 0.21f, 0.21f, 0.54f);
    colors[ImGuiCol_FrameBgHovered]             = ImVec4(0.45f, 0.45f, 0.45f, 0.40f);
    colors[ImGuiCol_FrameBgActive]              = ImVec4(0.74f, 0.74f, 0.74f, 0.67f);
    colors[ImGuiCol_TitleBg]                    = ImVec4(0.04f, 0.04f, 0.04f, 1.00f);
    colors[ImGuiCol_TitleBgActive]              = ImVec4(0.30f, 0.30f, 0.30f, 1.00f);
    colors[ImGuiCol_TitleBgCollapsed]           = ImVec4(0.00f, 0.00f, 0.00f, 0.51f);
    colors[ImGuiCol_MenuBarBg]                  = ImVec4(0.14f, 0.14f, 0.14f, 1.00f);
    colors[ImGuiCol_ScrollbarBg]                = ImVec4(0.31f, 0.31f, 0.31f, 0.25f);
    colors[ImGuiCol_ScrollbarGrab]              = ImVec4(0.31f, 0.31f, 0.31f, 1.00f);
    colors[ImGuiCol_ScrollbarGrabHovered]       = ImVec4(0.41f, 0.41f, 0.41f, 1.00f);
    colors[ImGuiCol_ScrollbarGrabActive]        = ImVec4(0.51f, 0.51f, 0.51f, 1.00f);
    colors[ImGuiCol_CheckMark]                  = ImVec4(0.85f, 0.85f, 0.85f, 1.00f);
    colors[ImGuiCol_SliderGrab]                 = ImVec4(0.59f, 0.59f, 0.59f, 1.00f);
    colors[ImGuiCol_SliderGrabActive]           = ImVec4(1.00f, 1.00f, 1.00f, 1.00f);
    colors[ImGuiCol_Button]                     = ImVec4(0.15f, 0.15f, 0.16f, 0.75f);
    colors[ImGuiCol_ButtonHovered]              = ImVec4(0.25f, 0.25f, 0.27f, 0.75f);
    colors[ImGuiCol_ButtonActive]               =                      colors[ImGuiCol_Button];
    colors[ImGuiCol_Header]                     = ImVec4(0.33f, 0.33f, 0.33f, 0.31f);
    colors[ImGuiCol_HeaderHovered]              = ImVec4(0.97f, 0.97f, 0.96f, 0.80f);
    colors[ImGuiCol_HeaderActive]               = ImVec4(0.30f, 0.30f, 0.30f, 1.00f);
    colors[ImGuiCol_Separator]                  = ImVec4(0.47f, 0.47f, 0.47f, 0.50f);
    colors[ImGuiCol_SeparatorHovered]           = ImVec4(0.48f, 0.48f, 0.48f, 0.78f);
    colors[ImGuiCol_SeparatorActive]            = ImVec4(0.31f, 0.31f, 0.31f, 1.00f);
    colors[ImGuiCol_ResizeGrip]                 = ImVec4(0.43f, 0.43f, 0.43f, 0.20f);
    colors[ImGuiCol_ResizeGripHovered]          = ImVec4(0.41f, 0.41f, 0.41f, 0.67f);
    colors[ImGuiCol_ResizeGripActive]           = ImVec4(0.36f, 0.36f, 0.36f, 0.95f);
    colors[ImGuiCol_InputTextCursor]            = ImVec4(1.00f, 1.00f, 1.00f, 1.00f);
    colors[ImGuiCol_TabHovered]                 = ImVec4(0.29f, 0.29f, 0.29f, 0.80f);
    colors[ImGuiCol_Tab]                        = ImVec4(0.19f, 0.19f, 0.19f, 0.86f);
    colors[ImGuiCol_TabSelected]                = ImVec4(0.32f, 0.32f, 0.32f, 1.00f);
    colors[ImGuiCol_TabSelectedOverline]        = ImVec4(0.50f, 0.50f, 0.50f, 1.00f);
    colors[ImGuiCol_TabDimmed]                  = ImVec4(0.05f, 0.05f, 0.05f, 0.97f);
    colors[ImGuiCol_TabDimmedSelected]          = ImVec4(0.08f, 0.08f, 0.08f, 1.00f);
    colors[ImGuiCol_TabDimmedSelectedOverline]  = ImVec4(0.50f, 0.50f, 0.50f, 0.00f);
    colors[ImGuiCol_PlotLines]                  = ImVec4(0.61f, 0.61f, 0.61f, 1.00f);
    colors[ImGuiCol_PlotLinesHovered]           = ImVec4(1.00f, 0.43f, 0.35f, 1.00f);
    colors[ImGuiCol_PlotHistogram]              = ImVec4(0.90f, 0.70f, 0.00f, 1.00f);
    colors[ImGuiCol_PlotHistogramHovered]       = ImVec4(1.00f, 0.60f, 0.00f, 1.00f);
    colors[ImGuiCol_TableHeaderBg]              = ImVec4(0.19f, 0.19f, 0.20f, 1.00f);
    colors[ImGuiCol_TableBorderStrong]          = ImVec4(0.31f, 0.31f, 0.35f, 1.00f);
    colors[ImGuiCol_TableBorderLight]           = ImVec4(0.23f, 0.23f, 0.25f, 1.00f);
    colors[ImGuiCol_TableRowBg]                 = ImVec4(0.00f, 0.00f, 0.00f, 0.00f);
    colors[ImGuiCol_TableRowBgAlt]              = ImVec4(1.00f, 1.00f, 1.00f, 0.06f);
    colors[ImGuiCol_TextLink]                   = ImVec4(0.26f, 0.59f, 0.98f, 1.00f);
    colors[ImGuiCol_TextSelectedBg]             = ImVec4(0.26f, 0.59f, 0.98f, 0.35f);
    colors[ImGuiCol_DragDropTarget]             = ImVec4(1.00f, 1.00f, 0.00f, 0.90f);
    colors[ImGuiCol_NavCursor]                  = ImVec4(0.26f, 0.59f, 0.98f, 1.00f);
    colors[ImGuiCol_NavWindowingHighlight]      = ImVec4(1.00f, 1.00f, 1.00f, 0.70f);
    colors[ImGuiCol_NavWindowingDimBg]          = ImVec4(0.80f, 0.80f, 0.80f, 0.20f);
    colors[ImGuiCol_ModalWindowDimBg]           = ImVec4(0.80f, 0.80f, 0.80f, 0.35f);
}