#!/bin/bash

# Description: This script sets my main host machine running Debian 13+ with all of the tools needed. 


# Add packages that needs to be installed
PKGS="wget curl git brave-browser ffmpeg yt-dlp openssh-server"

sudo apt update

echo "Installing packages..."
sudo apt install "$PKGS"

sudo apt upgrade -y

echo "Installing starship prompt"
curl -sS https://starship.rs/install.sh | sh

echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

#echo "Installing Antigravity CLI"
#curl -fsSL https://antigravity.google/cli/install.sh | bash


echo -e "\e[1;32mOmnia installation is complete.\e[0m"



