#!/usr/bin/env python3
"""
Update script for lark-bin AUR package.
Checks the Lark API for new versions, downloads binaries to calculate checksums,
and updates the PKGBUILD file accordingly.
"""

import hashlib
import re
import sys
import urllib.request
import json
import os

PKGBUILD_PATH = "PKGBUILD"

# API Endpoints
# Platform 10 = Linux x64 DEB, 12 = Linux arm64 DEB
URL_X64 = "https://www.larksuite.com/api/package_info?platform=10"
URL_ARM64 = "https://www.larksuite.com/api/package_info?platform=12"

# Expected version_number prefixes to verify the correct platform is returned
EXPECTED_PREFIX_X64 = "Linux-x64-deb"
EXPECTED_PREFIX_ARM64 = "Linux-arm64-deb"

def get_pkg_info(api_url, expected_prefix=None):
    """Fetch version and download link from Lark API."""
    with urllib.request.urlopen(api_url) as response:
        data = json.loads(response.read().decode())
        pkg = data.get("data", {})
        raw_ver = pkg.get("version_number", "")
        # version_number is like "Linux-x64-deb@V7.59.12" — extract semver only
        match = re.search(r'@V([\d.]+)$', raw_ver)
        version = match.group(1) if match else None
        if expected_prefix and not raw_ver.startswith(expected_prefix):
            print(f"Warning: Platform ID may have changed! Expected prefix '{expected_prefix}', "
                  f"but got '{raw_ver}' from {api_url}")
            print("Update URL_X64 / URL_ARM64 constants with the correct platform IDs.")
            sys.exit(1)
        return version, pkg.get("download_link")

def get_sha256(url):
    """Download a file and calculate its SHA256 hash."""
    print(f"Downloading and calculating hash for {url}...")
    sha256 = hashlib.sha256()
    with urllib.request.urlopen(url) as response:
        while True:
            data = response.read(65536)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def update_pkgbuild(new_ver, sum_x64, sum_arm64):
    """Update PKGBUILD with new version and checksums."""
    with open(PKGBUILD_PATH, "r") as f:
        content = f.read()

    # Regex to find current version
    ver_match = re.search(r"^pkgver=(.*)$", content, re.MULTILINE)
    if not ver_match:
        print("Could not find pkgver in PKGBUILD")
        sys.exit(1)
    
    current_ver = ver_match.group(1)
    
    if current_ver == new_ver:
        print(f"Version {new_ver} is already up to date.")
        # Output for GitHub Actions
        with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
            f.write("updated=false\n")
        return

    print(f"Update found: {current_ver} -> {new_ver}")

    # Update Content
    # 1. Update pkgver
    content = re.sub(r"^pkgver=.*$", f"pkgver={new_ver}", content, flags=re.MULTILINE)
    # 2. Reset pkgrel to 1
    content = re.sub(r"^pkgrel=.*$", "pkgrel=1", content, flags=re.MULTILINE)
    # 3. Update sha256sums
    content = re.sub(
        r"sha256sums_x86_64=\('.*'\)", 
        f"sha256sums_x86_64=('{sum_x64}')", 
        content
    )
    content = re.sub(
        r"sha256sums_aarch64=\('.*'\)", 
        f"sha256sums_aarch64=('{sum_arm64}')", 
        content
    )

    with open(PKGBUILD_PATH, "w") as f:
        f.write(content)
    
    print("PKGBUILD updated successfully.")
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
        f.write("updated=true\n")
        f.write(f"version={new_ver}\n")

if __name__ == "__main__":
    try:
        print("Checking for Lark updates...")
        ver_x64, link_x64 = get_pkg_info(URL_X64, EXPECTED_PREFIX_X64)
        ver_arm64, link_arm64 = get_pkg_info(URL_ARM64, EXPECTED_PREFIX_ARM64)
        
        print(f"Latest version - x64: {ver_x64}, arm64: {ver_arm64}")

        if ver_x64 is None or link_x64 is None or ver_arm64 is None or link_arm64 is None:
            print("Error: Failed to retrieve version or download link from API.")
            sys.exit(1)

        if ver_x64 != ver_arm64:
            print(f"Warning: Versions differ! x64: {ver_x64}, arm64: {ver_arm64}. Using x64.")
        
        # Check against local file before downloading huge binaries
        if os.path.exists(PKGBUILD_PATH):
            with open(PKGBUILD_PATH, "r") as f:
                if f"pkgver={ver_x64}" in f.read():
                    print(f"Version {ver_x64} is already up to date.")
                    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
                        f.write("updated=false\n")
                    sys.exit(0)
        else:
            print(f"Error: PKGBUILD not found at {PKGBUILD_PATH}")
            sys.exit(1)

        # Download and calculate hashes
        hash_x64 = get_sha256(link_x64)
        hash_arm64 = get_sha256(link_arm64)
        
        print(f"x86_64 SHA256: {hash_x64}")
        print(f"aarch64 SHA256: {hash_arm64}")

        update_pkgbuild(ver_x64, hash_x64, hash_arm64)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
