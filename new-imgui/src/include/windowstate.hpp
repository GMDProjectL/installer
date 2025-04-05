#pragma once
#include "GLFW/glfw3.h"
#include "imgui.h"

namespace WindowState {
    inline GLFWwindow* window;

    inline ImVec2 getWindowSize() {
        int width, height;
        glfwGetWindowSize(window, &width, &height);

        return ImVec2(width, height);
    }
}