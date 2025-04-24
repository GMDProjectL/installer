#include "introduction.hpp"

#include "imgui.h"
#include "installationstate.hpp"
#include "styleshit.hpp"
#include "titletext.hpp"
#include "windowstate.hpp"
#include "languages.hpp"
#include "font_awesome.h"
#include <format>

Introduction* Introduction::instance = nullptr;

void Introduction::render() {
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, opacity);
    ImGui::Begin("#Introduction", NULL, StyleShit::g_defaultWindowFlags);

    ImVec2 inputWindowSize = { 600.0, 400.0 };

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowSize(globalWindowSize, ImGuiCond_Always);

    ImGui::SetWindowPos(
        {
            transitionX,
            0
        }, 
        ImGuiCond_Always
    );

    ImGui::SetCursorPosY(40);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 40.0});
    Components::TitleText(std::format("{}  {}",
        ICON_FA_USER,
        Languages::getLanguageString("introduce_yourself")
    ).c_str());

    ImGui::SetNextWindowPos({
        (globalWindowSize.x - inputWindowSize.x) / 2 + transitionX,
        (globalWindowSize.y - inputWindowSize.y) / 2
    });

    ImGui::BeginChild("#InputFields", inputWindowSize, 0, StyleShit::g_defaultWindowFlags);

    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s  %s", ICON_FA_USER, Languages::getLanguageString("username").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###username", InstallationState::info.username.data(), 64);


    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s  %s", ICON_FA_DESKTOP, Languages::getLanguageString("hostname").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###hostname", InstallationState::info.hostname.data(), 64);


    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s  %s", ICON_FA_LOCK, Languages::getLanguageString("password").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###password", InstallationState::info.password.data(), 64, ImGuiInputTextFlags_Password);


    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s  %s", ICON_FA_LOCK, Languages::getLanguageString("password2").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###password2", InstallationState::info.password2.data(), 64, ImGuiInputTextFlags_Password);

    ImGui::PopStyleVar(10);
    ImGui::EndChild();

    ImGui::End();
}