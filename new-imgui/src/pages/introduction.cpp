#include "introduction.hpp"

#include "imgui.h"
#include "installationstate.hpp"
#include "styleshit.hpp"
#include "titletext.hpp"
#include "windowstate.hpp"
#include "languages.hpp"
#include "font_awesome.h"
#include <format>
#include "navigation.hpp"
#include "inputpreviewtext.hpp"

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

    auto& info = InstallationState::info;

    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s  %s", ICON_FA_USER, Languages::getLanguageString("username").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###username", info.username, 64);
    Components::InputPreviewText("relative", info.username);


    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s  %s", ICON_FA_DESKTOP, Languages::getLanguageString("hostname").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###hostname", info.hostname, 64);
    Components::InputPreviewText("relatives-pc", info.hostname);


    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s  %s", ICON_FA_LOCK, Languages::getLanguageString("password").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###password", info.password, 64, ImGuiInputTextFlags_Password);
    Components::InputPreviewText("**************", info.password);


    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s  %s", ICON_FA_LOCK, Languages::getLanguageString("password2").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###password2", info.password2, 64, ImGuiInputTextFlags_Password);
    Components::InputPreviewText("**************", info.password2);


    if(strlen(info.username) == 0||
        strlen(info.hostname) == 0 ||
        strlen(info.password) == 0 ||
        strlen(info.password2) == 0 ||
        strcmp(info.password, info.password2) != 0)
    {
        Components::NavigationEx::disableNext = true;
    }

    ImGui::PopStyleVar(10);
    ImGui::EndChild();

    ImGui::End();
}