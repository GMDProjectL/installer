#include "globalview.hpp"
#include "imgui.h"
#include "installationstate.hpp"
#include "welcome.hpp"


void GlobalView::render() {
    switch (InstallationState::page) {
        case 0:
            Welcome::render();
            break;
        
        default:
            ImGui::Text("No page selected");
            break;
    }
}