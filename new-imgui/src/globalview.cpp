#include "globalview.hpp"
#include "basepage.hpp"
#include "imgui.h"
#include "installationstate.hpp"
#include "navigation.hpp"
#include "pagecounter.hpp"


void GlobalView::render() {
    auto deltaTime = ImGui::GetIO().DeltaTime;

    if (nextPage) {
        nextPage->opacity += deltaTime * 8;
        currentPage->opacity -= deltaTime * 8;
        nextPage->transitionX -= deltaTime * 350;
        currentPage->transitionX -= deltaTime * 350;

        if (nextPage->transitionX < 0.0f) {
            nextPage->transitionX = 0.0f;
        }
        if (nextPage->opacity > 1.0f) {
            nextPage->opacity = 1.0f;
        }
        if (currentPage->transitionX < -60.0f) {
            currentPage->transitionX = -60.0f;
        }
        if (currentPage->opacity < 0.0f) {
            currentPage->opacity = 0.0f;
        }

        if (nextPage->transitionX <= 0 && nextPage->opacity >= 1 && currentPage->opacity <= 0 && currentPage->transitionX <= -60) {
            currentPage->opacity = 0.0f;
            currentPage->transitionX = 60;
            currentPage = nextPage;
            nextPage = nullptr;
        }
    }

    if (currentPage) {
        currentPage->render();
    }

    if (nextPage) {
        nextPage->render();
    }

    Components::PageCounter(InstallationState::page, 6);

    Components::Navigation();
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
            nextPage->opacity = 0.0f;
            nextPage->transitionX = 60.f;
        }
        nextPage = page;
    }
}