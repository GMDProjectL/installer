#pragma once

#include <map>
#include <string>
#include <vector>

namespace Backend::Utils {
    std::map<std::string, std::vector<std::string>> getTimezones();
    bool loadTexture(const char* path, unsigned int* outTextureID, int* outWidth, int* outHeight);
}