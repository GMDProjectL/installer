#include "utils.hpp"
#include "execute.hpp"
#include <sstream>

#define STB_IMAGE_IMPLEMENTATION
#include <stb_image.h>
#include <GL/glew.h>


std::map<std::string, std::vector<std::string>> Backend::Utils::getTimezones() {
    size_t pos = 0;
    std::map<std::string, std::vector<std::string>> map;
    auto zones = execute("timedatectl list-timezones");

    std::istringstream iss(zones);

    for (std::string line; std::getline(iss, line);) {
        if(line.find('/') == line.npos) {
            map[line];
            continue;
        }

        pos = line.find("/");
        auto region = line.substr(0, pos);
        line.erase(0, pos + 1);

        map[region].push_back(line);
    }

    return map;
}

bool Backend::Utils::loadTexture(const char *path, unsigned int *outTextureID, int *outWidth, int *outHeight) {
    int imageWidth = 0, imageHeight = 0;

    unsigned char* imageData = stbi_load(path, &imageWidth, &imageHeight, nullptr, 4);
    if (imageData == NULL)
        return false;

    GLuint textureID;

    glGenTextures(1, &textureID);
    glBindTexture(GL_TEXTURE_2D, textureID);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    glPixelStorei(GL_UNPACK_ROW_LENGTH, 0);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imageWidth, imageHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData);
    stbi_image_free(imageData);

    *outTextureID = textureID;
    *outWidth = imageWidth;
    *outHeight = imageHeight;

    return true;

}