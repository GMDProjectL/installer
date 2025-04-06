#include "pagecounter.hpp"
#include "imgui.h"
#include "windowstate.hpp"


void Components::PageCounter(int page, int total) {
    ImGui::Begin("#PageCounter", NULL, 
        ImGuiWindowFlags_NoTitleBar |
        ImGuiWindowFlags_NoDecoration |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoResize |
        ImGuiWindowFlags_NoNav
    );

    ImGui::SetWindowSize({
        100, 50
    }, ImGuiCond_Always);

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowPos(
        {
            globalWindowSize.x / 2.0f - 50.0f,
            globalWindowSize.y - 50.0f
        }, 
        ImGuiCond_Always
    );

    ImDrawList* draw_list = ImGui::GetWindowDrawList();

    ImVec2 pos = ImGui::GetCursorScreenPos();

    for (int i = 0; i < total; i++) {
        ImGui::PushID(i);
        if (i == page) {
            draw_list->AddCircleFilled(pos, 5.0f, IM_COL32(255, 255, 255, 255));
        } else {
            draw_list->AddCircleFilled(pos, 2.0f, IM_COL32(150, 150, 150, 255));
        }
        pos.x += 15.0f;
        ImGui::PopID();
    }

    ImGui::End();

}