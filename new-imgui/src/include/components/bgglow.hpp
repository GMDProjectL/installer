#include "GL/glew.h"
#include "imgui.h"
#include <glm/glm.hpp>

namespace Components {
    void BGGlow();
}

namespace Components::BGGlowEx {
    namespace {
        inline float quadVertices[] = {
            -1, 1,
            -1, -1,
            1, 1,
            1, -1,
        };
        inline int quadIndices[] = {
            0, 1, 2,
            1, 2, 3
        };
        inline bool init = false;
        inline GLuint quadVAO, quadVBO, quadEBO;
        inline GLuint circleProgram;
        inline GLint modelLoc;
        inline constexpr float duration = 10.0f;
        inline constexpr float startPos = 1.5f;
        inline constexpr float endPos = 1.0f;
        inline float translationY = startPos;
        inline float currentTime = 0.0f;
        inline bool moveDown = true;
    }

    inline const char* circleVertexShader = R"(
        #version 330 core
        layout(location = 0) in vec2 position;
        uniform mat4 model;
        out vec2 fragCoord;

        void main() {
            gl_Position = model * vec4(position, 0.0, 1.0);
            fragCoord = position;
        }
    )";

    inline const char* circleFragShader = R"(
        #version 330 core
        in vec2 fragCoord;
        out vec4 color;

        void main() {
            float dist = 1.0 - length(fragCoord);

            if (dist > 0.0)
                color = vec4(dist * 0.4);
            else discard;
        }
    )";

    void render(const ImDrawList* draw_list, const ImDrawCmd* cmd);
    GLuint createShaderProgram(const char* vertexShader, const char* fragShader);
}