#include "pagecounter.hpp"

#include <algorithm>

#include "imgui.h"
#include "windowstate.hpp"

constexpr float padding = 15.0f;

void Components::PageCounter(int page, int total) {
    ImGui::Begin("#PageCounter", NULL, 
        ImGuiWindowFlags_NoTitleBar |
        ImGuiWindowFlags_NoDecoration |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoResize |
        ImGuiWindowFlags_NoNav
    );

    // Init for animation
    if (circleRadius.size() != total)
        circleRadius.resize(total, 2.0f);

    if (!initDone) {
        circleRadius[page] = 5.0f;
        initDone = true;
    }

    if (previousPage != page) {
        PageCounterEx::queueAnimation(previousPage, page);
        previousPage = page;
    }
    
    const auto framePadding = ImGui::GetStyle().FramePadding.x;

    ImGui::SetWindowSize({
        padding * total + framePadding, 50
    }, ImGuiCond_Always);

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowPos(
        {
            (globalWindowSize.x - padding * total + framePadding) / 2.0f,
            globalWindowSize.y - 50.0f
        }, 
        ImGuiCond_Always
    );

    ImDrawList* draw_list = ImGui::GetWindowDrawList();
    ImVec2 pos = ImGui::GetCursorScreenPos();

    for (int i = 0; i < total; i++) {
        ImGui::PushID(i);
        if (i == page) {
            draw_list->AddCircleFilled(pos, circleRadius[i], IM_COL32(255, 255, 255, 255));
        } else {
            draw_list->AddCircleFilled(pos, circleRadius[i], IM_COL32(150, 150, 150, 255));
        }
        pos.x += padding;
        ImGui::PopID();
    }

    ImGui::End();

}

void Components::PageCounterEx::queueAnimation(int previousPage, int currentPage) {
    auto previousIter = std::ranges::find_if(animationQueue.begin(), animationQueue.end(), [previousPage](auto& item) {
        return item.pageNum == previousPage;
    });
    if (previousIter != animationQueue.end()) {
        animationQueue.erase(previousIter);
    }
    auto currentIter = std::ranges::find_if(animationQueue.begin(), animationQueue.end(), [currentPage](auto& item) {
        return item.pageNum == currentPage;
    });
    if (currentIter != animationQueue.end()) {
        animationQueue.erase(currentIter);
    }
    animationQueue.emplace_back(previousPage, false);
    animationQueue.emplace_back(currentPage, true);
}

void Components::PageCounterEx::doAnimationStep() {
    const auto dt = ImGui::GetIO().DeltaTime;

    for (auto it = animationQueue.begin(); it != animationQueue.end();) {
        if (it->increase) {
            circleRadius[it->pageNum] += dt * 10;
            if (circleRadius[it->pageNum] > 5.0f) {
                circleRadius[it->pageNum] = 5.0f;
                it = animationQueue.erase(it);
            } else ++it;
        } else {
            circleRadius[it->pageNum] -= dt * 10;
            if (circleRadius[it->pageNum] < 2.0f) {
                circleRadius[it->pageNum] = 2.0f;
                it = animationQueue.erase(it);
            } else ++it;
        }
    }
}