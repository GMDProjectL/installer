#include "navigation.hpp"
#include "imgui.h"
#include "installationstate.hpp"
#include "styleshit.hpp"
#include "windowstate.hpp"
#include "font_awesome.h"
#include "languages.hpp"
#include <format>


void Components::Navigation() {
    ImGui::Begin("#Navigation", NULL, 
        ImGuiWindowFlags_NoTitleBar |
        ImGuiWindowFlags_NoDecoration |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoResize |
        ImGuiWindowFlags_NoNav
    );

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowSize({
        -1.f, 100.0f
    }, ImGuiCond_Always);

    ImGui::SetWindowPos(
        {
            globalWindowSize.x - ImGui::GetWindowWidth(),
            globalWindowSize.y - 100.0f
        }, 
        ImGuiCond_Always
    );

    ImGui::PushFont(StyleShit::g_fontAwesome);
    ImGui::PushStyleColor(ImGuiCol_Button, ImU32(ImColor{ 0, 0, 0, 0 }));
    ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, {40.f, ImGui::GetStyle().FramePadding.y});

    if (InstallationState::page > 0) {

        if (ImGui::Button(std::format(
            "{}   {}", ICON_FA_CHEVRON_CIRCLE_LEFT, 
            Languages::getLanguageString("back")
        ).c_str())) {

            InstallationState::page--;
        }
    
        ImGui::SameLine(0, 40);
    }

    if (ImGui::Button(std::format(
        "{}   {}", ICON_FA_CHEVRON_CIRCLE_RIGHT, 
        Languages::getLanguageString("next")
    ).c_str())) {

        InstallationState::page++;
    }

    ImGui::PopStyleVar();
    ImGui::PopStyleColor();
    ImGui::PopFont();

    ImGui::End();

}