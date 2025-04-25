#include "utils.hpp"
#include "execute.hpp"
#include <sstream>


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