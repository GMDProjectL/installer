cmake_minimum_required(VERSION 3.10.0)
project(gdl-imgui-installer VERSION 0.1.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address -g -O0")

find_package(OpenGL REQUIRED)
find_package(glfw3 CONFIG REQUIRED)
find_package(GLEW REQUIRED)
find_package(glm CONFIG REQUIRED)

file(GLOB_RECURSE PROJ_SRC src/*.c*)
file(GLOB_RECURSE IMGUI_SRC thirdparty/imgui/*.c*)

add_executable(${PROJECT_NAME} ${PROJ_SRC} ${IMGUI_SRC})

target_include_directories(
    ${PROJECT_NAME} PUBLIC 
    thirdparty/imgui
    thirdparty/imgui/backends
    thirdparty/fontawesome
    /usr/include/stb/
    /usr/include/rapidjson/
    src/include
    src/include/components
    src/include/languages
    src/include/backend
    src/include/pages
)

if(PASS_CHECKS)
    add_compile_definitions(PASS_INSTALLER_CHECKS)
endif()

file(COPY ./resources DESTINATION ${CMAKE_BINARY_DIR})

target_link_libraries(${PROJECT_NAME} PUBLIC
    OpenGL::OpenGL
    glfw
    GLEW
    glm::glm
)