#include "introduction.hpp"

#include "imgui.h"
#include "installationstate.hpp"
#include "titletext.hpp"
#include "windowstate.hpp"
#include "languages.hpp"

Introduction* Introduction::instance = nullptr;

void Introduction::render() {
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, opacity);
    ImGui::Begin("#Introduction", NULL, 
        ImGuiWindowFlags_NoTitleBar |
        ImGuiWindowFlags_NoDecoration |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoResize |
        ImGuiWindowFlags_NoNav
    );

    ImVec2 welcomeWindowSize = { 600.0, 500.0 };

    ImGui::SetWindowSize(welcomeWindowSize, ImGuiCond_Always);

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowPos(
        {
            globalWindowSize.x / 2.0f - welcomeWindowSize.x / 2 + transitionX,
            globalWindowSize.y / 2.4f - welcomeWindowSize.y / 2
        }, 
        ImGuiCond_Always
    );

    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 40.0});
    Components::TitleText(Languages::getLanguageString("introduce_yourself").c_str());


    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s", Languages::getLanguageString("username").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###username", InstallationState::info.username.data(), 64);


    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s", Languages::getLanguageString("hostname").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###hostname", InstallationState::info.hostname.data(), 64);


    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s", Languages::getLanguageString("password").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###password", InstallationState::info.password.data(), 64, ImGuiInputTextFlags_Password);


    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 10.0});
    ImGui::TextDisabled("%s", Languages::getLanguageString("password2").c_str());
    
    ImGui::SetNextItemWidth(-1);
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    ImGui::InputText("###password2", InstallationState::info.password2.data(), 64, ImGuiInputTextFlags_Password);



    ImGui::PopStyleVar(10);

    ImGui::End();
}