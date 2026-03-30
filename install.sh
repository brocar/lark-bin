#!/bin/bash

# Check for build dependencies
pacman -Qi git base-devel > /dev/null

# Update the repository and build the package
git pull
makepkg -sic

# Clean up downloaded files
rm *.zst *.deb
