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
        bool moveDown = true;
        float translationY = 1.5f;
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
            vec2 uv = fragCoord;

            float dist = 1.0 - length(uv);
            float intensity = pow(dist, 1.5);
            
            if (dist > 0.0)
                color = vec4(dist * 0.4);
            else discard;
        }
    )";
    void render(const ImDrawList* draw_list, const ImDrawCmd* cmd);
    GLuint createShaderProgram(const char* vertexShader, const char* fragShader);
}