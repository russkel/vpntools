import os
import sys
import subprocess
import zipfile


def mod_time():
    statinfo = os.stat("openvpn.zip")
    return statinfo.st_mtime


def fix_conf(ovpn):
    for i, line in enumerate(ovpn):
        if not line.strip():
            ovpn[i] = ''
        if line.startswith("auth-user-pass"):
            ovpn[i] = "auth-user-pass pia/pia-auth.conf\n"

    ovpn += ["script-security 2\n", "up /etc/openvpn/update-resolv-conf.sh\n", "down /etc/openvpn/update-resolv-conf.sh\n"]
    return ovpn

modtime = mod_time()
subprocess.run("curl -z openvpn.zip https://www.privateinternetaccess.com/openvpn/openvpn.zip", shell=True)

if modtime == mod_time():
    # file is intact, do nothing
    print("No new files.")
    sys.exit()

subprocess.run("rm confs/*", shell=True)

with zipfile.ZipFile("openvpn.zip") as zf:
    for fn in zf.namelist():
        if fn.endswith(".ovpn"):
            new_fn = "confs/{}".format(fn.replace(' ', '_').replace('.ovpn', '.conf'))
            print("Writing {}".format(new_fn))

            with zf.open(fn, mode="r") as zff, open(new_fn, "w") as out:
                ovpn = [b.decode() for b in zff.readlines()]
                out.writelines(fix_conf(ovpn))
        elif fn.endswith('.crt') or fn.endswith('.pem'):
            zf.extract(fn, "confs/")

print("Installing configuration files")
subprocess.run("sudo cp confs/* /etc/openvpn/", shell=True)