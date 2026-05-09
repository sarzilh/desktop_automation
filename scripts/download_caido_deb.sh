#!/usr/bin/env bash

touch /tmp/file_$1
touch /tmp/file_$2
touch /tmp/file_$3

download_path=$1

version_name=$(curl -s https://api.github.com/repos/caido/caido/releases/latest | jq -r '.tag_name')
caido_url=$(echo https://caido.download/releases/${version_name}/caido-desktop-${version_name}-linux-x86_64.deb)
wget -O $download_path/caido.deb $caido_url
