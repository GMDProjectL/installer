#include "pagecounter.hpp"

#include <algorithm>

#include "imgui.h"
#include "windowstate.hpp"


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
        auto previousIter = std::ranges::find_if(jobIndexes.begin(), jobIndexes.end(), [](auto& item) {
            return item.pageNum == previousPage;
        });
        if (previousIter != jobIndexes.end()) {
            jobIndexes.erase(previousIter);
        }
        auto currentIter = std::ranges::find_if(jobIndexes.begin(), jobIndexes.end(), [page](auto& item) {
            return item.pageNum == page;
        });
        if (currentIter != jobIndexes.end()) {
            jobIndexes.erase(currentIter);
        }
        jobIndexes.emplace_back(previousPage, false);
        jobIndexes.emplace_back(page, true);
        previousPage = page;
    }

    ImGui::SetWindowSize({
        100, 50
    }, ImGuiCond_Always);

    auto globalWindowSize = WindowState::getWindowSize();

    ImGui::SetWindowPos(
        {
            globalWindowSize.x / 2.0f - 50.0f,
            globalWindowSize.y - 50.0f
        }, 
        ImGuiCond_Always
    );

    ImDrawList* draw_list = ImGui::GetWindowDrawList();

    ImVec2 pos = ImGui::GetCursorScreenPos();

    const auto deltaTime = ImGui::GetIO().DeltaTime;

    for (auto it = jobIndexes.begin(); it != jobIndexes.end();) {
        if (it->increase) {
            circleRadius[it->pageNum] += deltaTime * 10;
            if (circleRadius[it->pageNum] > 5.0f) {
                circleRadius[it->pageNum] = 5.0f;
                it = jobIndexes.erase(it);
            } else ++it;
        } else {
            circleRadius[it->pageNum] -= deltaTime * 10;
            if (circleRadius[it->pageNum] < 2.0f) {
                circleRadius[it->pageNum] = 2.0f;
                it = jobIndexes.erase(it);
            } else ++it;
        }
    }

    for (int i = 0; i < total; i++) {
        ImGui::PushID(i);
        if (i == page) {
            draw_list->AddCircleFilled(pos, circleRadius[i], IM_COL32(255, 255, 255, 255));
        } else {
            draw_list->AddCircleFilled(pos, circleRadius[i], IM_COL32(150, 150, 150, 255));
        }
        pos.x += 15.0f;
        ImGui::PopID();
    }

    ImGui::End();

}