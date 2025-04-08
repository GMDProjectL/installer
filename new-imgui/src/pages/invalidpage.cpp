#include "invalidpage.hpp"
#include "imgui.h"
#include "windowstate.hpp"

InvalidPage* InvalidPage::instance = nullptr;

void InvalidPage::render() {
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, opacity);
    ImGui::Begin("#Notfound", NULL, ImGuiWindowFlags_NoDecoration | ImGuiWindowFlags_NoMove);
    auto globalWindowSize = WindowState::getWindowSize();
    auto notFoundWindowSize = ImGui::CalcTextSize("Invalid page selected");
    ImGui::SetWindowPos(
        {
            globalWindowSize.x / 2.0f - notFoundWindowSize.x / 2.0f + transitionX,
            globalWindowSize.y / 2.0f - notFoundWindowSize.y / 2.0f
        }, 
        ImGuiCond_Always
    );
    ImGui::Text("Invalid page selected");
    ImGui::End();
    ImGui::PopStyleVar();
}