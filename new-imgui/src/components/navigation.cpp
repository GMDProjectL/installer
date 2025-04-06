#include "navigation.hpp"
#include "hoverbutton.h"
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
    ImGui::PushStyleColor(ImGuiCol_Button, {0.1f, 0.1f, 0.1f, 1.f});
    ImGui::PushStyleColor(ImGuiCol_ButtonHovered, {0.15f, 0.15f, 0.15f, 1.f});
    ImGui::PushStyleColor(ImGuiCol_ButtonActive, {0.2f, 0.2f, 0.2f, 1.f});
    ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, {40.f, ImGui::GetStyle().FramePadding.y});

    if (InstallationState::page > 0) {
        
        if (Components::HoverButton(std::format(
            "{}   {}", ICON_FA_CHEVRON_CIRCLE_LEFT, 
            Languages::getLanguageString("back")
        ), {0.f, 0.f})) {

            InstallationState::page--;
        }
    
        ImGui::SameLine(0, 40);
    }

    if (Components::HoverButton(std::format(
        "{}   {}", ICON_FA_CHEVRON_CIRCLE_RIGHT, 
        Languages::getLanguageString("next")
    ), {0.f, 0.f})) {

        InstallationState::page++;
    }

    ImGui::PopStyleVar();
    ImGui::PopStyleColor(3);
    ImGui::PopFont();

    ImGui::End();

}