#pragma once

#define INSTANCE_FUNC(TYPE) \
    static TYPE* getInstance() { \
        static TYPE instance; \
        return &instance; \
    }

class BasePage {
public:
    float flyOffset = 60;
    float opacity = 0.0f;

    virtual ~BasePage() = default;
    virtual void render() = 0;
};