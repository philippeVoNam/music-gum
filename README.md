# LAG WITH SSH, TRY THIS

https://gist.github.com/jcberthon/ea8cfe278998968ba7c5a95344bc8b55#networkmanager-wifi-power-saving

NetworkManager WiFi Power Saving
================================

NetworkManager supports WiFi powersaving but the function is rather undocumented.

From the source code: wifi.powersave can have the following value:

  - NM_SETTING_WIRELESS_POWERSAVE_DEFAULT (0): use the default value
  - NM_SETTING_WIRELESS_POWERSAVE_IGNORE  (1): don't touch existing setting
  - NM_SETTING_WIRELESS_POWERSAVE_DISABLE (2): disable powersave
  - NM_SETTING_WIRELESS_POWERSAVE_ENABLE  (3): enable powersave

Then I propose 2 files, only one of them needs to be put under `/etc/NetworkManager/conf.d/`.  
One is forcing to disable powersaving, while the other one enable it.

Once you have put the file in the right folder, simply restart NetworkManager:

    sudo systemctl restart NetworkManager

name of file : wifi-powersave-off.conf
# File to be place under /etc/NetworkManager/conf.d
# Values are 0 (use default), 1 (ignore/don't touch), 2 (disable) or 3 (enable).
[connection]
wifi.powersave = 2

# THE ONLY THING THAT YOU NEED TODO IS THAT YOU NEED TO RESTART NETWORK MANAGER ON BOOT EVERYTIME
