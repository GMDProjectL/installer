#include "GL/glew.h"
#include "imgui.h"

namespace BGGlow {
    inline const char* simpleVertexShader = R"(
#version 330 core
layout(location = 0) in vec2 position;
out vec2 fragCoord;

void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    fragCoord = position;
}
)";

    inline const char* circleVertexShader = R"(
#version 330 core
layout(location = 0) in vec2 position;
out vec2 fragCoord;

void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    fragCoord = position * 0.5 + 0.5;  // Transform to [0,1] range
}
)";

    inline const char* circleFragShader = R"(
#version 330 core
in vec2 fragCoord;
out vec4 color;

void main() {
    float dist = length(fragCoord - vec2(0.5, 0.5)); // Distance from the center
    if (dist < 0.25) {
        color = vec4(1.0, 0.0, 0.0, 1.0); // Red circle
    } else {
        discard;  // Outside the circle, discard fragment
    }
}
)";

    inline const char* gaussianHorizontalFragShader = R"(
#version 330 core
in vec2 fragCoord;
out vec4 color;

uniform sampler2D inputTexture;
uniform float texWidth;

void main() {
    vec2 texOffset = vec2(1.0 / texWidth, 0.0);  // Texture offset for horizontal sampling
    vec4 sum = vec4(0.0);
    for (int i = -4; i <= 4; ++i) { // Gaussian blur kernel size, can be adjusted
        sum += texture(inputTexture, fragCoord.xy + texOffset * i) * exp(-float(i * i) / 16.0); // Gaussian weight
    }
    color = sum / 9.0; // Normalize by kernel size
}    
)";

    inline const char* gaussianVerticalFragShader = R"(
#version 330 core
in vec2 fragCoord;
out vec4 color;

uniform sampler2D inputTexture;
uniform float texHeight;

void main() {
    vec2 texOffset = vec2(0.0, 1.0 / texHeight);  // Texture offset for vertical sampling
    vec4 sum = vec4(0.0);
    for (int i = -4; i <= 4; ++i) { // Gaussian blur kernel size
        sum += texture(inputTexture, fragCoord.xy + texOffset * i) * exp(-float(i * i) / 16.0); // Gaussian weight
    }
    color = sum / 9.0; // Normalize by kernel size
}
)";
    inline float quadVertices[] = {
        -1.0f,  1.0f,      0.0f, 1.0f,
        -1.0f, -1.0f,      0.0f, 0.0f,
         1.0f, -1.0f,      1.0f, 0.0f,
         1.0f,  1.0f,      1.0f, 1.0f
    };
    inline bool init = false;
    inline GLuint fbo, tex, horizontalBlurTex, verticalBlurTex, quadVAO, quadVBO;
    inline GLuint circleShader, horizontalBlurShader, verticalBlurShader;
    void render(ImDrawList* draw_list, const ImDrawCmd* cmd);
    GLuint createShaderProgram(const char* vertexShader, const char* fragShader);
}