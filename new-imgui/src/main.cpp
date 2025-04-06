#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include "windowstate.hpp"
#include <stdio.h>
#define GL_SILENCE_DEPRECATION
#include <GLFW/glfw3.h>

#include "styleshit.hpp"
#include "globalview.hpp"


static void glfw_error_callback(int error, const char* description)
{
    fprintf(stderr, "GLFW Error %d: %s\n", error, description);
}

// Main code
int main(int, char**)
{
    glfwSetErrorCallback(glfw_error_callback);
    if (!glfwInit())
        return 1;

    const char* glsl_version = "#version 130";
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);

    // Create window with graphics context
    WindowState::window = glfwCreateWindow(1280, 720, "Project GDL installer", nullptr, nullptr);
    
    if (WindowState::window == nullptr)
        return 1;

    glfwMakeContextCurrent(WindowState::window);
    glfwSwapInterval(0); // Enable vsync

    // Setup Dear ImGui context
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO(); (void)io;
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;

    ImGui::StyleColorsDark();

    ImGui_ImplGlfw_InitForOpenGL(WindowState::window, true);
    ImGui_ImplOpenGL3_Init(glsl_version);


    io.Fonts->AddFontDefault();
    ImFont* font = io.Fonts->AddFontFromFileTTF(
        "/usr/share/fonts/Adwaita/AdwaitaSans-Regular.ttf", 18.0f, nullptr, 
        io.Fonts->GetGlyphRangesCyrillic()
    );

    StyleShit::g_boldFont = io.Fonts->AddFontFromFileTTF(
        "./resources/fonts/inter-bold.ttf", 18.0f, nullptr, 
        io.Fonts->GetGlyphRangesCyrillic()
    );

    ImFontConfig titleFontConfig;

    StyleShit::g_titleFont = io.Fonts->AddFontFromFileTTF(
        "./resources/fonts/inter-bold.ttf", 42.0f, &titleFontConfig, 
        io.Fonts->GetGlyphRangesCyrillic()
    );

    IM_ASSERT(font != nullptr);
    IM_ASSERT(StyleShit::g_titleFont != nullptr);

    io.FontDefault = font;

    ImVec4 clear_color = ImVec4(0.1, 0.1, 0.1, 1.00f);

    StyleShit::setupStyles();

    while (!glfwWindowShouldClose(WindowState::window))
    {
        glfwPollEvents();

        if (glfwGetWindowAttrib(WindowState::window, GLFW_ICONIFIED) != 0)
        {
            ImGui_ImplGlfw_Sleep(10);
            continue;
        }

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        GlobalView::render();
        ImGui::ShowStyleEditor();
        
        ImGui::Render();
        int display_w, display_h;
        glfwGetFramebufferSize(WindowState::window, &display_w, &display_h);
        glViewport(0, 0, display_w, display_h);
        glClearColor(clear_color.x * clear_color.w, clear_color.y * clear_color.w, clear_color.z * clear_color.w, clear_color.w);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

        glfwSwapBuffers(WindowState::window);
    }

    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();

    glfwDestroyWindow(WindowState::window);
    glfwTerminate();

    return 0;
}
