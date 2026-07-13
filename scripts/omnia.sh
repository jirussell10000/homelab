#!/bin/bash

WEB_PKGS="wget curl"

echo "Updating package index..."
sudo apt update -y

echo "Installing packages: $WEB_PKGS"
sudo apt install -y "$WEB_PKGS"

sudo apt update -y

sudo apt install antigravity

echo "Installation complete."



