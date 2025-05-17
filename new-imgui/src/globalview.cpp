#include "globalview.hpp"
#include "basepage.hpp"
#include "imgui.h"
#include "installationstate.hpp"
#include "navigation.hpp"
#include "pagecounter.hpp"
#include "bgglow.hpp"
#include "hoverbutton.hpp"
#include <algorithm>

constexpr int opacityTransitionScale = 8;
constexpr int moveTransitionScale = 350;

void GlobalView::render() {
    Components::BGGlow();

    auto dt = ImGui::GetIO().DeltaTime;

    if (nextPage) {
        currentPage->opacity -= dt * opacityTransitionScale;
        currentPage->transitionX -= dt * moveTransitionScale;
        nextPage->opacity += dt * opacityTransitionScale;
        nextPage->transitionX -= dt * moveTransitionScale;

        currentPage->opacity = std::clamp(currentPage->opacity, 0.f, 1.f);
        currentPage->transitionX = std::clamp(currentPage->transitionX, -60.f, 0.f);

        nextPage->opacity = std::clamp(nextPage->opacity, 0.f, 1.f);
        nextPage->transitionX = std::clamp(nextPage->transitionX, 0.f, 60.f);

        if (nextPage->transitionX <= 0 && nextPage->opacity >= 1 && currentPage->opacity <= 0 && currentPage->transitionX <= -60) {
            currentPage->opacity = 0.0f;
            currentPage->transitionX = 60;
            currentPage = nextPage;
            nextPage = nullptr;
        }
    }

    Components::Navigation();
    Components::PageCounterEx::doAnimationStep();
    Components::PageCounter(InstallationState::page, InstallationState::maxPages);
    Components::HoverButtonEx::CleanupHover();

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
        nextPage->transitionX = 60.f;
        nextPage = nullptr;
    }
    if (currentPage) {
        currentPage->opacity = 0.0f;
        currentPage->transitionX = 60.0f;
    }
    page->transitionX = 0;
    page->opacity = 1.0f;
    currentPage = page;
}

void GlobalView::changePageWithTransition(BasePage* page) {
    if (currentPage != page) {
        if(nextPage && nextPage != page) {
            page->opacity = nextPage->opacity;
            page->transitionX = nextPage->transitionX;
            
            nextPage->opacity = 0.0f;
            nextPage->transitionX = 60.f;
        }
        nextPage = page;
    }
}