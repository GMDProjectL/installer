#include "additionalsoftpage.hpp"

#include "imgui.h"
#include "installationstate.hpp"
#include "windowstate.hpp"
#include "styleshit.hpp"
#include "titletext.hpp"
#include "font_awesome.h"
#include <format>
#include "languages.hpp"
#include "navigation.hpp"

constexpr float intendation = 50.0f;
constexpr float windowWidth = 500.0f;

void AdditionalSoftPage::render() {
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, opacity);
    ImGui::Begin("#AdditionalSoftPage", NULL, StyleShit::g_defaultWindowFlags);

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowSize(globalWindowSize);

    ImGui::SetWindowPos({
            flyOffset,
            0
        }, ImGuiCond_Always
    );

    ImGui::SetCursorPosY(40);
    Components::TitleText(std::format("{}  {}",
        ICON_FA_MAGIC,
        Languages::getLanguageString("additional_software")
    ).c_str());

    ImGui::SetNextWindowPos({(WindowState::getWindowSize().x - windowWidth) / 2 + flyOffset, ImGui::GetCursorPosY() + 60});
    
    ImGui::BeginChild("#Checkboxes", {windowWidth, WindowState::getWindowSize().y - ImGui::GetCursorPosY() - 60}, ImGuiChildFlags_None, StyleShit::g_defaultWindowFlags);
    ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, {6,6});
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {8, 16});
    ImGui::PushStyleVar(ImGuiStyleVar_ItemInnerSpacing, {12, 6});


    ImGui::Checkbox(
        std::format(
            "{}   {}",
            Languages::getLanguageString("enable_multilib_repo"),
            ICON_FA_MAGIC
        ).c_str(),
        &InstallationState::info.enableMultilibRepo
    );

    if(!InstallationState::info.enableMultilibRepo) {
        InstallationState::info.installSteam = false;
        InstallationState::info.vulkanIntel = false;
        InstallationState::info.vulkanNvidia = false;
        InstallationState::info.vulkanAmd = false;
        InstallationState::info.installWine = false;
        InstallationState::info.installWinetricks = false;
    }

    ImGui::BeginDisabled(!InstallationState::info.enableMultilibRepo);
        ImGui::Checkbox(
            std::format(
                "{}   {}",
                Languages::getLanguageString("install_steam"),
                ICON_FA_SHOPPING_BAG
            ).c_str(),
            &InstallationState::info.installSteam
        );

        if (!InstallationState::info.installSteam) {
            InstallationState::info.vulkanIntel = false;
            InstallationState::info.vulkanNvidia = false;
            InstallationState::info.vulkanAmd = false;
        }

        ImGui::BeginDisabled(!InstallationState::info.installSteam);
            ImGui::SetCursorPosX(ImGui::GetCursorPosX() + intendation);
            ImGui::Checkbox(
                "HD / UHD / Iris / Arc Graphics",
                &InstallationState::info.vulkanIntel
            );

            ImGui::SetCursorPosX(ImGui::GetCursorPosX() + intendation);
            ImGui::Checkbox(
                "NVIDIA",
                &InstallationState::info.vulkanNvidia
            );

            ImGui::SetCursorPosX(ImGui::GetCursorPosX() + intendation);
            ImGui::Checkbox(
                "AMD",
                &InstallationState::info.vulkanAmd
            );
        ImGui::EndDisabled();
        
        ImGui::Checkbox(
            Languages::getLanguageString("install_wine").c_str(),
            &InstallationState::info.installWine
        );

        if (!InstallationState::info.installWine) {
            InstallationState::info.installWinetricks = false;
        }

        ImGui::BeginDisabled(!InstallationState::info.installWine);
            ImGui::SetCursorPosX(ImGui::GetCursorPosX() + intendation);
            ImGui::Checkbox(
                Languages::getLanguageString("install_winetricks").c_str(),
                &InstallationState::info.installWinetricks
            );
        ImGui::EndDisabled();
    ImGui::EndDisabled();

    ImGui::Checkbox(
        Languages::getLanguageString("install_gnome_disks").c_str(),
        &InstallationState::info.installGnomeDisks
    );

    ImGui::Checkbox(
        Languages::getLanguageString("install_intel_media").c_str(),
        &InstallationState::info.installIntelMedia
    );

    ImGui::Checkbox(
        Languages::getLanguageString("setup_bluetooth").c_str(),
        &InstallationState::info.setupBluetooth
    );

    ImGui::PopStyleVar(3);
    ImGui::EndChild();

#ifndef PASS_INSTALLER_CHECKS
    if (InstallationState::info.installSteam && !(
        InstallationState::info.vulkanAmd || 
        InstallationState::info.vulkanIntel || 
        InstallationState::info.vulkanNvidia)) 
    {
        Components::NavigationEx::disableNext = true;
    }
#endif

    ImGui::PopStyleVar();
    ImGui::End();
}