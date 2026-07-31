#!/bin/bash

# Description: This script sets my main host machine running Debian 13+ with all of the tools needed. 

# Add packages that needs to be installed
PKGS="wget curl git brave-browser ffmpeg qtile yt-dlp "

echo "Updating package index..."
sudo apt update
echo "Package index updated."

echo "Installing packages: $PKGS"
sudo apt install "$PKGS"

sudo apt upgrade -y

echo "Installing starship prompt"
curl -sS https://starship.rs/install.sh | sh

# Get dotfiles from remote repo



echo "Installing Antigravity CLI"
curl -fsSL https://antigravity.google/cli/install.sh | bash

echo "Omnia installation is complete."



