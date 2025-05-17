#include "depage.hpp"

#include "imgui.h"
#include "windowstate.hpp"
#include "styleshit.hpp"
#include "titletext.hpp"
#include "font_awesome.h"
#include <format>
#include "languages.hpp"

DEPage* DEPage::instance = nullptr;

void DEPage::render() {
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, opacity);
    ImGui::Begin("#DEPage", NULL, StyleShit::g_defaultWindowFlags);

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowSize(globalWindowSize);

    ImGui::SetWindowPos({
            transitionX,
            0
        }, ImGuiCond_Always
    );

    ImGui::SetCursorPosY(40);
    Components::TitleText(std::format("{}  {}",
        ICON_FA_DESKTOP,
        Languages::getLanguageString("desktop_environment")
    ).c_str());

    

    ImGui::PopStyleVar();
    ImGui::End();
}