from pyinfra.operations import apt, server, systemd, files
from pyinfra import host
from pyinfra.facts.server import Command
from random import randint 

# Create a temp file for storing things
TEMP_DIR = f"/tmp/tmp_{ hex(randint(int(10e19),int(10e20)))[2:] }"
files.directory(
    path = TEMP_DIR,
    present = True,
    user = "root",
    group = "root",
    mode = "0700"
)
# pyinfra got no handlers, so MUST MANUALLY mention at bottom to also delete this file

# Move to unstable
#release_name = host.get_fact(Command, command="lsb_release -a | grep '^Codename' | awk '{ print $2 }' | xargs") # actually its not even going to be used.. testing is packed in unstable release lol
files.template(
    src="templates/sources.list.j2",
    dest="/etc/apt/sources.list",
    user="root",
    group="root",
    mode="644",
 #   jinja_env_kwargs={"release_name": release_name}
)

# Create My User
server.user(
        user = "rpq",
        present = True,
        home = "/home/rpq",
        shell = "/usr/bin/bash",
        groups = ["audio", "video", "sudo"],
        create_home=True,
        password = "$y$j9T$d28D120iXZFJZZYaFsINQ.$T6T8YvqtJVNAO6REapqbTrmIIdeR9NRL7KOzoCtJ9G5", # debian stores in yescrypt
)

# Install packages through apt
apt.packages(
    packages = [
        "sway",
        # utilities
        "sudo",
        "curl",
        "wget",
        "lynx",
        "jq",
        "dnsutils",
        "vim",
        "tor",
        "newsboat",
        "mupdf",
        "imagemagick",
        "mpv",
        "unzip",
        "7zip",
        "alacritty",
        "ufw",
        # audio
        "ffmpeg",
        "wireplumber",
        "pipewire",
        "pipewire-pulse",
        "pavucontrol",
        "alsa-utils",
        "qpwgraph",
        # needed
        "fonts-noto",
        "build-essential",
        # virt
        "qemu-system",
        "libvirt-daemon-system",
        ],
    present=True,
    latest=True,
    update=True,
    upgrade=True,
)

# Start Audio
systemd.service(
    service = "wireplumber",
    enabled = True,
    running = True,
    user_mode = True,
    user_name = "rpq",
)

# Install Brave
server.shell(
    name="install Brave from their shell code",
    commands=[
        f"curl -fsS -o {TEMP_DIR}/brave_install.sh https://dl.brave.com/install.sh",
        f"chmod +x {TEMP_DIR}/brave_install.sh",
        f"{TEMP_DIR}/brave_install.sh"
    ]
)

# Install DBeaver
dbeaver_url="https://dbeaver.io/files/dbeaver-ce-latest-linux-x86_64.deb"

files.download(
    name = "Download DBeaver DEB file",
    src = dbeaver_url,
    dest = f"{TEMP_DIR}/dbeaver.deb"
)

apt.deb(
    src = f"{TEMP_DIR}/dbeaver.deb",
    present = True
);

# Install Caido
server.script(
        name="Download Caido DEB package",
        src="scripts/download_caido_deb.sh",
        args=(TEMP_DIR,)
)

apt.deb(
    src = f"{TEMP_DIR}/caido.deb",
    present = True
)

# Install Docker
server.script(
        name="Install Docker",
        src="scripts/install_docker.sh"
)

systemd.service(
        service = "docker",
        enabled = True,
        running = True
)

server.user(
        user = "rpq",
        groups = ["docker"]
)

# Delete TEMP DIR
files.directory(
    path = TEMP_DIR,
    present = False,
)
