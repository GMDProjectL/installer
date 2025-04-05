#include "welcome.hpp"
#include "imgui.h"
#include "titletext.hpp"
#include "windowstate.hpp"

void Welcome::render() {
    ImGui::Begin("Welcome", NULL, 
        ImGuiWindowFlags_NoTitleBar |
        ImGuiWindowFlags_NoDecoration |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoResize |
        ImGuiWindowFlags_NoNav
    );

    ImGui::SetWindowSize({
        400.0, 500.0
    }, ImGuiCond_Always);

    ImGui::SetWindowPos(
        {
            static_cast<float>(WindowState::getWindowSize().x / 2.0 - 200.0),
            static_cast<float>(WindowState::getWindowSize().y / 2.0 - 250.0)
        }, 
        ImGuiCond_Always
    );

    Components::TitleText("Welcome!");

    ImGui::End();
}