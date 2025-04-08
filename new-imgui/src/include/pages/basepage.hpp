#pragma once

class BasePage {
public:
    float transitionX = 60;
    float opacity = 0.0f;

    virtual ~BasePage() = default;
    virtual void render() = 0;
};