#pragma once
#include "installationinfo.hpp"

namespace InstallationState {

    inline int page = 0;
    inline InstallationInfo info;

    void goBack(int count = 1);
    void goNext(int count = 1);

}