#include "welcome.hpp"
#include "centeredtext.hpp"
#include "font_awesome.h"
#include "imgui.h"
#include "installationstate.hpp"
#include "styleshit.hpp"
#include "titletext.hpp"
#include "windowstate.hpp"
#include "languages.hpp"
#include "hoverbutton.hpp"
#include <format>

Welcome* Welcome::instance = nullptr;

void Welcome::render() {
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, opacity);
    ImGui::Begin("#Welcome", NULL, StyleShit::g_defaultWindowFlags);

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
    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});
    Components::TitleText(Languages::getLanguageString("welcome").c_str());

    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 40.0});
    Components::CenteredText(Languages::getLanguageString("welcome_subtitle").c_str(), true);

    ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, {-1, 20.0});

    ImVec2 langWindowSize = { 350.0, 400.0 };

    auto fontAwesome = StyleShit::g_fonts[StyleShit::Fonts::semiBoldFont];
    ImGui::PushFont(fontAwesome);
    
    auto langSubtitleText = std::format("{}  {}", ICON_FA_GLOBE, Languages::getLanguageString("lang_title"));
    auto offset = 30;

    ImGui::SetNextWindowPos({
        (globalWindowSize.x - langWindowSize.x) / 2 + transitionX,
        (globalWindowSize.y - langWindowSize.y) / 2 + ImGui::GetCursorPosY() - offset - ImGui::CalcTextSize(langSubtitleText.c_str()).y
    });

    ImGui::BeginChild("#Languages", langWindowSize, 0, StyleShit::g_defaultWindowFlags);
    
    Components::CenteredText(langSubtitleText.c_str());
    ImGui::PopFont();

    ImGui::SetCursorPosY(ImGui::GetCursorPosY() + offset);

    for (auto language : Languages::langsMap) {

        auto currentLanguage = language.first == Languages::getCurrentLanguage();

        if (currentLanguage) {
            auto boldFont = StyleShit::g_fonts[StyleShit::Fonts::boldFont];
            ImGui::PushFont(boldFont);
        }

        if (Components::HoverButton(language.second["lang_name"].c_str(), {-1, 0})) {

            Languages::changeLanguage(language.first);
            InstallationState::info.language = language.first;
        }

        if (currentLanguage) {
            ImGui::PopFont();
        }
    }
    ImGui::EndChild();

    ImGui::PopStyleVar(4);

    ImGui::End();
}