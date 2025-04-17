#include "navigation.hpp"
#include "mutedbutton.hpp"
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
    ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, {40.f, ImGui::GetStyle().FramePadding.y});


    if (Components::MutedButton(std::format(
        "{}   {}", ICON_FA_CHEVRON_CIRCLE_LEFT, Languages::getLanguageString("back")
    ).c_str(), {0.f, 0.f}, !(InstallationState::page > 0))) {

        InstallationState::goBack();
    }

    ImGui::SameLine(0, 40);

    if (Components::MutedButton(std::format(
        "{}   {}", ICON_FA_CHEVRON_CIRCLE_RIGHT, Languages::getLanguageString("next")
    ).c_str(), {0.f, 0.f}, !(InstallationState::page < InstallationState::maxPages - 1))) {

        InstallationState::goNext();
    }

    ImGui::PopStyleVar();
    ImGui::PopFont();

    ImGui::End();

}