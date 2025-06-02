#include "invalidpage.hpp"
#include "imgui.h"
#include "styleshit.hpp"
#include "windowstate.hpp"

void InvalidPage::render() {
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, opacity);
    ImGui::Begin("#Notfound", NULL, StyleShit::g_defaultWindowFlags);
    auto globalWindowSize = WindowState::getWindowSize();
    auto notFoundWindowSize = ImGui::CalcTextSize("Invalid page selected");
    ImGui::SetWindowPos(
        {
            globalWindowSize.x / 2.0f - notFoundWindowSize.x / 2.0f + flyOffset,
            globalWindowSize.y / 2.0f - notFoundWindowSize.y / 2.0f
        }, 
        ImGuiCond_Always
    );
    ImGui::Text("Invalid page selected");
    ImGui::End();
    ImGui::PopStyleVar();
}