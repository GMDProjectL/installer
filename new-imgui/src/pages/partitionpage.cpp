#include "partitionpage.hpp"
#include <imgui.h>
#include "styleshit.hpp"
#include "windowstate.hpp"

void PartitionPage::render() {
    ImGui::Begin("#PartitionPage", NULL, StyleShit::g_defaultWindowFlags);

    auto globalWindowSize = WindowState::getWindowSize();
    ImGui::SetWindowSize(globalWindowSize);

    ImGui::SetWindowPos({
            flyOffset,
            0
        }, ImGuiCond_Always
    );



    ImGui::End();
}