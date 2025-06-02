#pragma once

#include <map>
#include <string>
#include <vector>

struct DiskObject {
    std::string location;
    std::string diskNaming;
    std::string size;
};

namespace Backend::Utils {
    std::map<std::string, std::vector<std::string>> getTimezones();
    std::vector<DiskObject> getDisks();
    bool loadTexture(const char* path, unsigned int* outTextureID, int* outWidth, int* outHeight);
}