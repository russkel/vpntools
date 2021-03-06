import os
import sys
import subprocess
import zipfile
import argparse
import json
from string import Template

parser = argparse.ArgumentParser(description='Obtain PIA VPNs and write config files.')
parser.add_argument('--refresh', action='store_true', default=False,
                    help='Write the config files ignoring checks for new file.')
parser.add_argument('--tough', action='store_true', default=False,
                    help='Use the "tough" configuration.')
parser.add_argument('--install', action='store_true', default=False,
                    help='Install the configuration files into the system.')
args = parser.parse_args()

if args.tough:
    zip_filename = "openvpn-strong-tcp.zip"
    template_filename = "template-tough.conf"
    hosts_json = "pia_hosts-tough-tcp.json"
    suffix = "-tough"
else:
    zip_filename = "openvpn.zip"
    template_filename = "template.conf"
    hosts_json = "pia_hosts-udp.json"
    suffix = ""


def mod_time():
    try:
        statinfo = os.stat(zip_filename)
        return statinfo.st_mtime
    except FileNotFoundError:
        return None


def extract_uri(ovpn):
    for line in ovpn:
        if line.startswith("remote "):
            return line.strip().split()[1:3]

    return (None, None)

if args.refresh:
    subprocess.run("rm -f {}".format(zip_filename), shell=True)

modtime = mod_time()
subprocess.run("curl -z {0} https://www.privateinternetaccess.com/openvpn/{0} -o {0}".format(zip_filename), shell=True)

if modtime == mod_time() and not args.refresh:
    # file is intact, do nothing
    print("No new files.")
    sys.exit()

subprocess.run("mkdir -p confs", shell=True)
subprocess.run("rm -f confs/*", shell=True)

servers = {}

with zipfile.ZipFile(zip_filename) as zf:
    for fn in zf.namelist():
        if fn.endswith(".ovpn"):
            name, ext = os.path.splitext(fn)

            with zf.open(fn, mode="r") as zff:
                ovpn = [b.decode() for b in zff.readlines()]

            hostname, port = extract_uri(ovpn)
            servers[name] = (hostname, port)

        elif fn.endswith('.crt') or fn.endswith('.pem'):
            zf.extract(fn, "confs/")

with open(hosts_json, "w") as out:
    json.dump(servers, out)

conf_file = Template("".join(open(template_filename, "r").readlines()))

for name, (hostname, port) in servers.items():
    new_fn = f"confs/PIA-{name.replace(' ', '_')}{suffix}.conf"
    print(f"Writing {new_fn}...")

    with open(new_fn, "w") as out:
        out.write(conf_file.substitute(hostname=hostname, port=port))

if args.install:
    print("Installing configuration files...")
    subprocess.run("sudo cp confs/* /etc/openvpn/client/", shell=True)
