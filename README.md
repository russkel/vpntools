# vpntools
Simple scripts to assist VPN usage

## update_pia.py
Downloads the OpenVPN configuration files from PIA and extracts the hostnames and ports. It then creates configuration files based on a provided template (derived from the TCP tough PIA configuration) incorporating an auth file and openresolv support.

You should put your credentials in pia/pia-auth.conf in the OpenVPN client configuration folder, which should be suitably restricted.

To use:
```sh
  pacman -S openvpn openresolv
  mkdir confs
  python3 update_pia.py --install
  sudo systemctl start openvpn@Brazil
```
