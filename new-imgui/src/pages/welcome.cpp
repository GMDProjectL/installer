#include "welcome.hpp"
#include "centeredtext.hpp"
#include "imgui.h"
#include "styleshit.hpp"
#include "titletext.hpp"
#include "windowstate.hpp"
#include "languages.hpp"
#include "hoverbutton.hpp"

void Welcome::render() {
    ImGui::Begin("#Welcome", NULL, 
        ImGuiWindowFlags_NoTitleBar |
        ImGuiWindowFlags_NoDecoration |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoResize |
        ImGuiWindowFlags_NoNav
    );

    ImVec2 welcomeWindowSize = { 700.0, 400.0 };

    ImGui::SetWindowSize(welcomeWindowSize, ImGuiCond_Always);

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowPos(
        {
            globalWindowSize.x / 2.0f - welcomeWindowSize.x / 2,
            globalWindowSize.y / 2.0f - welcomeWindowSize.y / 2
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

        if (Components::HoverButton(language.second["lang_name"], {-1, 0})) {

            Languages::changeLanguage(language.first);
        }

        if (currentLanguage) {
            ImGui::PopFont();
        }
    }

    ImGui::PopStyleVar(3);

    ImGui::End();
}