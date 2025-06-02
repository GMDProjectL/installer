#include "depage.hpp"

#include "imgui.h"
#include "installationstate.hpp"
#include "windowstate.hpp"
#include "styleshit.hpp"
#include "titletext.hpp"
#include "font_awesome.h"
#include <format>
#include "languages.hpp"
#include "desktopbutton.hpp"
#include "centeredtext.hpp"
#include "navigation.hpp"

constexpr ImVec2 buttonSize = {400, 300};
constexpr float spacing = 80.0f;

void DEPage::render() {
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, opacity);
    ImGui::Begin("#DEPage", NULL, StyleShit::g_defaultWindowFlags);

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowSize(globalWindowSize);

    ImGui::SetWindowPos({
            flyOffset,
            0
        }, ImGuiCond_Always
    );

    ImGui::SetCursorPosY(40);
    Components::TitleText(std::format("{}  {}",
        ICON_FA_DESKTOP,
        Languages::getLanguageString("desktop_environment")
    ).c_str());

    ImGui::SetCursorPosY(ImGui::GetCursorPosY() + 20);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 40.0});

    Components::CenteredText(std::format("{} {}",
        Languages::getLanguageString("you_selected"),
        (InstallationState::info.de.empty()) ?
            Languages::getLanguageString("no_selection") :
            Languages::getLanguageString(InstallationState::info.de)
    ).c_str(), true);
    
    ImGui::PopStyleVar();

    ImGui::SetCursorPos({
        (globalWindowSize.x - spacing) / 2 - buttonSize.x,
        (globalWindowSize.y - buttonSize.y) / 2
    });
    
    if (Components::DesktopButton("KDE", "./resources/images/kde.png", buttonSize)) {
        InstallationState::info.de = "kde";
    }
    if (ImGui::IsItemHovered(ImGuiHoveredFlags_DelayNormal)) {
        ImGui::SetTooltip("%s", Languages::getLanguageString("kde_description").c_str());
    }

    ImGui::SameLine(0, spacing);

    if (Components::DesktopButton("GNOME", "./resources/images/gnome.png", buttonSize)) {
        InstallationState::info.de = "gnome";
    }
    if (ImGui::IsItemHovered(ImGuiHoveredFlags_DelayNormal)) {
        ImGui::SetTooltip("%s", Languages::getLanguageString("gnome_description").c_str());
    }

#ifndef PASS_INSTALLER_CHECKS
    if (InstallationState::info.de.empty())
        Components::NavigationEx::disableNext = true;
#endif

    ImGui::PopStyleVar();
    ImGui::End();
}