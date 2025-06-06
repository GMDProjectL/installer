#include "globalview.hpp"
#include "basepage.hpp"
#include "imgui.h"
#include "installationstate.hpp"
#include "navigation.hpp"
#include "pagecounter.hpp"
#include "bgglow.hpp"
#include "smoothfactor.hpp"
#include <algorithm>

constexpr int opacityTransitionScale = 8;
constexpr int moveTransitionScale = 350;

void GlobalView::render() {
    Components::BGGlow();

    auto dt = ImGui::GetIO().DeltaTime;

    if (nextPage) {
        currentPage->opacity -= dt * opacityTransitionScale;
        currentPage->flyOffset -= dt * moveTransitionScale;
        nextPage->opacity += dt * opacityTransitionScale;
        nextPage->flyOffset -= dt * moveTransitionScale;

        currentPage->opacity = std::clamp(currentPage->opacity, 0.f, 1.f);
        currentPage->flyOffset = std::clamp(currentPage->flyOffset, -60.f, 0.f);

        nextPage->opacity = std::clamp(nextPage->opacity, 0.f, 1.f);
        nextPage->flyOffset = std::clamp(nextPage->flyOffset, 0.f, 60.f);

        if (nextPage->flyOffset <= 0 && nextPage->opacity >= 1 && currentPage->opacity <= 0 && currentPage->flyOffset <= -60) {
            currentPage->opacity = 0.0f;
            currentPage->flyOffset = 60;
            currentPage = nextPage;
            nextPage = nullptr;
        }
    }

    Components::Navigation();
    Components::PageCounterEx::updateAnimation();
    Components::PageCounter(InstallationState::page, InstallationState::maxPages);
    SmoothFactor::Cleanup();

    if (currentPage) {
        currentPage->render();
    }

    if (nextPage) {
        nextPage->render();
    }
}

void GlobalView::changePage(BasePage* page) {
    if(nextPage) {
        nextPage->opacity = 0.0f;
        nextPage->flyOffset = 60.f;
        nextPage = nullptr;
    }
    if (currentPage) {
        currentPage->opacity = 0.0f;
        currentPage->flyOffset = 60.0f;
    }
    page->flyOffset = 0;
    page->opacity = 1.0f;
    currentPage = page;
}

void GlobalView::changePageWithTransition(BasePage* page) {
    if (currentPage != page) {
        if(nextPage && nextPage != page) {
            page->opacity = nextPage->opacity;
            page->flyOffset = nextPage->flyOffset;
            
            nextPage->opacity = 0.0f;
            nextPage->flyOffset = 60.f;
        }
        nextPage = page;
    }
}