#include "utils.hpp"
#include "execute.hpp"
#include <format>
#include <sstream>

#define STB_IMAGE_IMPLEMENTATION
#include <stb_image.h>
#include <GL/glew.h>
#include <document.h>


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

std::vector<DiskObject> Backend::Utils::getDisks() {
    rapidjson::Document document;
    document.Parse(execute("lsblk -AJ").c_str());
    std::vector<DiskObject> ret;

    if (!document.HasMember("blockdevices") || !document["blockdevices"].IsArray())
        return ret;
    
    auto array = document["blockdevices"].GetArray();
    for (auto it = array.begin(); it != array.end(); ++it) {
        if (!it->HasMember("type") || std::strcmp(it->GetObject()["type"].GetString(), "disk") != 0) 
            continue;
        
        DiskObject obj;
        obj.location = it->GetObject()["name"].GetString();

        auto naming = execute(std::format("cat /sys/block/{}/device/model", obj.location).c_str());
        naming.erase(naming.size() - 1, naming.size()); // Erasing the '\n' at the end

        obj.diskNaming = naming;
        obj.size = it->GetObject()["size"].GetString();

        ret.push_back(obj);
    }

    return ret;
}