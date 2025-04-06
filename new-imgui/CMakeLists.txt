cmake_minimum_required(VERSION 3.10.0)
project(gdl-imgui-installer VERSION 0.1.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenGL REQUIRED)
find_package(glfw3 CONFIG REQUIRED)

file(GLOB_RECURSE PROJ_SRC src/*.c*)
file(GLOB_RECURSE IMGUI_SRC thirdparty/imgui/*.c*)

add_executable(${PROJECT_NAME} ${PROJ_SRC} ${IMGUI_SRC}
        src/include/components/hoverbutton.h
        src/components/hoverbutton.cpp)

target_include_directories(
    ${PROJECT_NAME} PUBLIC 
    thirdparty/imgui
    thirdparty/imgui/backends
    src/include
    src/include/components
    src/include/languages
)

file(COPY ./resources DESTINATION ${CMAKE_BINARY_DIR})

target_link_libraries(${PROJECT_NAME} PUBLIC
    OpenGL::OpenGL
    glfw
)