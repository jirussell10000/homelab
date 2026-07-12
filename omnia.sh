#!/bin/bash

WEB_PKGS="wget curl"

TXT_PKGS="vim"

echo "Updating package index..."
sudo apt update -y

echo "Installing packages: $WEB_PKGS"
sudo apt install -y $WEB_PKGS

echo "Installing google antigravity text editor"
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://us-central1-apt.pkg.dev/doc/repo-signing-key.gpg | \
  sudo gpg --dearmor --yes -o /etc/apt/keyrings/antigravity-repo-key.gpg
echo "deb [signed-by=/etc/apt/keyrings/antigravity-repo-key.gpg] https://us-central1-apt.pkg.dev/projects/antigravity-auto-updater-dev/ antigravity-debian main" | \
  sudo tee /etc/apt/sources.list.d/antigravity.list > /dev/null

sudo apt update -y

sudo apt install antigravity

echo "Installation complete."



