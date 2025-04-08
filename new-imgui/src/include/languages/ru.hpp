#pragma once
#include <string>
#include <map>


namespace Languages {
    inline std::map<std::string, std::string> g_russianStrings = {
        {"lang_name", "Русский"},
        {"welcome", "Добро пожаловать в установщик GDL!"},
        {"welcome_subtitle", "Лёгкий в использовании дистрибутив Linux."},
        {"back", "Назад"},
        {"next", "Вперёд"},
        {"introduce_yourself", "Представьтесь, пожалуйста"},
        {"username", "Имя пользователя"},
        {"hostname", "Имя компьютера"},
        {"password", "Пароль"},
        {"password2", "Повторите пароль"},
        {"timezone", "Часовой пояс"},
        {"timezone_region", "Регион"},
        {"timezone_info", "Информация о часовом поясе"},
        {"selected_drive", "Выбранный диск"},
        {"boot_partition", "Загрузочный раздел"},
        {"root_partition", "Корневой раздел"},
        {"format_boot_partition", "Отформатировать загрузочный раздел"},
        {"enable_multilib_repo", "Включить репозиторий multilib"},
        {"install_steam", "Установить Steam"},
        {"install_wine", "Установить Wine"},
        {"install_winetricks", "Установить Winetricks"},
        {"vulkan_nvidia", "Драйверы Vulkan для Nvidia"},
        {"vulkan_amd", "Драйверы Vulkan для AMD"},
        {"vulkan_intel", "Драйверы Vulkan для Intel"},
        {"install_gnome_disks", "Установить Gnome Disks"},
        {"install_intel_media", "Установить драйверы Intel Media"},
        {"setup_bluetooth", "Настроить Bluetooth"}
    };
}