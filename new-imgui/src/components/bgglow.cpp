#include "bgglow.hpp"

#include <iostream>
#include <glm/gtc/matrix_transform.hpp>
#include <windowstate.hpp>

void Components::BGGlowEx::render(const ImDrawList* draw_list, const ImDrawCmd* cmd) {
    //glPushAttrib(GL_ALL_ATTRIB_BITS);
    
    if (!init) {
        circleProgram = createShaderProgram(circleVertexShader, circleFragShader);

        modelLoc = glGetUniformLocation(circleProgram, "model");

        glCreateVertexArrays(1, &quadVAO);
        glCreateBuffers(1, &quadVBO);
        glCreateBuffers(1, &quadEBO);

        glBindVertexArray(quadVAO);

        glBindBuffer(GL_ARRAY_BUFFER, quadVBO);
        glBufferData(GL_ARRAY_BUFFER, sizeof(quadVertices), quadVertices, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, quadEBO);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(quadIndices), quadIndices, GL_STATIC_DRAW);

        glVertexAttribPointer(
            0,
            2,
            GL_FLOAT,
            GL_FALSE,
            2 * sizeof(float),                  
            (void*)0
        );

        glEnableVertexAttribArray(0);

        glBindBuffer(GL_ARRAY_BUFFER, 0);
        glBindVertexArray(0);
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);

        init = true;
    }

    glm::mat4 model = glm::mat4(1.0f);
    model = glm::translate(model, glm::vec3(0, translationY, 0));
    model = glm::scale(model, glm::vec3(2, 2, 1));

    auto winSize = WindowState::getWindowSize();

    glUseProgram(circleProgram);
    
    glUniformMatrix4fv(modelLoc, 1, GL_FALSE, &model[0][0]);

    glBindVertexArray(quadVAO);

    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

    //glPopAttrib();
}

void checkCompileErrors(GLuint shader, bool frag = false, bool program = false) {
    GLint success;
    GLchar infoLog[1024];
    
    if (!program) {
        glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
        if (!success) {
            glGetShaderInfoLog(shader, 1024, nullptr, infoLog);
            std::cerr << "ERROR::SHADER_COMPILATION_ERROR: " << (frag ? "FRAGMENT_TYPE: " : "VERTEX_TYPE: ") << "\n" << infoLog << std::endl;
        }
    } else {
        glGetProgramiv(shader, GL_LINK_STATUS, &success);
        if (!success) {
            glGetProgramInfoLog(shader, 1024, nullptr, infoLog);
            std::cerr << "ERROR::PROGRAM_LINKING_ERROR: " << "\n" << infoLog << std::endl;
        }
    }
}

GLuint Components::BGGlowEx::createShaderProgram(const char *vertexShaderSource, const char *fragmentShaderSource) {
    GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, nullptr);
    glCompileShader(vertexShader);
    checkCompileErrors(vertexShader);

    // Compile fragment shader
    GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSource, nullptr);
    glCompileShader(fragmentShader);
    checkCompileErrors(fragmentShader, true);

    // Link shaders into a shader program
    GLuint shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);
    checkCompileErrors(shaderProgram, true, true);

    // Clean up shaders as they're no longer needed after linking
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    return shaderProgram;
}

void Components::BGGlow() {
    auto dt = ImGui::GetIO().DeltaTime;
    auto drawList = ImGui::GetBackgroundDrawList();

    if (BGGlowEx::translationY >= 1.5) {
        BGGlowEx::moveDown = true;
    } else if (BGGlowEx::translationY <= 1) {
        BGGlowEx::moveDown = false;
    }
    
    if (BGGlowEx::moveDown) {
        BGGlowEx::translationY -= 0.15 * dt;
    } else {
        BGGlowEx::translationY += 0.15 * dt;
    }

    drawList->AddCallback(&BGGlowEx::render, nullptr);
    drawList->AddCallback(ImDrawCallback_ResetRenderState, nullptr);
}

