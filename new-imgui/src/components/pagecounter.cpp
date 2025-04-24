#include "pagecounter.hpp"

#include <algorithm>

#include "imgui.h"
#include "windowstate.hpp"

void Components::PageCounter(int page, int total) {
    ImGui::Begin("#PageCounter", NULL, 
        ImGuiWindowFlags_NoDecoration |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoNav |
        ImGuiWindowFlags_NoBackground |
        ImGuiWindowFlags_NoBringToFrontOnFocus
    );

    // Init for animation
    if (circleRadius.size() != total)
        circleRadius.resize(total, minSize);

    if (!initDone) {
        circleRadius[page] = maxSize;
        initDone = true;
    }

    if (previousPage != page) {
        PageCounterEx::queueAnimation(previousPage, page);
        previousPage = page;
    }
    
    const auto framePadding = ImGui::GetStyle().FramePadding.x;

    ImGui::SetWindowSize({
        spacing * total + framePadding, 35
    }, ImGuiCond_Always);

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowPos(
        {
            (globalWindowSize.x - ImGui::GetWindowWidth()) / 2.0f,
            globalWindowSize.y - 35
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
        pos.x += spacing;
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
            if (circleRadius[it->pageNum] > maxSize) {
                circleRadius[it->pageNum] = maxSize;
                it = animationQueue.erase(it);
            } else ++it;
        } else {
            circleRadius[it->pageNum] -= dt * 10;
            if (circleRadius[it->pageNum] < minSize) {
                circleRadius[it->pageNum] = minSize;
                it = animationQueue.erase(it);
            } else ++it;
        }
    }
}