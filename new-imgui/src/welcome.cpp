#include "welcome.hpp"
#include "centeredtext.hpp"
#include "imgui.h"
#include "styleshit.hpp"
#include "titletext.hpp"
#include "windowstate.hpp"
#include "languages.hpp"
#include "format"

void Welcome::render() {
    ImGui::Begin("#Welcome", NULL, 
        ImGuiWindowFlags_NoTitleBar |
        ImGuiWindowFlags_NoDecoration |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoResize |
        ImGuiWindowFlags_NoNav
    );

    ImGui::SetWindowSize({
        400.0, 300.0
    }, ImGuiCond_Always);

    auto welcomeWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowPos(
        {
            welcomeWindowSize.x / 2.0f - 200.0f,
            welcomeWindowSize.y / 2.0f - 150.0f
        }, 
        ImGuiCond_Always
    );

    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    Components::TitleText(Languages::getLanguageString("welcome").c_str());

    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 40.0});
    Components::CenteredText(Languages::getLanguageString("welcome_subtitle").c_str(), true);

    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});

    for (auto language : Languages::langsMap) {

        auto currentLanguage = language.first == Languages::getCurrentLanguage();

        if (currentLanguage) {
            ImGui::PushFont(StyleShit::g_boldFont);
        }

        if (ImGui::Button(language.second["lang_name"].c_str(), {-1, 0})) {

            Languages::changeLanguage(language.first);
        }

        if (currentLanguage) {
            ImGui::PopFont();
        }
    }

    ImGui::PopStyleVar(3);

    ImGui::End();
}