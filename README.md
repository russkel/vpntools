# vpntools
Simple scripts to assist VPN usage

## update_pia.py
Downloads the OpenVPN configuration files from PIA and modifies them to suit.

To use:
```sh
  pacman -S openvpn openresolv
  mkdir confs
  python3 update_pia.py
  sudo systemctl start openvpn@Russia
```
