#include "globalview.hpp"
#include "imgui.h"
#include "installationstate.hpp"
#include "navigation.hpp"
#include "pagecounter.hpp"
#include "welcome.hpp"


void GlobalView::render() {
    switch (InstallationState::page) {
        case 0:
            Welcome::render();
            break;
        
        default:
            ImGui::Begin("#Notfound", NULL, ImGuiWindowFlags_NoTitleBar | ImGuiWindowFlags_NoDecoration);
            ImGui::Text("No page selected");
            ImGui::End();
            break;
    }

    Components::PageCounter(InstallationState::page, 6);

    Components::Navigation();
}