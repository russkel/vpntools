# vpntools
Simple scripts to assist PIA VPN usage

## update_pia.py
Downloads the OpenVPN configuration files from PIA and extracts the hostnames and ports. It then creates configuration files based on a provided template (derived from the TCP tough PIA configuration) incorporating an auth file and [systemd-resolved support](https://github.com/jonathanio/update-systemd-resolved) (using the [AUR](https://aur.archlinux.org/packages/openvpn-update-systemd-resolved/) package).

You should put your credentials in `pia-auth` in the OpenVPN client configuration folder, which should be suitably restricted.

To install and setup:
```sh
  pacman -S openvpn
  pacaur -S openvpn-update-systemd-resolved
  systemctl enable systemd-resolved.service
  systemctl start systemd-resolved.service
  python3 update_pia.py --install
  sudo echo $'YOUR_USERNAME\nYOUR_PASSWORD' > /etc/openvpn/client/pia-auth
  sudo chmod 600 /etc/openvpn/client/pia-auth
```

Done, now connect to the VPN:
```sh
  sudo systemctl start openvpn-client@PIA-Brazil
```
