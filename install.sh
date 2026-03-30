#!/bin/bash

# Install build dependencies
sudo pacman -S --needed git base-devel

# Update the repository and build the package
git pull
makepkg -sic

# Clean up downloaded files
rm *.zst *.deb
